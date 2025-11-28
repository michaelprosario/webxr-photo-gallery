# Photo Archive API

A FastAPI-based REST API for importing, managing, and optimizing photos for web applications. The API automatically resizes images to web-friendly dimensions while maintaining aspect ratios and organizing them into collections.

## Features

- 📸 **Import photos** from any folder on your system
- 🗂️ **Organize photos** into named collections
- 📏 **Automatic image resizing** to web-optimized dimensions
- 🗜️ **Image compression** with configurable quality settings
- 💾 **File system storage** - simple, reliable, no database required
- 🚀 **Fast and efficient** using FastAPI
- 📊 **Collection management** - list, view details, and delete collections
- 🔍 **Metadata tracking** for each collection

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

## Configuration

The photo archive is stored in the `photo_archive` directory by default. You can change this by setting the `ARCHIVE_PATH` environment variable:

```bash
export ARCHIVE_PATH="/path/to/your/archive"
```

export ARCHIVE_PATH="/workspaces/webxr-photo-gallery/my_archive"

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

## Directory Structure

```
webxr-photo-gallery/
├── main.py                 # FastAPI application and endpoints
├── photo_manager.py        # Photo archive management logic
├── image_processor.py      # Image resizing and optimization
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── photo_archive/         # Photo storage (created automatically)
    ├── Collection_1/
    │   ├── .metadata.json
    │   ├── photo1.jpg
    │   └── photo2.jpg
    └── Collection_2/
        ├── .metadata.json
        └── photo3.jpg
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

1. **Start the server:**
   ```bash
   python main.py
   ```

2. **Import your first collection:**
   ```bash
   curl -X POST "http://localhost:8000/import" \
     -H "Content-Type: application/json" \
     -d '{
       "source_folder": "/workspaces/webxr-photo-gallery/FrancisRosarioAlbum",
       "collection_name": "Francis Rosario Album"
     }'
   ```

3. **List your collections:**
   ```bash
   curl http://localhost:8000/collections
   ```

4. **View collection details:**
   ```bash
   curl http://localhost:8000/collections/Francis_Rosario_Album
   ```

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