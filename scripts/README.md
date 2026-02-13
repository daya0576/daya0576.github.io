# Sync Blog to Dify Knowledge

Automatically sync blog posts to Dify Knowledge Base for AI assistant retrieval.

## Usage

### Local Execution

```bash
# Copy environment template
cp .env.example .env

# Edit .env and fill in your credentials
# DIFY_API_KEY=your-dataset-api-key
# DIFY_DATASET_ID=your-dataset-id

# Load environment variables
source .env  # or: export $(cat .env | xargs)

# Upload all files (skip existing)
python scripts/upload_to_dify.py --skip-existing

# Test mode (dry run)
python scripts/upload_to_dify.py --dry-run
```

### GitHub Actions

Automatically triggered on push to `content/` directory, uploads new or modified files.

Configure in Repository Settings → Secrets:
- `DIFY_API_KEY`: Dify Dataset API Key
- `DIFY_DATASET_ID`: Dataset ID

## Files

- **`scripts/upload_to_dify.py`**: Upload script
- **`scripts/requirements.txt`**: Python dependencies
- **`scripts/test_upload.py`**: Test suite
- **`.github/workflows/sync-to-dify.yaml`**: GitHub Actions configuration

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--skip-existing` | Skip documents that already exist (recommended) |
| `--dry-run` | Test mode, no actual upload |
| `--delay` | Upload interval in seconds (default: 1.0) |
