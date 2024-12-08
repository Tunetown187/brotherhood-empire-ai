import bpy
import json
import random
from pathlib import Path
import logging
from typing import List, Dict
import numpy as np

class NFT3DGenerator:
    def __init__(self):
        self.setup_logging()
        self.load_config()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('NFT3DGenerator')
        
    def load_config(self):
        config_path = Path('config/nft_config.json')
        if config_path.exists():
            with open(config_path, 'r') as f:
                self.config = json.load(f)
                
    def generate_3d_model(self, traits: Dict):
        """Generate a 3D model with given traits"""
        try:
            # Clear existing scene
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete()
            
            # Create base model
            if traits['base_type'] == 'humanoid':
                self.create_humanoid_base()
            elif traits['base_type'] == 'creature':
                self.create_creature_base()
                
            # Apply materials and textures
            self.apply_materials(traits['materials'])
            
            # Add accessories
            for accessory in traits['accessories']:
                self.add_accessory(accessory)
                
            # Set up lighting
            self.setup_lighting()
            
            # Render settings
            self.setup_render_settings()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error generating 3D model: {str(e)}")
            return False
            
    def create_humanoid_base(self):
        """Create humanoid base mesh"""
        bpy.ops.mesh.primitive_cube_add()
        body = bpy.context.active_object
        
        # Add modifiers for smooth mesh
        modifier = body.modifiers.new(name="Subsurf", type='SUBSURF')
        modifier.levels = 2
        
    def create_creature_base(self):
        """Create creature base mesh"""
        bpy.ops.mesh.primitive_uv_sphere_add()
        body = bpy.context.active_object
        
        # Add modifiers for organic shape
        modifier = body.modifiers.new(name="Subsurf", type='SUBSURF')
        modifier.levels = 3
        
    def apply_materials(self, materials: List[Dict]):
        """Apply materials to model"""
        for mat_data in materials:
            mat = bpy.data.materials.new(name=mat_data['name'])
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            
            # Create PBR material
            principled = nodes.get('Principled BSDF')
            if principled:
                principled.inputs['Base Color'].default_value = mat_data['color']
                principled.inputs['Metallic'].default_value = mat_data['metallic']
                principled.inputs['Roughness'].default_value = mat_data['roughness']
                
    def add_accessory(self, accessory: Dict):
        """Add accessory to model"""
        if accessory['type'] == 'weapon':
            self.add_weapon(accessory)
        elif accessory['type'] == 'armor':
            self.add_armor(accessory)
            
    def setup_lighting(self):
        """Set up three-point lighting"""
        # Key light
        bpy.ops.object.light_add(type='AREA', location=(5, -5, 5))
        key_light = bpy.context.active_object
        key_light.data.energy = 1000
        
        # Fill light
        bpy.ops.object.light_add(type='AREA', location=(-5, -2, 3))
        fill_light = bpy.context.active_object
        fill_light.data.energy = 500
        
        # Back light
        bpy.ops.object.light_add(type='AREA', location=(0, 5, 4))
        back_light = bpy.context.active_object
        back_light.data.energy = 750
        
    def setup_render_settings(self):
        """Configure render settings"""
        scene = bpy.context.scene
        scene.render.engine = 'CYCLES'
        scene.cycles.samples = 128
        scene.render.resolution_x = 2048
        scene.render.resolution_y = 2048
        
    def export_model(self, output_path: str, format: str = 'GLB'):
        """Export 3D model"""
        try:
            if format == 'GLB':
                bpy.ops.export_scene.gltf(
                    filepath=output_path,
                    export_format='GLB',
                    export_draco_mesh_compression_enable=True
                )
            elif format == 'FBX':
                bpy.ops.export_scene.fbx(
                    filepath=output_path,
                    use_selection=False
                )
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting model: {str(e)}")
            return False
