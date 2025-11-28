#!/usr/bin/env python3
"""
Environment Configuration Check
Verifies that .env file is properly configured
"""

import os
from dotenv import load_dotenv

def check_env():
    """Check environment configuration"""
    print("="*60)
    print("  Environment Configuration Check")
    print("="*60)
    
    # Load .env file
    print("\n1. Loading .env file...")
    if os.path.exists('.env'):
        load_dotenv()
        print("   ✓ .env file found and loaded")
    else:
        print("   ✗ .env file not found!")
        print("   → Run: cp .env.example .env")
        return False
    
    # Check GEMINI_API_KEY
    print("\n2. Checking GEMINI_API_KEY...")
    gemini_key = os.getenv('GEMINI_API_KEY')
    if gemini_key and gemini_key != 'your-api-key-here':
        masked_key = gemini_key[:10] + "..." + gemini_key[-4:] if len(gemini_key) > 14 else "***"
        print(f"   ✓ GEMINI_API_KEY is set: {masked_key}")
    elif gemini_key == 'your-api-key-here':
        print("   ⚠ GEMINI_API_KEY is set to placeholder value")
        print("   → Update .env with your actual API key")
        print("   → Get key at: https://aistudio.google.com/app/apikey")
    else:
        print("   ✗ GEMINI_API_KEY is not set")
        print("   → Add to .env: GEMINI_API_KEY=your-actual-key")
        return False
    
    # Check optional paths
    print("\n3. Checking optional configuration...")
    archive_path = os.getenv('ARCHIVE_PATH', './photo_archive')
    scene_path = os.getenv('SCENE_OUTPUT_PATH', './sceneOutput')
    
    print(f"   Archive Path: {archive_path}")
    if os.path.exists(archive_path):
        print("   ✓ Archive directory exists")
    else:
        print("   ℹ Archive directory will be created on first import")
    
    print(f"   Scene Output Path: {scene_path}")
    if os.path.exists(scene_path):
        print("   ✓ Scene output directory exists")
    else:
        print("   ℹ Scene directory will be created on first generation")
    
    # Check dependencies
    print("\n4. Checking dependencies...")
    try:
        import fastapi
        import uvicorn
        import google.generativeai
        from PIL import Image
        print("   ✓ All required packages installed")
    except ImportError as e:
        print(f"   ✗ Missing dependency: {e}")
        print("   → Run: pip install -r requirements.txt")
        return False
    
    print("\n" + "="*60)
    print("  ✓ Configuration check complete!")
    print("="*60)
    print("\nYou're ready to start the server:")
    print("  python main.py")
    print("\nAPI will be available at:")
    print("  http://localhost:8000")
    print("  http://localhost:8000/docs (interactive documentation)")
    print()
    
    return True

if __name__ == "__main__":
    check_env()
