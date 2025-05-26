# src/core/asset_loader.py
import pygame
import os

# Base path for assets, assumes this script is in src/core/
# and assets/ is at the same level as src/
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")

image_cache = {} # Cache for loaded images

def load_image(file_path_relative_to_images_dir, colorkey=None, use_alpha=False):
    """
    Loads an image, handles transparency, and caches it.
    file_path_relative_to_images_dir: e.g., "player/player.png" or "items/sword.png"
    colorkey: Pygame color for transparency, or -1 to use top-left pixel.
    use_alpha: Set to True if the image uses per-pixel alpha transparency.
    """
    if file_path_relative_to_images_dir in image_cache:
        return image_cache[file_path_relative_to_images_dir]

    full_path = os.path.join(IMAGES_DIR, file_path_relative_to_images_dir)

    try:
        image = pygame.image.load(full_path)
    except pygame.error as e:
        print(f"Error loading image '{full_path}': {e}")
        # Return a placeholder surface or raise error, depending on desired handling
        # For now, let's return a small, visible placeholder surface
        placeholder_surface = pygame.Surface((32, 32))
        placeholder_surface.fill((255, 0, 255)) # Bright pink as an obvious placeholder
        pygame.draw.line(placeholder_surface, (0,0,0), (0,0), (31,31), 1)
        pygame.draw.line(placeholder_surface, (0,0,0), (0,31), (31,0), 1)
        image_cache[file_path_relative_to_images_dir] = placeholder_surface # Cache placeholder too
        return placeholder_surface

    if use_alpha:
        image = image.convert_alpha() # For images with per-pixel alpha (e.g., PNGs with transparency)
    else:
        image = image.convert() # For images without alpha, faster blitting
        if colorkey is not None:
            if colorkey == -1: # Magic value: use top-left pixel color
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
    
    image_cache[file_path_relative_to_images_dir] = image
    print(f"Loaded image: {full_path}")
    return image

# Example of a sound loading function (for future use, not part of this step's core task)
# sound_cache = {}
# SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
# def load_sound(file_path_relative_to_sounds_dir):
#     # ... similar logic for loading and caching sounds ...
#     pass
