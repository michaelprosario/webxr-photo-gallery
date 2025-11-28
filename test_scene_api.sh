#!/bin/bash

# Test script for A-Frame Scene Generation API
# Make sure to set GEMINI_API_KEY environment variable before running

BASE_URL="http://localhost:8000"

echo "=== Testing A-Frame Scene Generation API ==="
echo ""

# Check if server is running
echo "1. Checking API health..."
curl -s $BASE_URL/health | jq '.'
echo ""

# List collections
echo "2. Listing available collections..."
curl -s $BASE_URL/collections | jq '.collections[] | {collection_name, photo_count}'
echo ""

# Get user input for collection names
echo "3. Example: Generate VR gallery scene"
echo ""
echo "Sample curl command:"
echo "curl -X POST \"$BASE_URL/scenes/generate\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{"
echo "    \"collection_names\": [\"FrancisRosarioAlbum\"],"
echo "    \"scene_name\": \"my_vr_gallery\""
echo "  }'"
echo ""

# List scenes
echo "4. Listing all generated scenes..."
curl -s $BASE_URL/scenes | jq '.'
echo ""

echo "=== Test Complete ==="
echo ""
echo "To generate a scene, run:"
echo "curl -X POST \"$BASE_URL/scenes/generate\" -H \"Content-Type: application/json\" -d '{\"collection_names\": [\"YOUR_COLLECTION_NAME\"], \"scene_name\": \"my_gallery\"}'"
echo ""
echo "Generated scenes will be saved in: ./sceneOutput/"
echo "Open the HTML files in a web browser to view your VR gallery!"
