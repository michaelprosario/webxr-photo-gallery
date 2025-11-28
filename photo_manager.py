import os
import shutil
from datetime import datetime
from typing import List, Optional, Dict
import json


class PhotoArchiveManager:
    """
    Manages the photo archive using a file system-based structure.
    Organizes photos into collections (folders).
    """
    
    def __init__(self, base_path: str):
        """
        Initialize the photo archive manager.
        
        Args:
            base_path: Base directory for the photo archive
        """
        self.base_path = base_path
        self._ensure_base_directory()
    
    def _ensure_base_directory(self):
        """Ensure the base archive directory exists"""
        os.makedirs(self.base_path, exist_ok=True)
    
    def create_collection(self, collection_name: str) -> str:
        """
        Create a new collection (folder) in the archive.
        
        Args:
            collection_name: Name of the collection
        
        Returns:
            str: Full path to the created collection
        """
        # Sanitize collection name
        safe_name = self._sanitize_name(collection_name)
        collection_path = os.path.join(self.base_path, safe_name)
        
        # Create directory if it doesn't exist
        os.makedirs(collection_path, exist_ok=True)
        
        # Create metadata file
        self._create_metadata(collection_path, collection_name)
        
        return collection_path
    
    def _sanitize_name(self, name: str) -> str:
        """
        Sanitize a collection name to be filesystem-safe.
        
        Args:
            name: Original name
        
        Returns:
            str: Sanitized name
        """
        # Replace spaces and special characters
        safe_name = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in name)
        return safe_name
    
    def _create_metadata(self, collection_path: str, original_name: str):
        """
        Create or update metadata file for a collection.
        
        Args:
            collection_path: Path to the collection
            original_name: Original collection name
        """
        metadata_file = os.path.join(collection_path, '.metadata.json')
        
        # Check if metadata already exists
        if os.path.exists(metadata_file):
            return
        
        metadata = {
            "name": original_name,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _update_metadata(self, collection_path: str):
        """Update the updated_at timestamp in metadata"""
        metadata_file = os.path.join(collection_path, '.metadata.json')
        
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            metadata['updated_at'] = datetime.now().isoformat()
            
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
    
    def list_collections(self) -> List[str]:
        """
        List all collections in the archive.
        
        Returns:
            List of collection names
        """
        if not os.path.exists(self.base_path):
            return []
        
        collections = []
        for item in os.listdir(self.base_path):
            item_path = os.path.join(self.base_path, item)
            if os.path.isdir(item_path):
                collections.append(item)
        
        return sorted(collections)
    
    def collection_exists(self, collection_name: str) -> bool:
        """
        Check if a collection exists.
        
        Args:
            collection_name: Name of the collection
        
        Returns:
            bool: True if collection exists
        """
        safe_name = self._sanitize_name(collection_name)
        collection_path = os.path.join(self.base_path, safe_name)
        return os.path.isdir(collection_path)
    
    def get_collection_path(self, collection_name: str) -> Optional[str]:
        """
        Get the full path to a collection.
        
        Args:
            collection_name: Name of the collection
        
        Returns:
            str or None: Full path if exists, None otherwise
        """
        safe_name = self._sanitize_name(collection_name)
        collection_path = os.path.join(self.base_path, safe_name)
        
        if os.path.isdir(collection_path):
            return collection_path
        return None
    
    def get_collection_info(self, collection_name: str) -> Dict:
        """
        Get detailed information about a collection.
        
        Args:
            collection_name: Name of the collection
        
        Returns:
            Dictionary with collection information
        """
        safe_name = self._sanitize_name(collection_name)
        collection_path = os.path.join(self.base_path, safe_name)
        
        if not os.path.isdir(collection_path):
            return {}
        
        # Read metadata
        metadata_file = os.path.join(collection_path, '.metadata.json')
        metadata = {}
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
        
        # Count photos (exclude metadata file)
        photo_count = 0
        total_size = 0
        photos = []
        
        for item in os.listdir(collection_path):
            if item == '.metadata.json':
                continue
            
            item_path = os.path.join(collection_path, item)
            if os.path.isfile(item_path):
                photo_count += 1
                file_size = os.path.getsize(item_path)
                total_size += file_size
                photos.append({
                    "filename": item,
                    "size_bytes": file_size,
                    "modified_at": datetime.fromtimestamp(os.path.getmtime(item_path)).isoformat()
                })
        
        return {
            "collection_name": metadata.get("name", collection_name),
            "folder_name": safe_name,
            "path": collection_path,
            "photo_count": photo_count,
            "total_size_bytes": total_size,
            "created_at": metadata.get("created_at"),
            "updated_at": metadata.get("updated_at"),
            "photos": sorted(photos, key=lambda x: x['filename'])
        }
    
    def delete_collection(self, collection_name: str) -> bool:
        """
        Delete a collection and all its contents.
        
        Args:
            collection_name: Name of the collection
        
        Returns:
            bool: True if successful, False otherwise
        """
        safe_name = self._sanitize_name(collection_name)
        collection_path = os.path.join(self.base_path, safe_name)
        
        if not os.path.isdir(collection_path):
            return False
        
        try:
            shutil.rmtree(collection_path)
            return True
        except Exception as e:
            print(f"Error deleting collection {collection_name}: {str(e)}")
            return False
    
    def get_photo_path(self, collection_name: str, photo_filename: str) -> Optional[str]:
        """
        Get the full path to a specific photo.
        
        Args:
            collection_name: Name of the collection
            photo_filename: Name of the photo file
        
        Returns:
            str or None: Full path if exists, None otherwise
        """
        collection_path = self.get_collection_path(collection_name)
        if not collection_path:
            return None
        
        photo_path = os.path.join(collection_path, photo_filename)
        if os.path.isfile(photo_path):
            return photo_path
        
        return None
