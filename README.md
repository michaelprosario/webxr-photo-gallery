# Photo Archive API

A FastAPI-based REST API for importing, managing, and optimizing photos for web applications. The API automatically resizes images to web-friendly dimensions while maintaining aspect ratios and organizing them into collections. **Now with AI-powered A-Frame VR gallery generation!**

## Features

- 📸 **Import photos** from any folder on your system
- 🗂️ **Organize photos** into named collections
- 📏 **Automatic image resizing** to web-optimized dimensions
- 🗜️ **Image compression** with configurable quality settings
- 💾 **File system storage** - simple, reliable, no database required
- 🚀 **Fast and efficient** using FastAPI
- 📊 **Collection management** - list, view details, and delete collections
- 🔍 **Metadata tracking** for each collection
- 🎨 **AI-Powered VR Gallery Generation** - Create immersive A-Frame art galleries using Google Gemini
- 🌅 **Customizable aesthetics** - Tuscan-inspired, airy 80s vibe with warm lighting

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download

If you have this code, navigate to the project directory:

```bash
cd /path/to/webxr-photo-gallery
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- FastAPI and Uvicorn (web framework)
- Pillow (image processing)
- Google Generative AI (Gemini for VR gallery generation)
- Pydantic (data validation)
- python-dotenv (environment variable management)

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Then edit `.env` and add your configuration:

```bash
# Required for VR gallery generation
GEMINI_API_KEY=your-actual-api-key-here

# Optional: customize paths
ARCHIVE_PATH=/workspaces/webxr-photo-gallery/my_archive
SCENE_OUTPUT_PATH=/workspaces/webxr-photo-gallery/sceneOutput
```

**Get your Gemini API key:** https://aistudio.google.com/app/apikey

> **Note:** The `.env` file is automatically loaded when the application starts. You don't need to export variables manually.

**Verify your setup:**
```bash
python check_env.py
```
This script verifies that your `.env` file is properly configured and all dependencies are installed.

## Configuration

### Environment Variables (Recommended Method)

The application automatically loads configuration from a `.env` file in the project root.

**Setup:**
1. Copy the example file: `cp .env.example .env`
2. Edit `.env` with your values

**Available variables:**

```bash
# Photo archive storage path (optional)
ARCHIVE_PATH=/path/to/your/archive

# VR scene output path (optional)
SCENE_OUTPUT_PATH=/path/to/sceneOutput

# Google Gemini API Key (required for VR gallery generation)
GEMINI_API_KEY=your-api-key-here
```

### Alternative: Manual Environment Variables

You can also set environment variables manually (without `.env` file):

**Photo Archive Configuration:**

The photo archive is stored in the `photo_archive` directory by default. You can change this by setting the `ARCHIVE_PATH` environment variable:

```bash
export ARCHIVE_PATH="/path/to/your/archive"
```

Example:
```bash
export ARCHIVE_PATH="/workspaces/webxr-photo-gallery/my_archive"
```

**Google Gemini API Configuration (Required for VR Gallery Generation):**

To use the A-Frame scene generation feature, you need a Google Gemini API key:

1. Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Set the environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

**Note:** Using the `.env` file is recommended as variables persist across sessions.

## Usage

### Starting the Server

```bash
# Start the API server
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

### API Documentation

Once the server is running, you can access:

- **Interactive API docs (Swagger)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### 1. Import Photos

Import photos from a folder into your archive.

**Endpoint:** `POST /import`

**Request Body:**
```json
{
  "source_folder": "/path/to/your/photos",
  "collection_name": "My Vacation Photos",
  "max_width": 1920,
  "max_height": 1080,
  "quality": 85
}
```

**Parameters:**
- `source_folder` (required): Absolute path to folder containing photos
- `collection_name` (required): Name for this collection
- `max_width` (optional): Maximum width in pixels (default: 1920)
- `max_height` (optional): Maximum height in pixels (default: 1080)
- `quality` (optional): JPEG quality 1-100 (default: 85)

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/import" \
  -H "Content-Type: application/json" \
  -d '{
    "source_folder": "/home/user/Pictures/vacation",
    "collection_name": "Summer 2025",
    "max_width": 1920,
    "max_height": 1080,
    "quality": 85
  }'
```

**Response:**
```json
{
  "collection_name": "Summer 2025",
  "imported_count": 45,
  "failed_count": 0,
  "collection_path": "/path/to/photo_archive/Summer_2025",
  "details": [
    {
      "filename": "IMG_001.jpg",
      "status": "success",
      "size_bytes": 245678
    }
  ]
}
```

### 2. List All Collections

Get a list of all photo collections.

**Endpoint:** `GET /collections`

**Example:**
```bash
curl http://localhost:8000/collections
```

**Response:**
```json
{
  "total_collections": 3,
  "collections": [
    {
      "collection_name": "Summer 2025",
      "folder_name": "Summer_2025",
      "path": "/path/to/photo_archive/Summer_2025",
      "photo_count": 45,
      "total_size_bytes": 12456789,
      "created_at": "2025-11-28T10:30:00",
      "updated_at": "2025-11-28T10:35:00"
    }
  ]
}
```

### 3. Get Collection Details

Get detailed information about a specific collection.

**Endpoint:** `GET /collections/{collection_name}`

**Example:**
```bash
curl http://localhost:8000/collections/Summer_2025
```

### 4. Delete a Collection

Delete a collection and all its photos.

**Endpoint:** `DELETE /collections/{collection_name}`

**Example:**
```bash
curl -X DELETE http://localhost:8000/collections/Summer_2025
```

### 5. Health Check

Check if the API is running.

**Endpoint:** `GET /health`

**Example:**
```bash
curl http://localhost:8000/health
```

### 6. Generate A-Frame VR Gallery Scene

Generate an immersive VR art gallery using Google Gemini AI for your photo collections.

**Endpoint:** `POST /scenes/generate`

**Request Body:**
```json
{
  "collection_names": ["Summer 2025", "Francis Rosario Album"],
  "scene_name": "my_tuscan_gallery"
}
```

**Parameters:**
- `collection_names` (required): Array of collection names to include in the gallery
- `scene_name` (optional): Custom name for the scene (auto-generated if not provided)

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/scenes/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "collection_names": ["Francis_Rosario_Album"],
    "scene_name": "francis_vr_gallery"
  }'
```

**Response:**
```json
{
  "scene_name": "francis_vr_gallery",
  "collections": ["Francis_Rosario_Album"],
  "photo_count": 25,
  "created_at": "2025-11-28T12:00:00",
  "file_path": "/path/to/sceneOutput/francis_vr_gallery.html",
  "assets_directory": "/path/to/sceneOutput/francis_vr_gallery_assets"
}
```

**Using the Generated Scene:**
1. Start a web server to view the gallery:
   ```bash
   ./serve.sh
   ```
2. Open http://localhost:8080/sceneOutput/francis_vr_gallery.html in your browser
3. Use WASD keys to move around the gallery
4. Use mouse to look around
5. For VR experience, open on a VR-capable device

**Note:** Each generated scene creates its own assets directory with copies of all photos, making the gallery self-contained and portable.

### 7. List Generated Scenes

Get a list of all generated VR gallery scenes.

**Endpoint:** `GET /scenes`

**Example:**
```bash
curl http://localhost:8000/scenes
```

**Response:**
```json
{
  "total_scenes": 2,
  "scenes": [
    {
      "scene_name": "francis_vr_gallery",
      "collections": ["Francis_Rosario_Album"],
      "photo_count": 25,
      "created_at": "2025-11-28T12:00:00",
      "file_path": "/path/to/sceneOutput/francis_vr_gallery.html",
      "assets_directory": "/path/to/sceneOutput/francis_vr_gallery_assets"
    }
  ]
}
```

### 8. View Generated Galleries

Start a simple web server to view your VR galleries:

**Endpoint:** `./serve.sh`

**Example:**
```bash
# Start web server on default port 8080
./serve.sh

# Or specify a custom port
./serve.sh 3000
```

Then open in browser: http://localhost:8080/sceneOutput/your_gallery.html

## Directory Structure

```
webxr-photo-gallery/
├── main.py                 # FastAPI application and endpoints
├── photo_manager.py        # Photo archive management logic
├── image_processor.py      # Image resizing and optimization
├── scene_generator.py      # A-Frame VR gallery generation with Gemini AI
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── serve.sh               # Simple web server for viewing galleries
├── photo_archive/         # Photo storage (created automatically)
│   ├── Collection_1/
│   │   ├── .metadata.json
│   │   ├── photo1.jpg
│   │   └── photo2.jpg
│   └── Collection_2/
│       ├── .metadata.json
│       └── photo3.jpg
└── sceneOutput/           # Generated A-Frame VR scenes
    ├── gallery_001.html
    ├── gallery_001_metadata.json
    ├── gallery_001_assets/    # Photos copied for this scene
    │   └── Collection_1/
    │       ├── photo1.jpg
    │       └── photo2.jpg
    └── my_tuscan_gallery.html
```

## How It Works

1. **Import Process:**
   - You specify a source folder containing photos
   - The API scans for supported image formats (JPG, PNG, GIF, BMP, WEBP, TIFF)
   - Each image is resized to fit within the specified dimensions while maintaining aspect ratio
   - Images are compressed with the specified quality setting
   - Processed images are saved to the collection folder

2. **Storage:**
   - Photos are organized into collections (folders)
   - Each collection has a metadata file with creation/update timestamps
   - Collections are stored in the `photo_archive` directory

3. **Optimization:**
   - Images larger than max dimensions are resized down
   - Images smaller than max dimensions are kept at original size
   - RGBA/transparent images are converted to RGB with white background
   - JPEG optimization is applied to reduce file size

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
- WebP (.webp)
- TIFF (.tiff)

## Example Workflow

### Basic Photo Import Workflow

1. **Configure your environment:**
   ```bash
   # Copy and edit .env file
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

2. **Start the server:**
   ```bash
   python main.py
   ```

3. **Import your first collection:**
   ```bash
   curl -X POST "http://localhost:8000/import" \
     -H "Content-Type: application/json" \
     -d '{
       "source_folder": "/workspaces/webxr-photo-gallery/FrancisRosarioAlbum",
       "collection_name": "Francis Rosario Album"
     }'
   ```

4. **List your collections:**
   ```bash
   curl http://localhost:8000/collections
   ```

5. **View collection details:**
   ```bash
   curl http://localhost:8000/collections/Francis_Rosario_Album
   ```

### VR Gallery Generation Workflow

1. **Generate a VR gallery for your collection:**
   ```bash
   curl -X POST "http://localhost:8000/scenes/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "collection_names": ["Francis_Rosario_Album"],
       "scene_name": "my_art_gallery"
     }'
   ```

2. **Start web server and view the gallery:**
   ```bash
   # In a new terminal
   ./serve.sh
   ```
   
3. **Open in browser:**
   - Navigate to http://localhost:8080/sceneOutput/my_art_gallery.html
   - Use WASD to move, mouse to look around
   - Experience your photos in an immersive VR gallery!

4. **List all your generated galleries:**
   ```bash
   curl http://localhost:8000/scenes
   ```

### Gallery Features
The AI-generated A-Frame galleries include:
- 🌅 Warm, Tuscan-inspired lighting with peachy/golden tones
- 🎨 Geometric decorative elements (spheres, toruses, cones, pyramids)
- 🏛️ Multiple rooms or areas for different collections
- 🎮 WASD movement controls and mouse look-around
- 🥽 VR headset support
- ✨ Atmospheric effects and subtle animations
- 🖼️ Photos displayed on gallery walls at eye level

## Troubleshooting

### Common Issues

**Issue: "Source folder not found"**
- Ensure the path in `source_folder` exists and is accessible
- Use absolute paths (e.g., `/home/user/Pictures` not `~/Pictures`)

**Issue: "Permission denied"**
- Check that the application has read permissions for source folder
- Check that the application has write permissions for archive directory

**Issue: "No images imported"**
- Verify the source folder contains supported image formats
- Check that files have proper extensions (.jpg, .png, etc.)

## Development

To run in development mode with auto-reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## License

This project is provided as-is for educational and personal use.

## Support

For issues or questions, please refer to the API documentation at http://localhost:8000/docs when the server is running.