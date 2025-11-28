#!/usr/bin/env python3
"""
Example script demonstrating the A-Frame VR Gallery API
This script shows how to use the API programmatically with Python
"""

import requests
import json
import os
import time

# Configuration
API_BASE_URL = "http://localhost:8000"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def check_api_health():
    """Check if the API is running"""
    print_section("1. Checking API Health")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ API is healthy!")
            print(f"  Status: {data['status']}")
            print(f"  Timestamp: {data['timestamp']}")
            return True
        else:
            print(f"✗ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to API at {API_BASE_URL}")
        print("  Make sure the server is running: python main.py")
        return False

def list_collections():
    """List all available photo collections"""
    print_section("2. Listing Photo Collections")
    try:
        response = requests.get(f"{API_BASE_URL}/collections")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {data['total_collections']} collection(s):")
            
            collections = []
            for collection in data['collections']:
                print(f"\n  📁 {collection['collection_name']}")
                print(f"     Photos: {collection['photo_count']}")
                print(f"     Size: {collection['total_size_bytes']:,} bytes")
                print(f"     Folder: {collection['folder_name']}")
                collections.append(collection['folder_name'])
            
            return collections
        else:
            print(f"✗ Error listing collections: {response.status_code}")
            return []
    except Exception as e:
        print(f"✗ Error: {e}")
        return []

def import_sample_collection():
    """Import a sample collection (if available)"""
    print_section("3. Import Sample Collection (Optional)")
    
    sample_folder = "/workspaces/webxr-photo-gallery/FrancisRosarioAlbum"
    
    if not os.path.exists(sample_folder):
        print("⊘ Sample folder not found, skipping import")
        return None
    
    print(f"Importing from: {sample_folder}")
    
    payload = {
        "source_folder": sample_folder,
        "collection_name": "Francis Rosario Album",
        "max_width": 1920,
        "max_height": 1080,
        "quality": 85
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/import",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Import successful!")
            print(f"  Collection: {data['collection_name']}")
            print(f"  Imported: {data['imported_count']} photos")
            print(f"  Failed: {data['failed_count']} photos")
            return data['collection_name']
        else:
            print(f"✗ Import failed: {response.status_code}")
            print(f"  {response.text}")
            return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def generate_vr_gallery(collection_names):
    """Generate an A-Frame VR gallery"""
    print_section("4. Generating VR Gallery")
    
    if not collection_names:
        print("✗ No collections available for gallery generation")
        return None
    
    if not GEMINI_API_KEY:
        print("⚠ Warning: GEMINI_API_KEY not set!")
        print("  Set it with: export GEMINI_API_KEY='your-key'")
        print("  Get your key at: https://aistudio.google.com/app/apikey")
        return None
    
    scene_name = f"demo_gallery_{int(time.time())}"
    
    payload = {
        "collection_names": collection_names[:3],  # Limit to first 3 collections
        "scene_name": scene_name
    }
    
    print(f"Generating gallery for collections: {', '.join(payload['collection_names'])}")
    print("This may take 10-30 seconds as Gemini AI creates your gallery...")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/scenes/generate",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60  # Allow up to 60 seconds for generation
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ Gallery generated successfully!")
            print(f"  Scene Name: {data['scene_name']}")
            print(f"  Collections: {', '.join(data['collections'])}")
            print(f"  Total Photos: {data['photo_count']}")
            print(f"  Created: {data['created_at']}")
            print(f"\n  📄 HTML File: {data['file_path']}")
            print(f"\n  🎨 Open the HTML file in your browser to view the VR gallery!")
            return data
        else:
            print(f"\n✗ Generation failed: {response.status_code}")
            print(f"  {response.text}")
            return None
    except requests.exceptions.Timeout:
        print("\n✗ Request timed out (>60s)")
        print("  Gemini API might be slow, try again later")
        return None
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return None

def list_generated_scenes():
    """List all generated VR gallery scenes"""
    print_section("5. Listing Generated Scenes")
    
    try:
        response = requests.get(f"{API_BASE_URL}/scenes")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {data['total_scenes']} generated scene(s):")
            
            for scene in data['scenes']:
                print(f"\n  🎨 {scene['scene_name']}")
                print(f"     Collections: {', '.join(scene['collections'])}")
                print(f"     Photos: {scene['photo_count']}")
                print(f"     Created: {scene['created_at']}")
                print(f"     File: {scene['file_path']}")
            
            return data['scenes']
        else:
            print(f"✗ Error listing scenes: {response.status_code}")
            return []
    except Exception as e:
        print(f"✗ Error: {e}")
        return []

def main():
    """Main execution flow"""
    print("\n" + "🎨"*30)
    print("  WebXR Photo Gallery - A-Frame VR Scene Generator")
    print("  Python API Example")
    print("🎨"*30)
    
    # Step 1: Check API health
    if not check_api_health():
        return
    
    # Step 2: List existing collections
    collections = list_collections()
    
    # Step 3: Optional - Import sample collection
    if not collections:
        print("\nNo collections found. Attempting to import sample...")
        imported = import_sample_collection()
        if imported:
            collections = list_collections()
    
    # Step 4: Generate VR gallery
    if collections:
        generate_vr_gallery(collections)
    
    # Step 5: List all generated scenes
    list_generated_scenes()
    
    print_section("Complete!")
    print("\nNext Steps:")
    print("  1. Open the generated HTML file in your web browser")
    print("  2. Use WASD keys to move, mouse to look around")
    print("  3. Enjoy your immersive VR photo gallery!")
    print("\nAPI Documentation: http://localhost:8000/docs")
    print()

if __name__ == "__main__":
    main()
