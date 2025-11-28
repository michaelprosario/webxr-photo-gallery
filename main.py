from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from photo_manager import PhotoArchiveManager
from image_processor import ImageProcessor
from scene_generator import AFrameSceneGenerator

app = FastAPI(title="Photo Archive API", version="1.0.0")

# Initialize managers
ARCHIVE_BASE_PATH = os.getenv("ARCHIVE_PATH", "./photo_archive")
SCENE_OUTPUT_PATH = os.getenv("SCENE_OUTPUT_PATH", "./sceneOutput")
photo_manager = PhotoArchiveManager(ARCHIVE_BASE_PATH)
image_processor = ImageProcessor()

# Initialize scene generator (lazy loading to handle missing API key gracefully)
scene_generator = None

def get_scene_generator():
    global scene_generator
    if scene_generator is None:
        scene_generator = AFrameSceneGenerator(SCENE_OUTPUT_PATH)
    return scene_generator


class ImportRequest(BaseModel):
    source_folder: str
    collection_name: str
    max_width: Optional[int] = 1920
    max_height: Optional[int] = 1080
    quality: Optional[int] = 85


class ImportResponse(BaseModel):
    collection_name: str
    imported_count: int
    failed_count: int
    collection_path: str
    details: List[dict]


class GenerateSceneRequest(BaseModel):
    collection_names: List[str]
    scene_name: Optional[str] = None


class GenerateSceneResponse(BaseModel):
    scene_name: str
    collections: List[str]
    photo_count: int
    created_at: str
    file_path: str
    assets_directory: str


@app.get("/")
async def root():
    """Welcome endpoint with API information"""
    return {
        "message": "Photo Archive API",
        "version": "1.0.0",
        "endpoints": {
            "/import": "Import photos from a folder",
            "/collections": "List all collections",
            "/collections/{name}": "Get collection details",
            "/scenes/generate": "Generate A-Frame VR gallery scene",
            "/scenes": "List all generated scenes",
            "/health": "Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/import", response_model=ImportResponse)
async def import_photos(request: ImportRequest):
    """
    Import photos from a specified folder into the archive.
    
    - **source_folder**: Path to the folder containing photos to import
    - **collection_name**: Name for this collection of photos
    - **max_width**: Maximum width for resized images (default: 1920)
    - **max_height**: Maximum height for resized images (default: 1080)
    - **quality**: JPEG quality for compressed images (default: 85)
    """
    # Validate source folder exists
    if not os.path.exists(request.source_folder):
        raise HTTPException(status_code=404, detail=f"Source folder not found: {request.source_folder}")
    
    if not os.path.isdir(request.source_folder):
        raise HTTPException(status_code=400, detail=f"Path is not a directory: {request.source_folder}")
    
    # Create collection
    collection_path = photo_manager.create_collection(request.collection_name)
    
    # Process and import photos
    results = []
    imported_count = 0
    failed_count = 0
    
    # Supported image formats
    supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}
    
    try:
        for filename in os.listdir(request.source_folder):
            file_path = os.path.join(request.source_folder, filename)
            
            # Skip directories
            if os.path.isdir(file_path):
                continue
            
            # Check if file is an image
            _, ext = os.path.splitext(filename.lower())
            if ext not in supported_formats:
                continue
            
            try:
                # Process and save image
                output_path = os.path.join(collection_path, filename)
                
                # Resize and optimize image
                success = image_processor.process_image(
                    input_path=file_path,
                    output_path=output_path,
                    max_width=request.max_width,
                    max_height=request.max_height,
                    quality=request.quality
                )
                
                if success:
                    imported_count += 1
                    file_size = os.path.getsize(output_path)
                    results.append({
                        "filename": filename,
                        "status": "success",
                        "size_bytes": file_size
                    })
                else:
                    failed_count += 1
                    results.append({
                        "filename": filename,
                        "status": "failed",
                        "error": "Processing failed"
                    })
                    
            except Exception as e:
                failed_count += 1
                results.append({
                    "filename": filename,
                    "status": "failed",
                    "error": str(e)
                })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during import: {str(e)}")
    
    return ImportResponse(
        collection_name=request.collection_name,
        imported_count=imported_count,
        failed_count=failed_count,
        collection_path=collection_path,
        details=results
    )


@app.get("/collections")
async def list_collections():
    """List all photo collections in the archive"""
    collections = photo_manager.list_collections()
    
    collection_details = []
    for collection_name in collections:
        info = photo_manager.get_collection_info(collection_name)
        collection_details.append(info)
    
    return {
        "total_collections": len(collections),
        "collections": collection_details
    }


@app.get("/collections/{collection_name}")
async def get_collection(collection_name: str):
    """Get details about a specific collection"""
    if not photo_manager.collection_exists(collection_name):
        raise HTTPException(status_code=404, detail=f"Collection not found: {collection_name}")
    
    info = photo_manager.get_collection_info(collection_name)
    return info


@app.delete("/collections/{collection_name}")
async def delete_collection(collection_name: str):
    """Delete a collection and all its photos"""
    if not photo_manager.collection_exists(collection_name):
        raise HTTPException(status_code=404, detail=f"Collection not found: {collection_name}")
    
    success = photo_manager.delete_collection(collection_name)
    
    if success:
        return {"message": f"Collection '{collection_name}' deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete collection")


@app.post("/scenes/generate", response_model=GenerateSceneResponse)
async def generate_scene(request: GenerateSceneRequest):
    """
    Generate an A-Frame VR art gallery scene for specified photo collections.
    
    Uses Google Gemini AI to create an immersive 3D gallery with Tuscan-inspired,
    airy 80s aesthetic featuring warm lighting and geometric artistic elements.
    
    - **collection_names**: List of collection names to include in the gallery
    - **scene_name**: Optional custom name for the scene (auto-generated if not provided)
    """
    # Validate collections exist
    for collection_name in request.collection_names:
        if not photo_manager.collection_exists(collection_name):
            raise HTTPException(
                status_code=404, 
                detail=f"Collection not found: {collection_name}"
            )
    
    try:
        generator = get_scene_generator()
        metadata = generator.generate_scene(
            collection_names=request.collection_names,
            photo_manager=photo_manager,
            scene_name=request.scene_name
        )
        
        return GenerateSceneResponse(**metadata)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error generating scene: {str(e)}"
        )


@app.get("/scenes")
async def list_scenes():
    """List all generated A-Frame VR gallery scenes"""
    try:
        generator = get_scene_generator()
        scenes = generator.list_scenes()
        
        return {
            "total_scenes": len(scenes),
            "scenes": scenes
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing scenes: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
