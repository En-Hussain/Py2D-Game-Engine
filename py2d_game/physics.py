import pygame
from typing import List, Optional, Callable
from .utils import Vector2, Math2D

class Collider2D:
    def __init__(self, width: float, height: float, is_trigger: bool = False):
        self.width = width
        self.height = height
        self.is_trigger = is_trigger
        self.offset = Vector2(0, 0)
        self.game_object = None
        
    def get_bounds(self, position: Vector2) -> pygame.Rect:
        return pygame.Rect(
            position.x + self.offset.x - self.width / 2,
            position.y + self.offset.y - self.height / 2,
            self.width,
            self.height
        )
        
    def check_collision(self, other: 'Collider2D', pos1: Vector2, pos2: Vector2) -> bool:
        bounds1 = self.get_bounds(pos1)
        bounds2 = other.get_bounds(pos2)
        return bounds1.colliderect(bounds2)
        
    def get_collision_normal(self, other: 'Collider2D', pos1: Vector2, pos2: Vector2) -> Vector2:
        bounds1 = self.get_bounds(pos1)
        bounds2 = other.get_bounds(pos2)
        
        overlap_x = min(bounds1.right, bounds2.right) - max(bounds1.left, bounds2.left)
        overlap_y = min(bounds1.bottom, bounds2.bottom) - max(bounds1.top, bounds2.top)
        
        # Better collision normal calculation
        if overlap_x < overlap_y:
            # Horizontal collision
            if bounds1.centerx < bounds2.centerx:
                return Vector2(-1, 0)  # obj1 is to the left
            else:
                return Vector2(1, 0)   # obj1 is to the right
        else:
            # Vertical collision
            if bounds1.centery < bounds2.centery:
                return Vector2(0, -1)  # obj1 is above
            else:
                return Vector2(0, 1)   # obj1 is below

class RigidBody2D:
    def __init__(self, mass: float = 1.0, gravity_scale: float = 1.0):
        self.mass = mass
        self.velocity = Vector2(0, 0)
        self.angular_velocity = 0.0
        self.gravity_scale = gravity_scale
        self.drag = 0.0
        self.angular_drag = 0.0
        self.is_kinematic = False
        self.freeze_position_x = False
        self.freeze_position_y = False
        self.freeze_rotation = False
        
    def add_force(self, force: Vector2):
        if not self.is_kinematic:
            self.velocity += force / self.mass
            
    def add_impulse(self, impulse: Vector2):
        if not self.is_kinematic:
            self.velocity += impulse
            
    def set_velocity(self, velocity: Vector2):
        self.velocity = velocity
        
    def set_angular_velocity(self, angular_velocity: float):
        self.angular_velocity = angular_velocity

class Physics2D:
    def __init__(self, gravity: Vector2 = Vector2(0, 9.81)):
        self.gravity = gravity
        self.rigid_bodies: List[RigidBody2D] = []
        self.colliders: List[Collider2D] = []
        self.collision_callbacks: List[Callable] = []
        
    def add_rigid_body(self, rigid_body: RigidBody2D):
        self.rigid_bodies.append(rigid_body)
        
    def remove_rigid_body(self, rigid_body: RigidBody2D):
        if rigid_body in self.rigid_bodies:
            self.rigid_bodies.remove(rigid_body)
            
    def add_collider(self, collider: Collider2D):
        self.colliders.append(collider)
        
    def remove_collider(self, collider: Collider2D):
        if collider in self.colliders:
            self.colliders.remove(collider)
            
    def add_collision_callback(self, callback: Callable):
        self.collision_callbacks.append(callback)
        
    def update(self, delta_time: float, game_objects: List):
        for i, rigid_body in enumerate(self.rigid_bodies):
            if rigid_body.is_kinematic:
                continue
                
            if not rigid_body.freeze_position_x:
                rigid_body.velocity.x += self.gravity.x * rigid_body.gravity_scale * delta_time
            if not rigid_body.freeze_position_y:
                rigid_body.velocity.y += self.gravity.y * rigid_body.gravity_scale * delta_time
                
            rigid_body.velocity *= (1 - rigid_body.drag * delta_time)
            rigid_body.angular_velocity *= (1 - rigid_body.angular_drag * delta_time)
            
        self.check_collisions(game_objects)
        
    def check_collisions(self, game_objects: List):
        for i in range(len(self.colliders)):
            for j in range(i + 1, len(self.colliders)):
                collider1 = self.colliders[i]
                collider2 = self.colliders[j]
                
                if not collider1.game_object or not collider2.game_object:
                    continue
                    
                pos1 = collider1.game_object.position
                pos2 = collider2.game_object.position
                
                if collider1.check_collision(collider2, pos1, pos2):
                    self.handle_collision(collider1, collider2, pos1, pos2)
                    
    def handle_collision(self, collider1: Collider2D, collider2: Collider2D, pos1: Vector2, pos2: Vector2):
        if collider1.is_trigger or collider2.is_trigger:
            for callback in self.collision_callbacks:
                callback(collider1, collider2, pos1, pos2)
            return
            
        if not collider1.game_object or not collider2.game_object:
            return
            
        obj1 = collider1.game_object
        obj2 = collider2.game_object
        
        # Handle platform collision with better physics
        if hasattr(obj1, 'rigid_body') and hasattr(obj2, 'rigid_body'):
            rigid_body1 = obj1.rigid_body
            rigid_body2 = obj2.rigid_body
            
            if rigid_body1.is_kinematic and rigid_body2.is_kinematic:
                return
                
            normal = collider1.get_collision_normal(collider2, pos1, pos2)
            
            # Better collision response (no shaking)
            if abs(normal.y) > abs(normal.x):  # Vertical collision
                if normal.y < 0:  # obj1 is above obj2
                    if hasattr(obj1, 'on_ground') and obj1.rigid_body.velocity.y > 0:
                        obj1.on_ground = True
                        obj1.rigid_body.velocity.y = 0
                        obj1.position.y = pos2.y - collider1.height
                else:  # obj2 is above obj1
                    if hasattr(obj2, 'on_ground') and obj2.rigid_body.velocity.y > 0:
                        obj2.on_ground = True
                        obj2.rigid_body.velocity.y = 0
                        obj2.position.y = pos1.y - collider2.height
            else:  # Horizontal collision
                if normal.x < 0:  # obj1 is to the left of obj2
                    if abs(obj1.rigid_body.velocity.x) > 50:  # Only stop if moving fast enough
                        obj1.position.x = pos2.x - collider1.width
                        obj1.rigid_body.velocity.x = 0
                else:  # obj1 is to the right of obj2
                    if abs(obj1.rigid_body.velocity.x) > 50:  # Only stop if moving fast enough
                        obj1.position.x = pos2.x + collider2.width
                        obj1.rigid_body.velocity.x = 0
        else:
            # Handle collision with static objects (platforms)
            for callback in self.collision_callbacks:
                callback(collider1, collider2, pos1, pos2)
