import pygame
import sys
from typing import List, Optional, Callable
from .utils import Vector2, Color
from .graphics import Sprite
from .input import InputManager
from .audio import AudioManager

class GameObject:
    def __init__(self, x: float = 0, y: float = 0):
        self.position = Vector2(x, y)
        self.rotation = 0.0
        self.scale = Vector2(1.0, 1.0)
        self.visible = True
        self.active = True
        self.sprite: Optional[Sprite] = None
        self.children: List[GameObject] = []
        self.parent: Optional[GameObject] = None
        
    def add_child(self, child: 'GameObject'):
        child.parent = self
        self.children.append(child)
        
    def remove_child(self, child: 'GameObject'):
        if child in self.children:
            child.parent = None
            self.children.remove(child)
            
    def update(self, delta_time: float):
        if not self.active:
            return
            
        for child in self.children:
            child.update(delta_time)
            
    def render(self, screen, camera):
        if not self.visible or not self.active:
            return
            
        if self.sprite:
            self.sprite.render(screen, self.position, self.rotation, self.scale, camera)
            
        for child in self.children:
            child.render(screen, camera)
            
    def get_world_position(self) -> Vector2:
        if self.parent:
            return self.parent.get_world_position() + self.position
        return self.position

class Camera:
    def __init__(self, x: float = 0, y: float = 0, zoom: float = 1.0):
        self.position = Vector2(x, y)
        self.zoom = zoom
        self.rotation = 0.0
        
    def world_to_screen(self, world_pos: Vector2) -> Vector2:
        screen_pos = world_pos - self.position
        screen_pos = screen_pos.rotate(-self.rotation)
        screen_pos = screen_pos * self.zoom
        return screen_pos
        
    def screen_to_world(self, screen_pos: Vector2) -> Vector2:
        world_pos = screen_pos / self.zoom
        world_pos = world_pos.rotate(self.rotation)
        world_pos = world_pos + self.position
        return world_pos

class Scene:
    def __init__(self, name: str):
        self.name = name
        self.game_objects: List[GameObject] = []
        self.camera = Camera()
        self.background_color = Color(0, 0, 0)
        
    def add_object(self, obj: GameObject):
        obj.scene = self
        self.game_objects.append(obj)
        
    def remove_object(self, obj: GameObject):
        if obj in self.game_objects:
            self.game_objects.remove(obj)
            
    def get_objects_by_name(self, name: str) -> List[GameObject]:
        return [obj for obj in self.game_objects if hasattr(obj, 'name') and obj.name == name]
        
    def update(self, delta_time: float):
        for obj in self.game_objects:
            obj.update(delta_time)
            
    def render(self, screen):
        screen.fill(self.background_color.rgba)
        
        for obj in self.game_objects:
            obj.render(screen, self.camera)

class Py2DEngine:
    def __init__(self, width: int = 800, height: int = 600, title: str = "Py2D Game"):
        pygame.init()
        self.width = width
        self.height = height
        self.title = title
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        
        self.clock = pygame.time.Clock()
        self.running = False
        self.fps = 60
        
        self.current_scene: Optional[Scene] = None
        self.scenes: dict = {}
        
        self.input_manager = InputManager()
        self.audio_manager = AudioManager()
        
        self.delta_time = 0.0
        
    def add_scene(self, scene: Scene):
        scene.game_engine = self
        self.scenes[scene.name] = scene
        
    def set_scene(self, scene_name: str):
        if scene_name in self.scenes:
            self.current_scene = self.scenes[scene_name]
            
    def run(self):
        self.running = True
        
        while self.running:
            self.delta_time = self.clock.tick(self.fps) / 1000.0
            
            # معالجة الأحداث
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        
            # تحديث الإدخال
            self.input_manager.update()
            
            # تحديث وعرض المشهد
            if self.current_scene:
                self.current_scene.update(self.delta_time)
                self.current_scene.render(self.screen)
                
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()
        
    def quit(self):
        self.running = False
