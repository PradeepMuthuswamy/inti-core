"""
CAD Processing Engine for Inticore Estimation Automation
Handles geometry extraction from STEP/STL/OBJ files using Trimesh
"""

import trimesh
import numpy as np
from typing import Dict, Any, Optional
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CADProcessor:
    """Processes CAD files and extracts geometric properties"""
    
    def __init__(self):
        self.supported_formats = ['.stl', '.obj', '.ply', '.off', '.glb', '.gltf']
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process CAD file and extract geometric properties
        
        Args:
            file_path: Path to the CAD file
            
        Returns:
            Dictionary containing extracted properties
        """
        try:
            # Load the mesh
            mesh = trimesh.load(file_path)
            
            # Ensure we have a valid mesh
            if not hasattr(mesh, 'volume') or mesh.volume is None:
                raise Exception("Invalid mesh: no volume data")
            
            # Detect units - if volume is too large, likely in meters not mm
            # STL files are often in meters or mm
            raw_volume = float(mesh.volume) if mesh.volume > 0 else 0.0
            raw_area = float(mesh.area) if hasattr(mesh, 'area') and mesh.area > 0 else 0.0
            
            # Auto-detect units: if volume > 1, likely in meters (need to convert to mm³)
            # if volume < 0.001, likely already in mm³
            if raw_volume > 1:  # Likely in meters
                volume_mm3 = raw_volume * 1e9  # m³ to mm³
                surface_area_mm2 = raw_area * 1e6  # m² to mm²
            elif raw_volume < 0.001:  # Already in mm
                volume_mm3 = raw_volume
                surface_area_mm2 = raw_area
            else:  # Ambiguous, check bounding box
                bounds = mesh.bounds
                max_dimension = max(abs(bounds[1][0] - bounds[0][0]), 
                                  abs(bounds[1][1] - bounds[0][1]), 
                                  abs(bounds[1][2] - bounds[0][2]))
                if max_dimension > 1:  # Likely meters
                    volume_mm3 = raw_volume * 1e9
                    surface_area_mm2 = raw_area * 1e6
                else:  # Likely mm
                    volume_mm3 = raw_volume
                    surface_area_mm2 = raw_area
            
            properties = {
                'volume_mm3': volume_mm3,
                'surface_area_mm2': surface_area_mm2,
                'bounding_box': self._get_bounding_box(mesh),
                'weight_kg': self._calculate_weight(mesh),
                'features': self._detect_features(mesh),
                'complexity_score': self._calculate_complexity(mesh)
            }
            
            logger.info(f"Successfully processed {file_path}")
            return properties
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")
            raise Exception(f"Failed to process CAD file: {str(e)}")
    
    def _get_bounding_box(self, mesh) -> Dict[str, float]:
        """Get bounding box dimensions in mm"""
        bounds = mesh.bounds
        # Check if units are in meters or mm
        max_dim = max(abs(bounds[1][0] - bounds[0][0]), 
                     abs(bounds[1][1] - bounds[0][1]), 
                     abs(bounds[1][2] - bounds[0][2]))
        
        if max_dim > 1:  # Likely in meters
            scale = 1000
        else:  # Likely in mm
            scale = 1
            
        return {
            'length': float(bounds[1][0] - bounds[0][0]) * scale,
            'width': float(bounds[1][1] - bounds[0][1]) * scale,
            'height': float(bounds[1][2] - bounds[0][2]) * scale
        }
    
    def _calculate_weight(self, mesh, density: float = 2.68) -> float:
        """Calculate weight based on volume (density passed from material selection)"""
        # Note: Weight will be recalculated in estimation engine with correct material density
        # This is just for display purposes using aluminum as default
        raw_volume = mesh.volume
        
        # Detect units
        if raw_volume > 1:  # In meters
            volume_cc = raw_volume * 1e6  # m³ to cm³
        else:  # In mm
            volume_cc = raw_volume / 1000  # mm³ to cm³
            
        weight_kg = (volume_cc * density) / 1000  # Convert to kg
        return round(weight_kg, 3)
    
    def _detect_features(self, mesh) -> Dict[str, int]:
        """Detect basic features in the mesh"""
        # This is a simplified feature detection
        # In a real implementation, you'd use more sophisticated algorithms
        
        # Count holes (simplified - based on mesh topology)
        holes = self._count_holes(mesh)
        
        # Count edges and faces
        edges = len(mesh.edges)
        faces = len(mesh.faces)
        
        return {
            'holes': holes,
            'edges': edges,
            'faces': faces,
            'vertices': len(mesh.vertices)
        }
    
    def _count_holes(self, mesh) -> int:
        """Simplified hole counting based on mesh analysis"""
        # This is a placeholder - real hole detection requires sophisticated algorithms
        # For now, return 0 as we cannot reliably detect holes from mesh
        return 0
    
    def _calculate_complexity(self, mesh) -> float:
        """Calculate complexity score (0-1)"""
        try:
            # Simple complexity metric based on surface area to volume ratio
            if mesh.volume > 0 and hasattr(mesh, 'area') and mesh.area > 0:
                ratio = mesh.area / mesh.volume
                # Normalize to 0-1 scale
                complexity = min(ratio / 100, 1.0)
                return round(complexity, 2)
            # Fallback: use bounding box dimensions as complexity indicator
            elif mesh.volume > 0:
                bounds = mesh.bounds
                if bounds is not None:
                    dimensions = bounds[1] - bounds[0]
                    max_dim = max(dimensions)
                    min_dim = min(dimensions)
                    if min_dim > 0:
                        aspect_ratio = max_dim / min_dim
                        complexity = min(aspect_ratio / 10, 1.0)
                        return round(complexity, 2)
            return 0.5
        except:
            return 0.5
    
    def validate_file(self, file_path: str) -> bool:
        """Validate if file can be processed"""
        try:
            # Check file extension
            file_ext = file_path.lower().split('.')[-1]
            if f'.{file_ext}' not in self.supported_formats:
                return False
            
            # Try to load the file
            mesh = trimesh.load(file_path)
            return mesh is not None
            
        except Exception as e:
            logger.error(f"File validation failed: {str(e)}")
            return False

