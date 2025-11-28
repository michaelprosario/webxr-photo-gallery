# A-Frame VR Gallery Generation - Quick Start Guide

## Prerequisites

1. **Set up your environment**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your Gemini API key
   # GEMINI_API_KEY=your-api-key-here
   ```
   
   Get your API key from: https://aistudio.google.com/app/apikey

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

> **Note:** The application automatically loads variables from `.env` on startup.

## Step-by-Step Usage

### 1. Start the API Server

```bash
python main.py
```

The server will start at `http://localhost:8000`

### 2. Import Photos (if you haven't already)

```bash
curl -X POST "http://localhost:8000/import" \
  -H "Content-Type: application/json" \
  -d '{
    "source_folder": "/workspaces/webxr-photo-gallery/FrancisRosarioAlbum",
    "collection_name": "Francis Art Collection"
  }'
```

### 3. Generate Your VR Gallery

**Basic Example:**
```bash
curl -X POST "http://localhost:8000/scenes/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "collection_names": ["Francis_Art_Collection"]
  }'
```

**Custom Scene Name:**
```bash
curl -X POST "http://localhost:8000/scenes/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "collection_names": ["Francis_Art_Collection"],
    "scene_name": "francis_tuscan_gallery"
  }'
```

**Multiple Collections:**
```bash
curl -X POST "http://localhost:8000/scenes/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "collection_names": ["Francis_Art_Collection", "Summer_2025", "Vacation_Photos"],
    "scene_name": "combined_gallery"
  }'
```

### 4. View Your Generated Gallery

The generated HTML file will be in the `sceneOutput` folder along with an assets directory containing all photos:

```
sceneOutput/
├── francis_tuscan_gallery.html
├── francis_tuscan_gallery_metadata.json
└── francis_tuscan_gallery_assets/
    └── Francis_Art_Collection/
        ├── photo1.jpg
        ├── photo2.jpg
        └── photo3.jpg
```

**To view:**

1. Start the web server:
   ```bash
   ./serve.sh
   ```

2. Open in browser: http://localhost:8080/sceneOutput/francis_tuscan_gallery.html

3. Use **WASD** keys to move around

4. Use **mouse** to look around

5. For VR mode: Access from a VR-capable device

**Note:** Each scene is self-contained with its own copy of photos in the `_assets` directory, making it easy to share or move galleries.

### 5. List All Generated Scenes

```bash
curl http://localhost:8000/scenes
```

## Gallery Features

Your AI-generated gallery will include:

- **Aesthetic Style**: Light, warm Tuscan summer vibes with peachy/golden tones
- **Layout**: Multiple rooms or areas for different collections
- **Lighting**: Warm ambient and point lighting for atmosphere
- **Decorations**: Geometric shapes (spheres, toruses, cones, pyramids)
- **Navigation**: WASD movement + mouse look controls
- **VR Support**: Compatible with VR headsets
- **Photos**: Displayed on gallery walls at eye level (1.6m height)

## Gallery Controls

- **W** - Move forward
- **A** - Move left
- **S** - Move backward
- **D** - Move right
- **Mouse** - Look around
- **VR Mode** - Automatically detected on VR devices

## API Response Example

```json
{
  "scene_name": "francis_tuscan_gallery",
  "collections": ["Francis_Art_Collection"],
  "photo_count": 25,
  "created_at": "2025-11-28T12:00:00",
  "file_path": "/workspaces/webxr-photo-gallery/sceneOutput/francis_tuscan_gallery.html"
}
```

## Troubleshooting

**Error: "GEMINI_API_KEY environment variable not set"**
- Solution: Add your API key to `.env` file: `GEMINI_API_KEY=your-key`
- Or set it manually: `export GEMINI_API_KEY="your-key"`
- Get your key from: https://aistudio.google.com/app/apikey

**Error: "Collection not found"**
- Solution: Check available collections: `curl http://localhost:8000/collections`
- Import collections first using the `/import` endpoint

**Gallery doesn't display photos**
- Check that the photo paths in the HTML are correct
- Ensure your web server can serve the photo files
- Check browser console for errors

**.env file not loading?**
- Ensure `.env` is in the project root directory
- Restart the server after editing `.env`
- Check file permissions (should be readable)

## Advanced: Serving with a Web Server

For proper viewing and performance:

**Option 1: Use the included script (recommended)**
```bash
./serve.sh        # Default port 8080
./serve.sh 3000   # Custom port
```

**Option 2: Python's built-in server**
```bash
cd /workspaces/webxr-photo-gallery
python -m http.server 8080
# Then open: http://localhost:8080/sceneOutput/your_gallery.html
```

**Option 3: Node.js http-server (if installed)**
```bash
npx http-server -p 8080
```

**Why use a web server?**
- HTML files loaded directly (`file://`) may have CORS restrictions
- A web server properly serves images and assets
- Better performance and loading behavior
- Required for some A-Frame features

## Example Full Workflow

```bash
# 1. Set up environment
cp .env.example .env
# Edit .env and add: GEMINI_API_KEY=your-api-key-here

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start server
python main.py

# 4. Import photos (in another terminal)
curl -X POST "http://localhost:8000/import" \
  -H "Content-Type: application/json" \
  -d '{
    "source_folder": "/path/to/photos",
    "collection_name": "My Collection"
  }'

# 5. Generate VR gallery
curl -X POST "http://localhost:8000/scenes/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "collection_names": ["My_Collection"],
    "scene_name": "my_vr_gallery"
  }'

# 6. Open the generated file
# Navigate to: sceneOutput/my_vr_gallery.html in your browser
```

## Tips for Best Results

1. **Photo Quality**: Import high-quality photos for best VR experience
2. **Collection Size**: 10-30 photos per gallery works well
3. **Multiple Collections**: Combine related collections for themed galleries
4. **Scene Names**: Use descriptive names for easy organization
5. **Browser**: Use modern browsers (Chrome, Firefox, Edge) for best A-Frame support
6. **VR Testing**: Test on actual VR devices for immersive experience

## Next Steps

- Explore the interactive API docs: http://localhost:8000/docs
- Customize generated scenes by editing the HTML files
- Share your VR galleries by hosting the HTML files online
- Create multiple themed galleries for different occasions
