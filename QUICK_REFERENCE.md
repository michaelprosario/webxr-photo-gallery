# 🎨 A-Frame VR Gallery - Quick Reference

## Setup (One-time)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 3. Start server
python main.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/import` | Import photos from folder |
| `GET` | `/collections` | List all collections |
| `GET` | `/collections/{name}` | Get collection details |
| `DELETE` | `/collections/{name}` | Delete collection |
| `POST` | `/scenes/generate` | **Generate VR gallery** |
| `GET` | `/scenes` | List generated galleries |
| `GET` | `/health` | Health check |

## Quick Commands

### Import Photos
```bash
curl -X POST "http://localhost:8000/import" \
  -H "Content-Type: application/json" \
  -d '{
    "source_folder": "/path/to/photos",
    "collection_name": "My Collection"
  }'
```

### Generate VR Gallery
```bash
curl -X POST "http://localhost:8000/scenes/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "collection_names": ["My_Collection"],
    "scene_name": "my_vr_gallery"
  }'
```

### List Collections
```bash
curl http://localhost:8000/collections
```

### List Scenes
```bash
curl http://localhost:8000/scenes
```

## VR Gallery Controls

| Key/Action | Function |
|------------|----------|
| `W` | Move forward |
| `A` | Move left |
| `S` | Move backward |
| `D` | Move right |
| `Mouse` | Look around |
| `VR Headset` | Full VR experience |

## Gallery Features

- ✨ AI-generated layouts using Google Gemini
- 🌅 Warm Tuscan summer aesthetic
- 🎨 Geometric decorative elements
- 🏛️ Multiple rooms for different collections
- 💡 Warm peachy/golden lighting
- 🎮 WASD + Mouse controls
- 🥽 VR headset compatible

## File Locations

```
photo_archive/          # Your photo collections
sceneOutput/           # Generated VR galleries (HTML files)
```

## Environment Variables

**Using .env file (recommended):**
```bash
cp .env.example .env
# Edit .env with your values
```

**Variables:**
```bash
GEMINI_API_KEY         # Required for VR generation
ARCHIVE_PATH           # Optional: photo storage path
SCENE_OUTPUT_PATH      # Optional: scene output path
```

**Manual export (alternative):**
```bash
export GEMINI_API_KEY="your-key"
```

## Example Scripts

```bash
# Python example (full workflow)
python example_usage.py

# Bash test script
./test_scene_api.sh
```

## Interactive Docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Can't connect to API | Run `python main.py` |
| Missing GEMINI_API_KEY | Add to `.env` file or `export GEMINI_API_KEY="key"` |
| Collection not found | Use `GET /collections` to list |
| Scene won't load | Check browser console for errors |
| .env not loading | Restart server after editing `.env` |

## Gallery Aesthetic

**Theme:** Light, warm summer Tuscan + Airy 80s

**Colors:**
- Peachy/golden tones
- Warm ambient lighting
- Soft, inviting atmosphere

**Elements:**
- Spheres, toruses, cones, pyramids
- Textured walls and floors
- Spacious, open layout
- Photos at eye level (1.6m)

## Get API Key

🔑 https://aistudio.google.com/app/apikey

## Documentation

- `README.md` - Full documentation
- `AFRAME_GUIDE.md` - Detailed VR gallery guide
- `ARCHITECTURE.md` - System architecture
- `IMPLEMENTATION_SUMMARY.md` - Implementation details

## Support

- API Docs: http://localhost:8000/docs
- GitHub Issues: (your repo)
- Interactive testing: http://localhost:8000/docs

---

**Made with:** FastAPI + Google Gemini + A-Frame + Python 🐍
