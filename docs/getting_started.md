# Getting Started with Py2D Game Engine

This guide will help you get started with Py2D Game Engine and create your first game.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Install Py2D Game Engine

```bash
pip install py2d-game
```

### Verify Installation

```python
import py2d_game
print(f"Py2D Game Engine version: {py2d_game.__version__}")
```

## Basic Usage

### Creating Your First Game

Here's a simple example to get you started:

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
    # Create the game engine
    engine = Py2DEngine(800, 600, "My First Game")
    
    # Create a scene
    scene = Scene("Main Game")
    scene.background_color = Color(50, 50, 100)
    
    # Create a player
    player = Player(400, 300)
    scene.add_object(player)
    
    # Add scene to engine and run
    engine.add_scene(scene)
    engine.set_scene("Main Game")
    engine.run()

if __name__ == "__main__":
    main()
```

### Running the Game

Save the code above to a file called `my_game.py` and run it:

```bash
python my_game.py
```

You should see a window with a green square that you can move using WASD keys or arrow keys.

## Key Concepts

### Game Engine

The `Py2DEngine` is the main class that manages the game loop, window, and scenes.

### Game Objects

`GameObject` is the base class for all game entities. It has properties like position, rotation, scale, and visibility.

### Scenes

`Scene` represents a level or screen in your game. It contains game objects and manages rendering.

### Sprites

`Sprite` represents visual elements in your game. It can be an image or a colored rectangle.

### Input

The `InputManager` handles keyboard and mouse input. Use `get_movement_vector()` for smooth movement.

## Next Steps

1. **Learn about Graphics**: See how to use sprites, animations, and text
2. **Add Physics**: Implement collision detection and physics
3. **Handle Input**: Learn about different input methods
4. **Add Audio**: Include sound effects and music
5. **Create UI**: Build user interfaces for your game

## Examples

Check out the included examples:

- `examples/simple_game.py` - Basic movement and input
- `examples/platformer_game.py` - Platformer with physics
- `examples/space_shooter.py` - Space shooting game

## Getting Help

If you run into issues:

1. Check the [Troubleshooting](troubleshooting.md) guide
2. Look at the [API Reference](api_reference.md)
3. Contact support: support@py2d-game.com
4. Open an issue on [GitHub](https://github.com/En-Hussain/py2d-game/issues)

## What's Next?

Now that you have Py2D Game Engine installed and running, you can:

1. Explore the [API Reference](api_reference.md) to learn about all available classes and methods
2. Follow the [Tutorials](tutorials/) to build more complex games
3. Check out the [Examples](examples/) for inspiration
4. Read about [Best Practices](best_practices.md) for game development

Happy game development! 🎮
