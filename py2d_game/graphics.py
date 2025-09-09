import pygame
from typing import List, Optional, Tuple
from .utils import Vector2, Color

class Sprite:
    def __init__(self, image_path: str = None, width: int = 32, height: int = 32, color: Color = None):
        self.image = None
        self.width = width
        self.height = height
        self.color = color or Color(255, 255, 255)
        
        if image_path:
            self.load_image(image_path)
        else:
            self.create_colored_surface()
            
    def load_image(self, image_path: str):
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.width = self.image.get_width()
            self.height = self.image.get_height()
        except pygame.error:
            self.create_colored_surface()
            
    def create_colored_surface(self):
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(self.color.rgba)
        
    def render(self, screen, position: Vector2, rotation: float = 0, scale: Vector2 = None, camera=None):
        if not self.image:
            return
            
        scale = scale or Vector2(1, 1)
        
        if camera:
            screen_pos = camera.world_to_screen(position)
        else:
            screen_pos = position
            
        if rotation != 0 or scale.x != 1 or scale.y != 1:
            scaled_width = int(self.width * scale.x)
            scaled_height = int(self.height * scale.y)
            
            if scaled_width > 0 and scaled_height > 0:
                scaled_image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
                if rotation != 0:
                    scaled_image = pygame.transform.rotate(scaled_image, rotation)
                screen.blit(scaled_image, (screen_pos.x - scaled_width//2, screen_pos.y - scaled_height//2))
        else:
            screen.blit(self.image, (screen_pos.x - self.width//2, screen_pos.y - self.height//2))

class Animation:
    def __init__(self, frames: List[pygame.Surface], frame_duration: float = 0.1):
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.current_time = 0.0
        self.is_playing = False
        self.loop = True
        
    def play(self):
        self.is_playing = True
        self.current_frame = 0
        self.current_time = 0.0
        
    def stop(self):
        self.is_playing = False
        
    def pause(self):
        self.is_playing = False
        
    def update(self, delta_time: float):
        if not self.is_playing:
            return
            
        self.current_time += delta_time
        
        if self.current_time >= self.frame_duration:
            self.current_time = 0.0
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.is_playing = False
                    
    def get_current_frame(self) -> pygame.Surface:
        if self.frames and 0 <= self.current_frame < len(self.frames):
            return self.frames[self.current_frame]
        return None

class Text:
    def __init__(self, text: str = "", font_size: int = 24, color: Color = Color(255, 255, 255), font_name: str = None):
        self.text = text
        self.font_size = font_size
        self.color = color
        self.font_name = font_name
        self.font = None
        self.surface = None
        
        self.load_font()
        self.update_surface()
        
    def load_font(self):
        try:
            if self.font_name:
                self.font = pygame.font.Font(self.font_name, self.font_size)
            else:
                self.font = pygame.font.Font(None, self.font_size)
        except:
            self.font = pygame.font.Font(None, self.font_size)
            
    def set_text(self, text: str):
        self.text = text
        self.update_surface()
        
    def set_color(self, color: Color):
        self.color = color
        self.update_surface()
        
    def set_font_size(self, size: int):
        self.font_size = size
        self.load_font()
        self.update_surface()
        
    def update_surface(self):
        if self.font and self.text:
            self.surface = self.font.render(self.text, True, self.color.rgba)
        else:
            self.surface = None
            
    def render(self, screen, position: Vector2, camera=None):
        if not self.surface:
            return
            
        if camera:
            screen_pos = camera.world_to_screen(position)
        else:
            screen_pos = position
            
        screen.blit(self.surface, (screen_pos.x, screen_pos.y))

class Shape:
    def __init__(self, shape_type: str, width: int, height: int, color: Color = Color(255, 255, 255)):
        self.shape_type = shape_type
        self.width = width
        self.height = height
        self.color = color
        self.surface = None
        self.create_surface()
        
    def create_surface(self):
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        if self.shape_type == "rectangle":
            pygame.draw.rect(self.surface, self.color.rgba, (0, 0, self.width, self.height))
        elif self.shape_type == "circle":
            center = (self.width // 2, self.height // 2)
            radius = min(self.width, self.height) // 2
            pygame.draw.circle(self.surface, self.color.rgba, center, radius)
        elif self.shape_type == "ellipse":
            pygame.draw.ellipse(self.surface, self.color.rgba, (0, 0, self.width, self.height))
            
    def render(self, screen, position: Vector2, rotation: float = 0, scale: Vector2 = None, camera=None):
        if not self.surface:
            return
            
        scale = scale or Vector2(1, 1)
        
        if camera:
            screen_pos = camera.world_to_screen(position)
        else:
            screen_pos = position
            
        if rotation != 0 or scale.x != 1 or scale.y != 1:
            scaled_width = int(self.width * scale.x)
            scaled_height = int(self.height * scale.y)
            
            if scaled_width > 0 and scaled_height > 0:
                scaled_surface = pygame.transform.scale(self.surface, (scaled_width, scaled_height))
                if rotation != 0:
                    scaled_surface = pygame.transform.rotate(scaled_surface, rotation)
                screen.blit(scaled_surface, (screen_pos.x - scaled_width//2, screen_pos.y - scaled_height//2))
        else:
            screen.blit(self.surface, (screen_pos.x - self.width//2, screen_pos.y - self.height//2))

class TileMap:
    def __init__(self, tile_width: int, tile_height: int, map_width: int, map_height: int):
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.map_width = map_width
        self.map_height = map_height
        self.tiles = {}
        self.tile_sprites = {}
        
    def set_tile(self, x: int, y: int, tile_id: int):
        if 0 <= x < self.map_width and 0 <= y < self.map_height:
            self.tiles[(x, y)] = tile_id
            
    def get_tile(self, x: int, y: int) -> int:
        return self.tiles.get((x, y), 0)
        
    def add_tile_sprite(self, tile_id: int, sprite: Sprite):
        self.tile_sprites[tile_id] = sprite
        
    def render(self, screen, camera, offset: Vector2 = Vector2(0, 0)):
        start_x = max(0, int((camera.position.x - offset.x - camera.width/2) // self.tile_width))
        start_y = max(0, int((camera.position.y - offset.y - camera.height/2) // self.tile_height))
        end_x = min(self.map_width, int((camera.position.x - offset.x + camera.width/2) // self.tile_width) + 1)
        end_y = min(self.map_height, int((camera.position.y - offset.y + camera.height/2) // self.tile_height) + 1)
        
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile_id = self.get_tile(x, y)
                if tile_id in self.tile_sprites:
                    world_pos = Vector2(
                        x * self.tile_width + self.tile_width // 2 + offset.x,
                        y * self.tile_height + self.tile_height // 2 + offset.y
                    )
                    self.tile_sprites[tile_id].render(screen, world_pos, 0, Vector2(1, 1), camera)
