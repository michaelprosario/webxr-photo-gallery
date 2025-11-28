# Environment Variable Management Setup

## What Was Added

### 1. Python-dotenv Integration

**Added to `requirements.txt`:**
```
python-dotenv==1.0.0
```

**Updated `main.py`:**
```python
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
```

### 2. Configuration Files

**`.env.example`** - Template for environment configuration
```bash
ARCHIVE_PATH=/workspaces/webxr-photo-gallery/my_archive
SCENE_OUTPUT_PATH=/workspaces/webxr-photo-gallery/sceneOutput
GEMINI_API_KEY=your-api-key-here
```

**`.env`** - Active configuration (already exists, not in version control)

### 3. Verification Tool

**`check_env.py`** - Environment configuration checker
- Verifies `.env` file exists
- Checks GEMINI_API_KEY is set
- Validates optional configuration paths
- Confirms all dependencies installed
- Provides helpful error messages

## How It Works

### Automatic Loading

When you start the application:
```bash
python main.py
```

The app automatically:
1. Loads `load_dotenv()` from `python-dotenv`
2. Reads the `.env` file in the project root
3. Sets all variables as environment variables
4. Makes them available via `os.getenv()`

### No Manual Exports Needed

**Before (manual):**
```bash
export GEMINI_API_KEY="your-key"
export ARCHIVE_PATH="/path/to/archive"
python main.py
```

**After (automatic):**
```bash
# Just edit .env once
python main.py  # Variables auto-loaded
```

## User Workflow

### First-Time Setup

```bash
# 1. Copy template
cp .env.example .env

# 2. Edit with your values
nano .env  # or vim, code, etc.

# 3. Verify configuration
python check_env.py

# 4. Start server
python main.py
```

### Verification Output

```
============================================================
  Environment Configuration Check
============================================================

1. Loading .env file...
   ✓ .env file found and loaded

2. Checking GEMINI_API_KEY...
   ✓ GEMINI_API_KEY is set: AIzaSyDyW8...k_Gg

3. Checking optional configuration...
   Archive Path: /workspaces/webxr-photo-gallery/my_archive
   ✓ Archive directory exists
   Scene Output Path: /workspaces/webxr-photo-gallery/sceneOutput
   ✓ Scene output directory exists

4. Checking dependencies...
   ✓ All required packages installed

============================================================
  ✓ Configuration check complete!
============================================================
```

## Benefits

### 1. **Persistence**
- Variables survive terminal restarts
- No need to re-export on each session

### 2. **Security**
- `.env` excluded from git (via `.gitignore`)
- API keys not hardcoded in source
- Safe to share `.env.example` template

### 3. **Simplicity**
- Single file for all configuration
- Easy to update and maintain
- Clear separation of config from code

### 4. **Developer Experience**
- Quick setup with `cp .env.example .env`
- Self-documenting via comments
- Verification tool catches issues early

## Files Updated

### Code Changes
- `main.py` - Added `load_dotenv()` import and call
- `requirements.txt` - Added `python-dotenv==1.0.0`

### Documentation Updates
- `README.md` - Added .env setup instructions
- `AFRAME_GUIDE.md` - Updated prerequisites section
- `QUICK_REFERENCE.md` - Added .env quick reference
- `.env.example` - Enhanced comments and instructions

### New Files
- `check_env.py` - Configuration verification tool

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | Yes* | None | Google Gemini API key for VR gallery generation |
| `ARCHIVE_PATH` | No | `./photo_archive` | Photo collection storage path |
| `SCENE_OUTPUT_PATH` | No | `./sceneOutput` | VR scene output path |

*Required only for VR gallery generation feature

## Troubleshooting

### .env file not loading

**Symptoms:**
- "GEMINI_API_KEY environment variable not set" error
- Variables show as None in Python

**Solutions:**
1. Ensure `.env` is in project root (same directory as `main.py`)
2. Check file permissions: `ls -la .env`
3. Restart the server after editing `.env`
4. Run verification: `python check_env.py`

### API key not recognized

**Solutions:**
1. Check for quotes in `.env`:
   - ✓ Correct: `GEMINI_API_KEY=AIza...`
   - ✗ Wrong: `GEMINI_API_KEY="AIza..."` (quotes not needed)
2. Check for spaces:
   - ✓ Correct: `GEMINI_API_KEY=value`
   - ✗ Wrong: `GEMINI_API_KEY = value` (no spaces)
3. Ensure no placeholder: `GEMINI_API_KEY=your-api-key-here`

### Variables work in terminal but not in app

**Solution:**
The app only reads from `.env` file, not from shell exports. Put all variables in `.env`.

## Best Practices

### Development
1. Always use `.env` for local development
2. Keep `.env.example` up to date with new variables
3. Document each variable in `.env.example`
4. Run `check_env.py` before committing changes

### Production
1. Use environment-specific `.env` files
2. Never commit `.env` to version control
3. Use secure secret management in production
4. Rotate API keys regularly

### Security
1. Add `.env` to `.gitignore` (already done)
2. Use different keys for dev/prod
3. Don't share `.env` files
4. Use `.env.example` as template only

## Migration Guide

If you were using manual exports:

**Before:**
```bash
# In ~/.bashrc or startup script
export GEMINI_API_KEY="..."
export ARCHIVE_PATH="..."
```

**After:**
1. Create `.env` file:
```bash
cp .env.example .env
```

2. Move variables to `.env`:
```bash
GEMINI_API_KEY=your-actual-key
ARCHIVE_PATH=/workspaces/webxr-photo-gallery/my_archive
SCENE_OUTPUT_PATH=/workspaces/webxr-photo-gallery/sceneOutput
```

3. Remove from shell startup scripts (optional)

4. Start server normally:
```bash
python main.py
```

## Implementation Details

### Load Order
1. `main.py` imports `load_dotenv`
2. Calls `load_dotenv()` before other imports
3. Reads `.env` file from current directory
4. Sets variables in `os.environ`
5. Rest of application uses `os.getenv()`

### Override Behavior
- Existing environment variables take precedence
- `.env` only sets variables that aren't already set
- Can override with: `load_dotenv(override=True)`

### Multiple .env Files
Currently not used, but supported:
```python
load_dotenv('.env.production')  # Production settings
load_dotenv('.env.local')       # Local overrides
```

## Testing

```bash
# Test .env loading
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('GEMINI_API_KEY'))"

# Full configuration check
python check_env.py

# Test in application
python -c "import main; print('Success!')"
```

## Summary

Environment variables are now managed through:
- ✅ `.env` file for configuration
- ✅ `python-dotenv` for automatic loading
- ✅ `check_env.py` for verification
- ✅ Updated documentation
- ✅ Secure, persistent, simple workflow
