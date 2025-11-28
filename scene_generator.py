import os
import json
import shutil
from typing import List, Dict, Optional
import google.generativeai as genai
from datetime import datetime


class AFrameSceneGenerator:
    """
    Generates A-Frame VR gallery scenes using Google Gemini AI.
    Creates immersive 3D art gallery experiences for photo collections.
    """
    
    def __init__(self, output_base_path: str = "./sceneOutput"):
        """
        Initialize the scene generator.
        
        Args:
            output_base_path: Base directory for storing generated scenes
        """
        self.output_base_path = output_base_path
        self._ensure_output_directory()
        
        # Configure Gemini API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def _ensure_output_directory(self):
        """Ensure the scene output directory exists"""
        os.makedirs(self.output_base_path, exist_ok=True)
    
    def generate_scene(
        self, 
        collection_names: List[str],
        photo_manager,
        scene_name: Optional[str] = None
    ) -> Dict:
        """
        Generate an A-Frame art gallery scene for the specified collections.
        
        Args:
            collection_names: List of collection names to include in the scene
            photo_manager: PhotoArchiveManager instance to access collections
            scene_name: Optional name for the scene (auto-generated if not provided)
        
        Returns:
            Dictionary with scene information including file path
        """
        # Validate collections exist
        collections_data = []
        for collection_name in collection_names:
            if not photo_manager.collection_exists(collection_name):
                raise ValueError(f"Collection not found: {collection_name}")
            
            collection_info = photo_manager.get_collection_info(collection_name)
            collections_data.append(collection_info)
        
        # Create scene name if not provided
        if not scene_name:
            scene_name = f"gallery_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create scene-specific directory for assets
        scene_assets_dir = os.path.join(self.output_base_path, f"{scene_name}_assets")
        os.makedirs(scene_assets_dir, exist_ok=True)
        
        # Copy photos to scene assets directory and build photo list with new paths
        all_photos = []
        for collection_info in collections_data:
            collection_folder_name = collection_info['folder_name']
            
            # Create collection subdirectory in assets
            collection_assets_dir = os.path.join(scene_assets_dir, collection_folder_name)
            os.makedirs(collection_assets_dir, exist_ok=True)
            
            for photo in collection_info.get('photos', []):
                source_path = os.path.join(collection_info['path'], photo['filename'])
                dest_path = os.path.join(collection_assets_dir, photo['filename'])
                
                # Copy the photo file
                shutil.copy2(source_path, dest_path)
                
                # Store relative path from HTML file location
                relative_path = os.path.join(f"{scene_name}_assets", collection_folder_name, photo['filename'])
                
                all_photos.append({
                    'collection': collection_info['collection_name'],
                    'filename': photo['filename'],
                    'path': relative_path  # Use relative path for HTML
                })
        
        # Generate scene using Gemini
        scene_html = self._generate_with_gemini(collections_data, all_photos, scene_name)
        
        # Save scene to file
        scene_filename = f"{scene_name}.html"
        scene_path = os.path.join(self.output_base_path, scene_filename)
        
        with open(scene_path, 'w', encoding='utf-8') as f:
            f.write(scene_html)
        
        # Save metadata
        metadata = {
            'scene_name': scene_name,
            'collections': collection_names,
            'photo_count': len(all_photos),
            'created_at': datetime.now().isoformat(),
            'file_path': scene_path,
            'assets_directory': scene_assets_dir
        }
        
        metadata_path = os.path.join(self.output_base_path, f"{scene_name}_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return metadata
    
    def _generate_with_gemini(self, collections_data: List[Dict], all_photos: List[Dict], scene_name: str) -> str:
        """
        Use Gemini AI to generate the A-Frame scene HTML.
        
        Args:
            collections_data: List of collection information dictionaries
            all_photos: List of all photos with relative paths
            scene_name: Name of the scene
        
        Returns:
            Generated HTML content
        """
        # Prepare photo information for the prompt
        photo_list = []
        for idx, photo in enumerate(all_photos):
            photo_list.append(f"{idx}: {photo['collection']} - {photo['path']}")
        
        collection_names = [c['collection_name'] for c in collections_data]
        
        prompt = f"""Create a complete A-Frame HTML page for an immersive VR art gallery.

REQUIREMENTS:
1. The gallery should display {len(all_photos)} photos from these collections: {', '.join(collection_names)}
2. Art style inspiration: Light, warm summer Tuscan aesthetic. Airy, 80s vibe.
3. Use warm, soft lighting with peachy/golden tones
4. Include geometric shapes (spheres, toruses, cones, pyramids) as artistic elements throughout the space
5. Create multiple rooms or areas, one for each collection if possible
6. Use textured walls (consider stucco, marble, or painted textures)
7. Add ambient particle effects or subtle animations for atmosphere
8. Position the camera at a comfortable standing height (1.6m)
9. Include WASD movement controls and look-around with mouse/VR headset

PHOTO PATHS (use these exact paths in your src attributes):
{chr(10).join(photo_list[:20])}  
{"... and " + str(len(all_photos) - 20) + " more photos" if len(all_photos) > 20 else ""}

TECHNICAL REQUIREMENTS:
- Complete, valid HTML5 document
- Include A-Frame CDN (latest version)
- Use <a-image> entities for photos with proper positioning
- Photos should be arranged on walls at eye level (1.6m height)
- Space photos 2-3 meters apart
- Use <a-sky> for background with warm gradient color
- Add <a-plane> for floor with subtle texture
- Include geometric decorative elements positioned throughout
- Use <a-light> entities for warm ambient and point lighting
- Add smooth movement controls
- Include some 80s geometric patterns or shapes as decoration
- Make the gallery feel spacious and airy

Generate ONLY the complete HTML code, no explanations or markdown formatting."""

        try:
            response = self.model.generate_content(prompt)
            html_content = response.text
            
            # Clean up markdown code blocks if Gemini includes them
            if '```html' in html_content:
                html_content = html_content.split('```html')[1].split('```')[0].strip()
            elif '```' in html_content:
                html_content = html_content.split('```')[1].split('```')[0].strip()
            
            return html_content
            
        except Exception as e:
            # Fallback to basic template if Gemini fails
            return self._generate_fallback_scene(collections_data, all_photos)
    
    def _generate_fallback_scene(self, collections_data: List[Dict], all_photos: List[Dict]) -> str:
        """
        Generate a basic fallback A-Frame scene if Gemini is unavailable.
        
        Args:
            collections_data: List of collection information
            all_photos: List of all photos
        
        Returns:
            Basic HTML scene
        """
        # Generate photo entities
        photo_entities = []
        x_position = -10
        y_position = 1.6
        z_position = -5
        
        for idx, photo in enumerate(all_photos):
            photo_entities.append(f'''
      <a-image 
        src="{photo['path']}" 
        width="2" 
        height="1.5" 
        position="{x_position} {y_position} {z_position}">
      </a-image>''')
            
            x_position += 3
            if (idx + 1) % 5 == 0:
                x_position = -10
                z_position -= 4
        
        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Photo Gallery VR</title>
    <meta name="description" content="Immersive Photo Gallery">
    <script src="https://aframe.io/releases/1.5.0/aframe.min.js"></script>
</head>
<body>
    <a-scene>
        <!-- Sky with warm gradient -->
        <a-sky color="#FFE5CC"></a-sky>
        
        <!-- Lighting -->
        <a-light type="ambient" color="#FFD9B3" intensity="0.8"></a-light>
        <a-light type="point" position="0 5 0" color="#FFB380" intensity="0.6"></a-light>
        
        <!-- Floor -->
        <a-plane position="0 0 0" rotation="-90 0 0" width="40" height="40" color="#F5DEB3"></a-plane>
        
        <!-- Photos -->
        {"".join(photo_entities)}
        
        <!-- Decorative geometric elements -->
        <a-sphere position="5 2 -3" radius="0.3" color="#FFB380" opacity="0.7"></a-sphere>
        <a-torus position="-5 2.5 -6" radius="0.5" radius-tubular="0.1" color="#FFC9A3"></a-torus>
        <a-cone position="8 0 -8" radius-bottom="0.5" radius-top="0" height="2" color="#FFD4AD"></a-cone>
        
        <!-- Camera with movement controls -->
        <a-entity id="rig" position="0 1.6 5">
            <a-camera wasd-controls look-controls></a-camera>
        </a-entity>
    </a-scene>
</body>
</html>'''
        
        return html
    
    def list_scenes(self) -> List[Dict]:
        """
        List all generated scenes.
        
        Returns:
            List of scene metadata dictionaries
        """
        scenes = []
        
        if not os.path.exists(self.output_base_path):
            return scenes
        
        for filename in os.listdir(self.output_base_path):
            if filename.endswith('_metadata.json'):
                metadata_path = os.path.join(self.output_base_path, filename)
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                    scenes.append(metadata)
        
        return sorted(scenes, key=lambda x: x.get('created_at', ''), reverse=True)
