# System Architecture - WebXR Photo Gallery

## Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        FastAPI Server                        │
│                         (main.py)                            │
└─────────────────┬───────────────────────┬───────────────────┘
                  │                       │
                  ▼                       ▼
    ┌─────────────────────┐   ┌──────────────────────┐
    │  Photo Management   │   │  Scene Generation    │
    │ (photo_manager.py)  │   │ (scene_generator.py) │
    └──────────┬──────────┘   └──────────┬───────────┘
               │                          │
               ▼                          ▼
    ┌──────────────────┐      ┌──────────────────────┐
    │ Image Processing │      │  Google Gemini API   │
    │(image_processor.py)     │  (AI Generation)     │
    └──────────────────┘      └──────────────────────┘
               │                          │
               ▼                          ▼
    ┌──────────────────┐      ┌──────────────────────┐
    │  photo_archive/  │      │    sceneOutput/      │
    │   Collections    │      │    VR Galleries      │
    └──────────────────┘      └──────────────────────┘
```

## API Flow - Photo Import

```
User
  │
  │ POST /import
  │ {source_folder, collection_name}
  ▼
FastAPI Endpoint
  │
  │ validate folder exists
  ▼
PhotoArchiveManager
  │
  │ create collection folder
  ▼
For each image:
  │
  │ ImageProcessor.process_image()
  │   │
  │   ├─ Resize to max dimensions
  │   ├─ Convert to RGB if needed
  │   └─ Optimize JPEG quality
  ▼
Save to collection folder
  │
  │ create/update metadata
  ▼
Return ImportResponse
  │
  ▼
User receives result
```

## API Flow - VR Gallery Generation

```
User
  │
  │ POST /scenes/generate
  │ {collection_names, scene_name}
  ▼
FastAPI Endpoint
  │
  │ validate collections exist
  ▼
AFrameSceneGenerator
  │
  │ gather photo information
  │ from PhotoArchiveManager
  ▼
Build Gemini Prompt
  │
  ├─ Collection names
  ├─ Photo paths & counts
  ├─ Aesthetic requirements:
  │   └─ "Tuscan summer, airy 80s"
  │       "warm lighting, geometric shapes"
  ▼
Google Gemini API
  │
  │ AI generates A-Frame HTML
  │ with custom gallery layout
  ▼
Post-process HTML
  │
  │ clean markdown formatting
  │ validate structure
  ▼
Save to sceneOutput/
  │
  ├─ scene_name.html
  └─ scene_name_metadata.json
  ▼
Return GenerateSceneResponse
  │
  ▼
User receives file path
  │
  ▼
User opens HTML in browser
  │
  ▼
Immersive VR Gallery Experience!
```

## Data Models

### ImportRequest
```python
{
  "source_folder": str,      # Path to photos
  "collection_name": str,    # Collection name
  "max_width": int = 1920,   # Optional
  "max_height": int = 1080,  # Optional
  "quality": int = 85        # Optional
}
```

### GenerateSceneRequest
```python
{
  "collection_names": List[str],  # Collections to include
  "scene_name": str = None        # Optional custom name
}
```

### Collection Metadata
```json
{
  "name": "Collection Name",
  "created_at": "2025-11-28T10:00:00",
  "updated_at": "2025-11-28T10:00:00"
}
```

### Scene Metadata
```json
{
  "scene_name": "my_gallery",
  "collections": ["Collection1", "Collection2"],
  "photo_count": 50,
  "created_at": "2025-11-28T12:00:00",
  "file_path": "/path/to/sceneOutput/my_gallery.html"
}
```

## Directory Structure

```
webxr-photo-gallery/
│
├── API Layer
│   └── main.py                  # FastAPI endpoints
│
├── Business Logic
│   ├── photo_manager.py         # Collection management
│   ├── image_processor.py       # Image optimization
│   └── scene_generator.py       # VR gallery generation
│
├── Configuration
│   ├── requirements.txt         # Python dependencies
│   └── .env.example            # Environment variables
│
├── Documentation
│   ├── README.md               # Main documentation
│   ├── AFRAME_GUIDE.md         # VR gallery guide
│   └── IMPLEMENTATION_SUMMARY.md  # Implementation details
│
├── Testing
│   └── test_scene_api.sh       # API test script
│
└── Data Storage
    ├── photo_archive/          # Photo collections
    │   └── Collection_Name/
    │       ├── .metadata.json
    │       ├── photo1.jpg
    │       └── photo2.jpg
    │
    └── sceneOutput/            # Generated VR galleries
        ├── gallery_001.html
        └── gallery_001_metadata.json
```

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### Image Processing
- **Pillow** - Python Imaging Library
- Supports: JPEG, PNG, GIF, BMP, WebP, TIFF

### AI Integration
- **Google Gemini 1.5 Flash** - AI scene generation
- **google-generativeai** - Python SDK

### VR Framework
- **A-Frame** - WebVR framework
- HTML5 + WebGL
- VR headset compatible

## Key Features by Component

### PhotoArchiveManager
- Create collections
- List collections
- Get collection info
- Delete collections
- Metadata management
- File system organization

### ImageProcessor
- Resize images
- Maintain aspect ratios
- Optimize JPEG quality
- Convert color modes
- Handle multiple formats

### AFrameSceneGenerator
- AI-powered scene generation
- Gemini prompt engineering
- Fallback template
- Metadata tracking
- Multi-collection support
- Custom aesthetic themes

## Security Considerations

- API key stored in environment variables
- Path validation for file operations
- Sanitized collection names
- Error handling for invalid inputs
- No direct file system exposure

## Performance Characteristics

### Photo Import
- Processing time: ~100-500ms per image
- Depends on: original size, output quality
- Batch processing supported

### Scene Generation
- Generation time: ~5-30 seconds
- Depends on: Gemini API latency, photo count
- One-time generation, reusable HTML

## Scalability Notes

### Current Implementation
- File system storage (simple, reliable)
- Synchronous processing
- Single server deployment

### Future Scaling Options
- Add database for metadata
- Queue system for batch processing
- CDN for photo serving
- Caching for generated scenes
- Load balancer for multiple instances
