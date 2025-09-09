import pygame
from typing import Callable, Optional
from .utils import Vector2, Color
from .graphics import Text, Shape

class UIElement:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.position = Vector2(x, y)
        self.size = Vector2(width, height)
        self.visible = True
        self.active = True
        self.parent: Optional['UIElement'] = None
        self.children: list = []
        
    def add_child(self, child: 'UIElement'):
        child.parent = self
        self.children.append(child)
        
    def remove_child(self, child: 'UIElement'):
        if child in self.children:
            child.parent = None
            self.children.remove(child)
            
    def get_world_position(self) -> Vector2:
        if self.parent:
            return self.parent.get_world_position() + self.position
        return self.position
        
    def contains_point(self, point: Vector2) -> bool:
        world_pos = self.get_world_position()
        return (world_pos.x <= point.x <= world_pos.x + self.size.x and
                world_pos.y <= point.y <= world_pos.y + self.size.y)
        
    def update(self, delta_time: float):
        if not self.active:
            return
            
        for child in self.children:
            child.update(delta_time)
            
    def render(self, screen):
        if not self.visible or not self.active:
            return
            
        for child in self.children:
            child.render(screen)

class Button(UIElement):
    def __init__(self, x: float, y: float, width: float, height: float, text: str = ""):
        super().__init__(x, y, width, height)
        self.text = Text(text, 16, Color(0, 0, 0))
        self.background_color = Color(200, 200, 200)
        self.hover_color = Color(180, 180, 180)
        self.pressed_color = Color(160, 160, 160)
        self.border_color = Color(100, 100, 100)
        self.border_width = 2
        
        self.is_hovered = False
        self.is_pressed = False
        self.on_click: Optional[Callable] = None
        
        self.background = Shape("rectangle", int(width), int(height), self.background_color)
        
    def set_text(self, text: str):
        self.text.set_text(text)
        
    def set_on_click(self, callback: Callable):
        self.on_click = callback
        
    def handle_mouse_input(self, mouse_pos: Vector2, mouse_pressed: bool):
        self.is_hovered = self.contains_point(mouse_pos)
        
        if self.is_hovered and mouse_pressed:
            self.is_pressed = True
        elif not mouse_pressed and self.is_pressed and self.is_hovered:
            if self.on_click:
                self.on_click()
            self.is_pressed = False
        elif not mouse_pressed:
            self.is_pressed = False
            
    def update(self, delta_time: float):
        super().update(delta_time)
        
    def render(self, screen):
        if not self.visible or not self.active:
            return
            
        world_pos = self.get_world_position()
        
        if self.is_pressed:
            color = self.pressed_color
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.background_color
            
        self.background.color = color
        self.background.render(screen, world_pos + self.size / 2)
        
        pygame.draw.rect(screen, self.border_color.rgba, 
                        (world_pos.x, world_pos.y, self.size.x, self.size.y), 
                        self.border_width)
        
        text_pos = world_pos + self.size / 2
        self.text.render(screen, text_pos)
        
        for child in self.children:
            child.render(screen)

class Label(UIElement):
    def __init__(self, x: float, y: float, text: str = "", font_size: int = 16, color: Color = Color(255, 255, 255)):
        super().__init__(x, y, 0, 0)
        self.text = Text(text, font_size, color)
        self.update_size()
        
    def set_text(self, text: str):
        self.text.set_text(text)
        self.update_size()
        
    def set_color(self, color: Color):
        self.text.set_color(color)
        
    def set_font_size(self, size: int):
        self.text.set_font_size(size)
        self.update_size()
        
    def update_size(self):
        if self.text.surface:
            self.size = Vector2(self.text.surface.get_width(), self.text.surface.get_height())
        
    def render(self, screen):
        if not self.visible or not self.active:
            return
            
        world_pos = self.get_world_position()
        self.text.render(screen, world_pos)
        
        for child in self.children:
            child.render(screen)

class Panel(UIElement):
    def __init__(self, x: float, y: float, width: float, height: float, 
                 background_color: Color = Color(50, 50, 50, 200), 
                 border_color: Color = Color(100, 100, 100),
                 border_width: int = 1):
        super().__init__(x, y, width, height)
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width
        
    def render(self, screen):
        if not self.visible or not self.active:
            return
            
        world_pos = self.get_world_position()
        
        if self.background_color.a < 255:
            surface = pygame.Surface((int(self.size.x), int(self.size.y)), pygame.SRCALPHA)
            surface.fill(self.background_color.rgba)
            screen.blit(surface, (world_pos.x, world_pos.y))
        else:
            pygame.draw.rect(screen, self.background_color.rgba, 
                           (world_pos.x, world_pos.y, self.size.x, self.size.y))
        
        if self.border_width > 0:
            pygame.draw.rect(screen, self.border_color.rgba, 
                           (world_pos.x, world_pos.y, self.size.x, self.size.y), 
                           self.border_width)
        
        for child in self.children:
            child.render(screen)
