# Readio Setup Guide

## Quick Start

1. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

## Alternative: Use the run script
```bash
./run.sh
```

## Environment Variables

Create a `.env` file in the root directory with your API keys:
```
LLAMA4_API_BASE=your_llama4_api_base
LLAMA4_API_KEY=your_llama4_api_key
PLAYHT_API_KEY=your_playht_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
```

## Virtual Environment

- **Activate:** `source venv/bin/activate`
- **Deactivate:** `deactivate`
- **Install new package:** `pip install package_name`
- **Update requirements:** `pip freeze > requirements.txt`

## Troubleshooting

If you get import errors:
1. Make sure the virtual environment is activated
2. Run `pip install -r requirements.txt`
3. Check that you're using Python 3 (not Python 2) 