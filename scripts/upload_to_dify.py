#!/usr/bin/env python3
"""
Upload blog content files to Dify Knowledge Base.

This script traverses all markdown files under the content directory
and uploads them to Dify Knowledge API.

Usage:
    1. Set environment variables:
       export DIFY_API_KEY="your-api-key"
       export DIFY_DATASET_ID="your-dataset-id"  # Optional, will create new if not set
    
    2. Run the script:
       python scripts/upload_to_dify.py

API Reference:
    - Create document by text: POST /datasets/{dataset_id}/document/create-by-text
    - Create dataset: POST /datasets
"""

import os
import re
import sys
import time
import logging
import argparse
import subprocess
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# Constants
DIFY_API_BASE = "https://api.dify.ai/v1"
CONTENT_DIR = Path(__file__).parent.parent / "content"
SUPPORTED_EXTENSIONS = {".md", ".markdown"}


@dataclass
class DifyConfig:
    """Dify API configuration."""
    api_key: str
    api_base: str = DIFY_API_BASE
    dataset_id: Optional[str] = None
    dataset_name: str = "Henry's Blog"


class DifyKnowledgeClient:
    """Client for Dify Knowledge API."""

    def __init__(self, config: DifyConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
        })

    def _request(self, method: str, endpoint: str, max_retries: int = 3, **kwargs) -> dict:
        """Make a request to the Dify API with retry logic."""
        url = f"{self.config.api_base}{endpoint}"
        
        for attempt in range(max_retries):
            try:
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                return response.json() if response.text else {}
                
            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code
                
                # Check if it's a rate limit error (403 or 429)
                if status_code in (403, 429):
                    if attempt < max_retries - 1:
                        # Wait 60 seconds before retry
                        wait_time = 60
                        logger.warning(f"Rate limit hit (attempt {attempt + 1}/{max_retries})")
                        logger.warning(f"Waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                        continue
                
                # For other errors or last attempt, log and raise
                logger.error(f"HTTP error: {e}")
                logger.error(f"Response: {e.response.text}")
                raise
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error: {e}")
                raise
        
        # Should not reach here, but just in case
        raise Exception(f"Failed after {max_retries} attempts")

    def list_datasets(self, page: int = 1, limit: int = 20) -> dict:
        """List all datasets."""
        return self._request("GET", "/datasets", params={"page": page, "limit": limit})

    def create_dataset(self, name: str, description: str = "") -> dict:
        """Create a new dataset (knowledge base)."""
        payload = {
            "name": name,
            "description": description,
            "indexing_technique": "high_quality",
            "permission": "only_me",
        }
        return self._request("POST", "/datasets", json=payload)

    def get_or_create_dataset(self, name: str, description: str = "") -> str:
        """Get existing dataset by name or create a new one."""
        # List existing datasets
        result = self.list_datasets(limit=100)
        datasets = result.get("data", [])
        
        # Check if dataset with the same name exists
        for dataset in datasets:
            if dataset.get("name") == name:
                logger.info(f"Found existing dataset: {name} (ID: {dataset['id']})")
                return dataset["id"]
        
        # Create new dataset
        logger.info(f"Creating new dataset: {name}")
        result = self.create_dataset(name, description)
        dataset_id = result.get("id")
        logger.info(f"Created dataset: {name} (ID: {dataset_id})")
        return dataset_id

    def create_document_by_text(
        self,
        dataset_id: str,
        name: str,
        text: str,
        indexing_technique: str = "high_quality",
        process_rule: Optional[dict] = None,
    ) -> dict:
        """Create a document by text content."""
        if process_rule is None:
            process_rule = {
                "mode": "automatic",
            }

        payload = {
            "name": name,
            "text": text,
            "indexing_technique": indexing_technique,
            "process_rule": process_rule,
        }

        return self._request(
            "POST",
            f"/datasets/{dataset_id}/document/create-by-text",
            json=payload,
        )

    def list_documents(self, dataset_id: str, page: int = 1, limit: int = 20) -> dict:
        """List documents in a dataset."""
        return self._request(
            "GET",
            f"/datasets/{dataset_id}/documents",
            params={"page": page, "limit": limit},
        )

    def get_all_document_names(self, dataset_id: str) -> set[str]:
        """Get all document names in a dataset.
        
        Returns:
            Set of document names
        """
        all_names = set()
        page = 1
        limit = 100
        
        while True:
            result = self.list_documents(dataset_id, page=page, limit=limit)
            documents = result.get("data", [])
            
            for doc in documents:
                name = doc.get("name", "")
                if name:
                    all_names.add(name)
            
            # Check if there are more pages
            if not result.get("has_more", False):
                break
            page += 1
        
        logger.info(f"Found {len(all_names)} existing document(s) in dataset")
        return all_names


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    
    frontmatter = {}
    for line in match.group(1).split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            frontmatter[key.strip()] = value.strip().strip('"').strip("'")
    return frontmatter


def get_document_name(file_path: Path, frontmatter: dict) -> str:
    """Generate document name from file path or frontmatter title."""
    return frontmatter.get("title", file_path.stem)


def collect_content_files(content_dir: Path) -> list[Path]:
    """Collect all markdown files under content directory."""
    files = []
    for ext in SUPPORTED_EXTENSIONS:
        files.extend(content_dir.rglob(f"*{ext}"))
    return sorted(files)


def get_changed_files(content_dir: Path, base_ref: str = "HEAD~1") -> list[Path]:
    """Get changed markdown files using git diff.
    
    Args:
        content_dir: Content directory path
        base_ref: Git reference to compare against (default: HEAD~1)
    
    Returns:
        List of changed file paths
    """
    try:
        # Get the repository root
        repo_root = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        repo_root = Path(repo_root)

        # Get changed files (added, modified, renamed)
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=AMR", base_ref, "HEAD"],
            capture_output=True,
            text=True,
            check=True,
            cwd=repo_root,
        )

        changed_files = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            file_path = repo_root / line
            # Only include files in content directory with supported extensions
            if (
                file_path.suffix.lower() in SUPPORTED_EXTENSIONS
                and content_dir in file_path.parents or file_path.parent == content_dir
            ):
                if file_path.exists():
                    changed_files.append(file_path)

        return sorted(changed_files)

    except subprocess.CalledProcessError as e:
        logger.warning(f"Git command failed: {e}")
        logger.warning("Falling back to all files")
        return collect_content_files(content_dir)


def upload_files_to_dify(
    client: DifyKnowledgeClient,
    dataset_id: str,
    files: list[Path],
    dry_run: bool = False,
    delay: float = 1.0,
    existing_names: Optional[set[str]] = None,
) -> tuple[int, int, int]:
    """Upload files to Dify Knowledge Base.
    
    Returns:
        Tuple of (success_count, failure_count, skipped_count)
    """
    success_count = 0
    failure_count = 0
    skipped_count = 0

    for i, file_path in enumerate(files, 1):
        try:
            # Read file content
            content = file_path.read_text(encoding="utf-8")
            
            # Extract frontmatter and get document name
            frontmatter = extract_frontmatter(content)
            doc_name = get_document_name(file_path, frontmatter)
            
            # Calculate relative path for logging
            try:
                rel_path = file_path.relative_to(CONTENT_DIR.parent)
            except ValueError:
                # If file is not under CONTENT_DIR.parent, use absolute path
                rel_path = file_path

            logger.info(f"[{i}/{len(files)}] Processing: {rel_path}")
            logger.info(f"  Title: {doc_name}")

            # Skip if document already exists
            if existing_names and doc_name in existing_names:
                logger.info("  ⏭ Skipped (already exists in dataset)")
                skipped_count += 1
                continue

            if dry_run:
                logger.info("  [DRY RUN] Would upload this document")
                success_count += 1
                continue

            # Upload to Dify
            result = client.create_document_by_text(
                dataset_id=dataset_id,
                name=doc_name,
                text=content,  # Upload full content including frontmatter
            )

            doc_id = result.get("document", {}).get("id", "unknown")
            batch = result.get("batch", "unknown")
            logger.info(f"  ✓ Uploaded successfully (doc_id: {doc_id}, batch: {batch})")
            success_count += 1

            # Rate limiting - wait between requests
            if i < len(files):
                time.sleep(delay)

        except Exception as e:
            logger.error(f"  ✗ Failed to upload: {e}")
            failure_count += 1

    return success_count, failure_count, skipped_count


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Upload blog content files to Dify Knowledge Base"
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("DIFY_API_KEY"),
        help="Dify API key (default: $DIFY_API_KEY)",
    )
    parser.add_argument(
        "--api-base",
        default=os.environ.get("DIFY_API_BASE", DIFY_API_BASE),
        help=f"Dify API base URL (default: {DIFY_API_BASE})",
    )
    parser.add_argument(
        "--dataset-id",
        default=os.environ.get("DIFY_DATASET_ID"),
        help="Dify dataset ID (default: $DIFY_DATASET_ID)",
    )
    parser.add_argument(
        "--dataset-name",
        default="Henry's Blog",
        help="Name for new dataset if dataset-id is not provided",
    )
    parser.add_argument(
        "--content-dir",
        type=Path,
        default=CONTENT_DIR,
        help=f"Content directory to scan (default: {CONTENT_DIR})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without uploading",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between uploads in seconds (default: 1.0)",
    )
    parser.add_argument(
        "--list-datasets",
        action="store_true",
        help="List existing datasets and exit",
    )
    parser.add_argument(
        "--changed-only",
        action="store_true",
        help="Only upload files changed since last commit",
    )
    parser.add_argument(
        "--base-ref",
        default="HEAD~1",
        help="Git reference to compare against (default: HEAD~1)",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip files that already exist in the dataset (by document name)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validate API key
    if not args.api_key:
        logger.error("DIFY_API_KEY environment variable is not set")
        logger.error("Please set it: export DIFY_API_KEY='your-api-key'")
        sys.exit(1)

    # Initialize client
    config = DifyConfig(
        api_key=args.api_key,
        api_base=args.api_base,
        dataset_id=args.dataset_id,
        dataset_name=args.dataset_name,
    )
    client = DifyKnowledgeClient(config)

    # List datasets mode
    if args.list_datasets:
        logger.info("Listing datasets...")
        result = client.list_datasets(limit=100)
        datasets = result.get("data", [])
        if not datasets:
            logger.info("No datasets found")
        else:
            logger.info(f"Found {len(datasets)} dataset(s):")
            for ds in datasets:
                logger.info(f"  - {ds['name']} (ID: {ds['id']})")
        return

    # Get or create dataset
    if args.dry_run and not args.dataset_id:
        dataset_id = "dry-run-dataset-id"
        logger.info(f"[DRY RUN] Would use or create dataset: {args.dataset_name}")
    elif args.dataset_id:
        dataset_id = args.dataset_id
        logger.info(f"Using existing dataset ID: {dataset_id}")
    else:
        dataset_id = client.get_or_create_dataset(
            args.dataset_name,
            description="Blog content from changchen.me",
        )

    # Collect content files
    content_dir = args.content_dir
    if not content_dir.exists():
        logger.error(f"Content directory not found: {content_dir}")
        sys.exit(1)

    logger.info(f"Scanning content directory: {content_dir}")
    
    # Collect files based on mode
    if args.changed_only:
        logger.info(f"Mode: Changed files only (base: {args.base_ref})")
        files = get_changed_files(content_dir, args.base_ref)
    else:
        logger.info("Mode: All files")
        files = collect_content_files(content_dir)
    
    logger.info(f"Found {len(files)} file(s) to upload")

    if not files:
        logger.warning("No files found to upload")
        return

    # Get existing document names if skip-existing is enabled
    existing_names = None
    if args.skip_existing and not args.dry_run:
        logger.info("Fetching existing documents from dataset...")
        existing_names = client.get_all_document_names(dataset_id)

    # Upload files
    if args.dry_run:
        logger.info("=== DRY RUN MODE ===")

    logger.info(f"Starting upload to dataset: {dataset_id}")
    success, failure, skipped = upload_files_to_dify(
        client=client,
        dataset_id=dataset_id,
        files=files,
        dry_run=args.dry_run,
        delay=args.delay,
        existing_names=existing_names,
    )

    # Summary
    logger.info("=" * 50)
    logger.info("Upload Summary:")
    logger.info(f"  Total files:  {len(files)}")
    logger.info(f"  Successful:   {success}")
    logger.info(f"  Skipped:      {skipped}")
    logger.info(f"  Failed:       {failure}")

    if failure > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
