import math
import pygame
from typing import Tuple

class Vector2:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y
        
    def __add__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x + other.x, self.y + other.y)
        
    def __sub__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x - other.x, self.y - other.y)
        
    def __mul__(self, scalar: float) -> 'Vector2':
        return Vector2(self.x * scalar, self.y * scalar)
        
    def __truediv__(self, scalar: float) -> 'Vector2':
        return Vector2(self.x / scalar, self.y / scalar)
        
    def __eq__(self, other: 'Vector2') -> bool:
        return abs(self.x - other.x) < 0.001 and abs(self.y - other.y) < 0.001
        
    def magnitude(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)
        
    def normalized(self) -> 'Vector2':
        mag = self.magnitude()
        if mag == 0:
            return Vector2(0, 0)
        return Vector2(self.x / mag, self.y / mag)
        
    def rotate(self, angle_degrees: float) -> 'Vector2':
        angle_rad = math.radians(angle_degrees)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        return Vector2(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )
        
    def dot(self, other: 'Vector2') -> float:
        return self.x * other.x + self.y * other.y
        
    def distance_to(self, other: 'Vector2') -> float:
        return (self - other).magnitude()
        
    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)
        
    def __str__(self) -> str:
        return f"Vector2({self.x}, {self.y})"

class Color:
    def __init__(self, r: int = 0, g: int = 0, b: int = 0, a: int = 255):
        self.r = max(0, min(255, r))
        self.g = max(0, min(255, g))
        self.b = max(0, min(255, b))
        self.a = max(0, min(255, a))
        
    @property
    def rgba(self) -> Tuple[int, int, int, int]:
        return (self.r, self.g, self.b, self.a)
        
    @property
    def rgb(self) -> Tuple[int, int, int]:
        return (self.r, self.g, self.b)
        
    def lerp(self, other: 'Color', t: float) -> 'Color':
        t = max(0, min(1, t))
        return Color(
            int(self.r + (other.r - self.r) * t),
            int(self.g + (other.g - self.g) * t),
            int(self.b + (other.b - self.b) * t),
            int(self.a + (other.a - self.a) * t)
        )
        
    def __str__(self) -> str:
        return f"Color({self.r}, {self.g}, {self.b}, {self.a})"

class Timer:
    def __init__(self, duration: float):
        self.duration = duration
        self.current_time = 0.0
        self.is_finished = False
        self.is_running = False
        
    def start(self):
        self.is_running = True
        self.is_finished = False
        self.current_time = 0.0
        
    def stop(self):
        self.is_running = False
        
    def reset(self):
        self.current_time = 0.0
        self.is_finished = False
        
    def update(self, delta_time: float):
        if self.is_running and not self.is_finished:
            self.current_time += delta_time
            if self.current_time >= self.duration:
                self.is_finished = True
                self.is_running = False
                
    def get_progress(self) -> float:
        if self.duration == 0:
            return 1.0
        return min(1.0, self.current_time / self.duration)

class Math2D:
    @staticmethod
    def lerp(a: float, b: float, t: float) -> float:
        return a + (b - a) * t
        
    @staticmethod
    def clamp(value: float, min_val: float, max_val: float) -> float:
        return max(min_val, min(max_val, value))
        
    @staticmethod
    def angle_between_vectors(v1: Vector2, v2: Vector2) -> float:
        dot = v1.dot(v2)
        mag1 = v1.magnitude()
        mag2 = v2.magnitude()
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
            
        cos_angle = dot / (mag1 * mag2)
        cos_angle = max(-1, min(1, cos_angle))
        return math.degrees(math.acos(cos_angle))
        
    @staticmethod
    def distance_point_to_line(point: Vector2, line_start: Vector2, line_end: Vector2) -> float:
        line_vec = line_end - line_start
        point_vec = point - line_start
        
        if line_vec.magnitude() == 0:
            return point_vec.magnitude()
            
        t = max(0, min(1, point_vec.dot(line_vec) / (line_vec.magnitude() ** 2)))
        projection = line_start + line_vec * t
        return point.distance_to(projection)
