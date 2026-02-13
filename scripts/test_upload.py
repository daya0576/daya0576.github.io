#!/usr/bin/env python3
"""
Test suite for upload_to_dify.py

Run tests:
    python scripts/test_upload.py
    python scripts/test_upload.py -v  # verbose mode
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from upload_to_dify import (
    DifyConfig,
    DifyKnowledgeClient,
    extract_frontmatter,
    get_document_name,
    collect_content_files,
)


class TestExtractFrontmatter(unittest.TestCase):
    """Test frontmatter extraction."""

    def test_extract_valid_frontmatter(self):
        """Test extracting valid YAML frontmatter."""
        content = """---
title: "Test Title"
date: 2026-01-01
tags: ["tag1", "tag2"]
---

Content here"""
        frontmatter = extract_frontmatter(content)
        
        self.assertEqual(frontmatter["title"], "Test Title")
        self.assertEqual(frontmatter["date"], "2026-01-01")

    def test_extract_no_frontmatter(self):
        """Test content without frontmatter."""
        content = "Just plain content"
        frontmatter = extract_frontmatter(content)
        
        self.assertEqual(frontmatter, {})

    def test_extract_empty_frontmatter(self):
        """Test empty frontmatter."""
        content = """---
---

Content"""
        frontmatter = extract_frontmatter(content)
        
        self.assertEqual(frontmatter, {})


class TestGetDocumentName(unittest.TestCase):
    """Test document name generation."""

    def test_name_from_frontmatter(self):
        """Test getting name from frontmatter title."""
        file_path = Path("test.md")
        frontmatter = {"title": "My Title"}
        
        name = get_document_name(file_path, frontmatter)
        
        self.assertEqual(name, "My Title")

    def test_name_from_filename(self):
        """Test fallback to filename."""
        file_path = Path("my-post.md")
        frontmatter = {}
        
        name = get_document_name(file_path, frontmatter)
        
        self.assertEqual(name, "my-post")


class TestDifyConfig(unittest.TestCase):
    """Test Dify configuration."""

    def test_config_creation(self):
        """Test creating configuration."""
        config = DifyConfig(
            api_key="test-key",
            dataset_id="test-id"
        )
        
        self.assertEqual(config.api_key, "test-key")
        self.assertEqual(config.dataset_id, "test-id")
        self.assertEqual(config.api_base, "https://api.dify.ai/v1")

    def test_config_custom_base(self):
        """Test configuration with custom base URL."""
        config = DifyConfig(
            api_key="test-key",
            api_base="https://custom.api"
        )
        
        self.assertEqual(config.api_base, "https://custom.api")


class TestDifyKnowledgeClient(unittest.TestCase):
    """Test Dify API client."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = DifyConfig(
            api_key="test-key",
            dataset_id="test-dataset"
        )
        self.client = DifyKnowledgeClient(self.config)

    @patch('upload_to_dify.requests.Session')
    def test_client_headers(self, mock_session_class):
        """Test client sets correct headers."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        
        client = DifyKnowledgeClient(self.config)
        
        mock_session.headers.update.assert_called_once()
        headers = mock_session.headers.update.call_args[0][0]
        self.assertEqual(headers["Authorization"], "Bearer test-key")

    @patch.object(DifyKnowledgeClient, '_request')
    def test_list_datasets(self, mock_request):
        """Test listing datasets."""
        mock_request.return_value = {"data": [{"id": "1", "name": "Test"}]}
        
        result = self.client.list_datasets()
        
        mock_request.assert_called_once_with(
            "GET", "/datasets", params={"page": 1, "limit": 20}
        )
        self.assertEqual(len(result["data"]), 1)

    @patch.object(DifyKnowledgeClient, '_request')
    def test_create_document(self, mock_request):
        """Test creating document."""
        mock_request.return_value = {
            "document": {"id": "doc-123"},
            "batch": "batch-456"
        }
        
        result = self.client.create_document_by_text(
            dataset_id="test-dataset",
            name="Test Doc",
            text="Test content"
        )
        
        mock_request.assert_called_once()
        self.assertEqual(result["document"]["id"], "doc-123")

    @patch.object(DifyKnowledgeClient, 'list_documents')
    def test_get_all_document_names(self, mock_list_docs):
        """Test getting all document names."""
        mock_list_docs.side_effect = [
            {
                "data": [
                    {"name": "Doc 1"},
                    {"name": "Doc 2"}
                ],
                "has_more": True
            },
            {
                "data": [
                    {"name": "Doc 3"}
                ],
                "has_more": False
            }
        ]
        
        names = self.client.get_all_document_names("test-dataset")
        
        self.assertEqual(len(names), 3)
        self.assertIn("Doc 1", names)
        self.assertIn("Doc 3", names)


class TestCollectContentFiles(unittest.TestCase):
    """Test file collection."""

    def test_collect_markdown_files(self):
        """Test collecting markdown files."""
        with patch('pathlib.Path.rglob') as mock_rglob:
            mock_rglob.return_value = [
                Path("test1.md"),
                Path("test2.markdown")
            ]
            
            content_dir = Path("/fake/content")
            files = collect_content_files(content_dir)
            
            # rglob is called for each extension
            self.assertEqual(mock_rglob.call_count, 2)


class TestIntegration(unittest.TestCase):
    """Integration tests."""

    @patch('upload_to_dify.requests.Session')
    def test_full_workflow(self, mock_session_class):
        """Test complete workflow."""
        # Mock session
        mock_session = MagicMock()
        mock_response = Mock()
        mock_response.text = '{"data": []}'
        mock_response.json.return_value = {"data": []}
        mock_session.request.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        # Create client
        config = DifyConfig(api_key="test-key")
        client = DifyKnowledgeClient(config)
        
        # Test listing datasets
        result = client.list_datasets()
        
        self.assertIn("data", result)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
