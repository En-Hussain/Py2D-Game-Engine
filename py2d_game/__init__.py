from .core import Py2DEngine, GameObject, Scene, Camera
from .graphics import Sprite, Animation, Text, Shape, TileMap
from .input import InputManager
from .audio import AudioManager
from .physics import Physics2D, Collider2D, RigidBody2D
from .utils import Vector2, Color, Timer, Math2D
from .ui import Button, Label, Panel, UIElement

__version__ = "1.0.0-beta"
__author__ = "En-Hussain"
__description__ = "A powerful and easy-to-use Python library for creating 2D games"

__all__ = [
    "Py2DEngine",
    "GameObject", 
    "Scene",
    "Camera",
    "Sprite",
    "Animation",
    "Text",
    "Shape",
    "TileMap",
    "InputManager",
    "AudioManager", 
    "Physics2D",
    "Collider2D",
    "RigidBody2D",
    "Vector2",
    "Color",
    "Timer",
    "Math2D",
    "Button",
    "Label", 
    "Panel",
    "UIElement"
]
