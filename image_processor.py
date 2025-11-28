from PIL import Image
import os
from typing import Tuple, Optional


class ImageProcessor:
    """
    Handles image processing operations including resizing and optimization
    """
    
    def __init__(self):
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}
    
    def process_image(
        self,
        input_path: str,
        output_path: str,
        max_width: int = 1920,
        max_height: int = 1080,
        quality: int = 85
    ) -> bool:
        """
        Process an image by resizing it to fit within max dimensions while maintaining aspect ratio
        and optimizing it for web use.
        
        Args:
            input_path: Path to the source image
            output_path: Path where processed image will be saved
            max_width: Maximum width in pixels
            max_height: Maximum height in pixels
            quality: JPEG quality (1-100)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Open the image
            with Image.open(input_path) as img:
                # Convert RGBA to RGB if saving as JPEG
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Create a white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Calculate new dimensions
                new_width, new_height = self._calculate_resize_dimensions(
                    img.width, img.height, max_width, max_height
                )
                
                # Only resize if necessary
                if new_width < img.width or new_height < img.height:
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Ensure output directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Determine output format
                _, ext = os.path.splitext(output_path.lower())
                
                # Save with optimization
                if ext in ['.jpg', '.jpeg']:
                    img.save(output_path, 'JPEG', quality=quality, optimize=True)
                elif ext == '.png':
                    img.save(output_path, 'PNG', optimize=True)
                elif ext == '.webp':
                    img.save(output_path, 'WEBP', quality=quality, method=6)
                else:
                    # Default to JPEG for other formats
                    output_path = os.path.splitext(output_path)[0] + '.jpg'
                    img.save(output_path, 'JPEG', quality=quality, optimize=True)
                
                return True
                
        except Exception as e:
            print(f"Error processing image {input_path}: {str(e)}")
            return False
    
    def _calculate_resize_dimensions(
        self,
        original_width: int,
        original_height: int,
        max_width: int,
        max_height: int
    ) -> Tuple[int, int]:
        """
        Calculate new dimensions that fit within max bounds while maintaining aspect ratio.
        
        Args:
            original_width: Original image width
            original_height: Original image height
            max_width: Maximum allowed width
            max_height: Maximum allowed height
        
        Returns:
            Tuple of (new_width, new_height)
        """
        # If image is already smaller than max dimensions, keep original size
        if original_width <= max_width and original_height <= max_height:
            return original_width, original_height
        
        # Calculate aspect ratio
        aspect_ratio = original_width / original_height
        
        # Calculate dimensions based on width constraint
        new_width = max_width
        new_height = int(new_width / aspect_ratio)
        
        # If height exceeds max, recalculate based on height constraint
        if new_height > max_height:
            new_height = max_height
            new_width = int(new_height * aspect_ratio)
        
        return new_width, new_height
    
    def get_image_info(self, image_path: str) -> Optional[dict]:
        """
        Get information about an image file.
        
        Args:
            image_path: Path to the image
        
        Returns:
            Dictionary with image info or None if error
        """
        try:
            with Image.open(image_path) as img:
                return {
                    "width": img.width,
                    "height": img.height,
                    "format": img.format,
                    "mode": img.mode,
                    "size_bytes": os.path.getsize(image_path)
                }
        except Exception as e:
            print(f"Error getting image info for {image_path}: {str(e)}")
            return None
