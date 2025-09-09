import pygame
from typing import Dict, Set
from .utils import Vector2

class InputManager:
    def __init__(self):
        self.keys_pressed: Set[int] = set()
        self.keys_just_pressed: Set[int] = set()
        self.keys_just_released: Set[int] = set()
        
        self.mouse_buttons_pressed: Set[int] = set()
        self.mouse_buttons_just_pressed: Set[int] = set()
        self.mouse_buttons_just_released: Set[int] = set()
        
        self.mouse_position = Vector2(0, 0)
        self.mouse_delta = Vector2(0, 0)
        self.mouse_wheel = 0
        
        self.key_mappings = {
            'up': pygame.K_UP,
            'down': pygame.K_DOWN,
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'space': pygame.K_SPACE,
            'enter': pygame.K_RETURN,
            'escape': pygame.K_ESCAPE,
            'w': pygame.K_w,
            'a': pygame.K_a,
            's': pygame.K_s,
            'd': pygame.K_d,
            'shift': pygame.K_LSHIFT,
            'ctrl': pygame.K_LCTRL,
            'alt': pygame.K_LALT
        }
        
    def update(self):
        self.keys_just_pressed.clear()
        self.keys_just_released.clear()
        self.mouse_buttons_just_pressed.clear()
        self.mouse_buttons_just_released.clear()
        self.mouse_delta = Vector2(0, 0)
        self.mouse_wheel = 0
        
        # تحديث حالة المفاتيح
        keys = pygame.key.get_pressed()
        for key in self.key_mappings.values():
            if keys[key] and key not in self.keys_pressed:
                self.keys_just_pressed.add(key)
                self.keys_pressed.add(key)
            elif not keys[key] and key in self.keys_pressed:
                self.keys_just_released.add(key)
                self.keys_pressed.discard(key)
        
        # تحديث حالة الماوس
        mouse_buttons = pygame.mouse.get_pressed()
        for i, pressed in enumerate(mouse_buttons):
            if pressed and i not in self.mouse_buttons_pressed:
                self.mouse_buttons_just_pressed.add(i)
                self.mouse_buttons_pressed.add(i)
            elif not pressed and i in self.mouse_buttons_pressed:
                self.mouse_buttons_just_released.add(i)
                self.mouse_buttons_pressed.discard(i)
        
        # تحديث موقع الماوس
        old_pos = self.mouse_position
        mouse_pos = pygame.mouse.get_pos()
        self.mouse_position = Vector2(mouse_pos[0], mouse_pos[1])
        self.mouse_delta = self.mouse_position - old_pos
                
    def is_key_pressed(self, key) -> bool:
        if isinstance(key, str):
            key = self.key_mappings.get(key, key)
        return key in self.keys_pressed
        
    def is_key_just_pressed(self, key) -> bool:
        if isinstance(key, str):
            key = self.key_mappings.get(key, key)
        return key in self.keys_just_pressed
        
    def is_key_just_released(self, key) -> bool:
        if isinstance(key, str):
            key = self.key_mappings.get(key, key)
        return key in self.keys_just_released
        
    def is_mouse_button_pressed(self, button: int) -> bool:
        return button in self.mouse_buttons_pressed
        
    def is_mouse_button_just_pressed(self, button: int) -> bool:
        return button in self.mouse_buttons_just_pressed
        
    def is_mouse_button_just_released(self, button: int) -> bool:
        return button in self.mouse_buttons_just_released
        
    def get_mouse_position(self) -> Vector2:
        return self.mouse_position
        
    def get_mouse_delta(self) -> Vector2:
        return self.mouse_delta
        
    def get_mouse_wheel(self) -> int:
        return self.mouse_wheel
        
    def get_movement_vector(self) -> Vector2:
        movement = Vector2(0, 0)
        
        if self.is_key_pressed('left') or self.is_key_pressed('a'):
            movement.x -= 1
        if self.is_key_pressed('right') or self.is_key_pressed('d'):
            movement.x += 1
        if self.is_key_pressed('up') or self.is_key_pressed('w'):
            movement.y -= 1
        if self.is_key_pressed('down') or self.is_key_pressed('s'):
            movement.y += 1
            
        return movement.normalized() if movement.magnitude() > 0 else Vector2(0, 0)
