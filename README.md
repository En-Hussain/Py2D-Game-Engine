# Py2D Game Engine

![Py2D Game Engine](https://sdmntprcentralus.oaiusercontent.com/files/00000000-36e4-61f5-aa56-ef2db6203bc2/raw?se=2025-09-09T13%3A31%3A49Z&sp=r&sv=2024-08-04&sr=b&scid=643fa069-9332-5d20-a501-56c8d9f804a6&skoid=04233560-0ad7-493e-8bf0-1347c317d021&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-09-09T09%3A38%3A22Z&ske=2025-09-10T09%3A38%3A22Z&sks=b&skv=2024-08-04&sig=OVLIXpo77bpkSgxn7DSOmAzDVzohZ5SeHyCgc4XbW9U%3D)

A powerful and easy-to-use Python library for creating 2D games with high capabilities and excellent performance.

## 🚀 Version 1.0.0 Beta

> **Note**: This is a beta version of Py2D Game Engine. Some features may be experimental and subject to change.

## Features

### 🎮 Core Game Engine
- **Py2DEngine**: Main game engine with window and scene management
- **GameObject**: Advanced object system with hierarchical structure
- **Scene**: Scene and layer management
- **Camera**: Advanced camera system with zoom and rotation

### 🎨 Graphics System
- **Sprite**: Image and graphics management
- **Animation**: Advanced animation system
- **Text**: Text rendering with custom fonts
- **Shape**: Geometric shape drawing
- **TileMap**: Tile maps for large worlds

### 🎵 Audio System
- **AudioManager**: Sound and music management
- Support for various audio formats
- Volume control
- Advanced sound effects

### 🎯 Physics System
- **Physics2D**: 2D physics engine
- **RigidBody2D**: Rigid bodies with gravity
- **Collider2D**: Advanced collision system
- Collision detection and interactions

### ⌨️ Input System
- **InputManager**: Keyboard and mouse management
- Vector movement support
- Advanced input events
- Keyboard shortcuts

### 🖼️ User Interface
- **UIElement**: Basic UI elements
- **Button**: Interactive buttons
- **Label**: Text labels
- **Panel**: Container panels

## Installation

```bash
pip install py2d-game
```

Or from source:

```bash
git clone https://github.com/En-Hussain/py2d-game.git
cd py2d-game
pip install -e .
```

## Quick Start

### Simple Game

```python
from py2d_game import Py2DEngine, GameObject, Scene, Sprite, Color, Vector2

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite(width=32, height=32, color=Color(0, 255, 0))
        self.speed = 200
        
    def update(self, delta_time):
        super().update(delta_time)
        
        input_manager = self.scene.game_engine.input_manager
        movement = input_manager.get_movement_vector()
        self.position += movement * self.speed * delta_time

def main():
    engine = Py2DEngine(800, 600, "My First Game")
    
    scene = Scene("Main Game")
    scene.background_color = Color(50, 50, 100)
    
    player = Player(400, 300)
    scene.add_object(player)
    
    engine.add_scene(scene)
    engine.set_scene("Main Game")
    engine.run()

if __name__ == "__main__":
    main()
```

### Platformer Game

```python
from py2d_game import Py2DEngine, GameObject, Scene, Sprite, Color, Physics2D, RigidBody2D, Collider2D

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite(width=24, height=32, color=Color(0, 255, 0))
        self.rigid_body = RigidBody2D(mass=1.0, gravity_scale=1.0)
        self.collider = Collider2D(24, 32)
        self.collider.game_object = self
        self.speed = 300
        self.jump_force = 400
        
    def update(self, delta_time):
        super().update(delta_time)
        
        input_manager = self.scene.game_engine.input_manager
        
        if input_manager.is_key_pressed('left'):
            self.rigid_body.velocity.x = -self.speed
        elif input_manager.is_key_pressed('right'):
            self.rigid_body.velocity.x = self.speed
            
        if input_manager.is_key_just_pressed('space'):
            self.rigid_body.velocity.y = -self.jump_force
            
        self.position += self.rigid_body.velocity * delta_time

def main():
    engine = Py2DEngine(800, 600, "Platformer Game")
    
    scene = Scene("Main Game")
    physics = Physics2D(Vector2(0, 500))
    
    player = Player(100, 400)
    scene.add_object(player)
    physics.add_rigid_body(player.rigid_body)
    physics.add_collider(player.collider)
    
    engine.add_scene(scene)
    engine.set_scene("Main Game")
    engine.run()

if __name__ == "__main__":
    main()
```

## Included Examples

The library includes several ready-to-use examples:

1. **Simple Game** (`examples/simple_game.py`) - Basic game with player and enemies
2. **Platformer Game** (`examples/platformer_game.py`) - Platformer with physics
3. **Space Shooter** (`examples/space_shooter.py`) - Space shooting game
4. **Simple Platformer** (`platformer_simple.py`) - Simplified platformer
5. **Simple Space Shooter** (`space_shooter_simple.py`) - Simplified space shooter

To run the examples:

```bash
python examples/simple_game.py
python examples/platformer_game.py
python examples/space_shooter.py
python platformer_simple.py
python space_shooter_simple.py
```

## Complete Documentation

### Py2DEngine

The main game engine:

```python
engine = Py2DEngine(width=800, height=600, title="My Game")
engine.add_scene(scene)
engine.set_scene("scene_name")
engine.run()
```

### GameObject

Basic game objects:

```python
class MyObject(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite(width=32, height=32, color=Color(255, 0, 0))
        
    def update(self, delta_time):
        super().update(delta_time)
        # Update logic here
```

### Input System

```python
input_manager = engine.input_manager

# Check keys
if input_manager.is_key_pressed('space'):
    # Do something

if input_manager.is_key_just_pressed('enter'):
    # Do something once

# Get movement vector
movement = input_manager.get_movement_vector()

# Check mouse
if input_manager.is_mouse_button_pressed(1):  # Left mouse button
    mouse_pos = input_manager.get_mouse_position()
```

### Audio System

```python
audio_manager = engine.audio_manager

# Load and play sound
audio_manager.load_sound("jump", "sounds/jump.wav")
audio_manager.play_sound("jump")

# Load and play music
audio_manager.load_music("background_music.mp3")
audio_manager.play_music(loop=-1)  # Infinite loop
```

### Physics System

```python
physics = Physics2D(Vector2(0, 500))  # Gravity

# Add rigid body
rigid_body = RigidBody2D(mass=1.0, gravity_scale=1.0)
physics.add_rigid_body(rigid_body)

# Add collider
collider = Collider2D(32, 32)
physics.add_collider(collider)

# Update physics
physics.update(delta_time, game_objects)
```

## Requirements

- Python 3.7 or higher
- pygame 2.0.0 or higher

## License

This library is licensed under the MIT License. See the LICENSE file for details.

## Contributing

We welcome contributions! Please read the contributing guide before submitting pull requests.

## Technical Support

For technical support and questions, please contact:

- **Email**: support@py2d-game.com
- **GitHub**: [En-Hussain](https://github.com/En-Hussain)
- **Issues**: [GitHub Issues](https://github.com/En-Hussain/py2d-game/issues)

## Upcoming Features

- [ ] Advanced animation system
- [ ] Particle system
- [ ] Multiplayer networking support
- [ ] Advanced development tools
- [ ] Support for more image formats

## Changelog

### Version 1.0.0
- Initial release
- Core game engine
- Graphics system
- Physics system
- Input system
- Audio system
- UI system
- Example games

---

**Py2D Game Engine** - Make game development easy and fun! 🎮

Created by [En-Hussain](https://github.com/En-Hussain)