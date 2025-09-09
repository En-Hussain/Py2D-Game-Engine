# Examples

This directory contains example games and code snippets that demonstrate various features of Py2D Game Engine.

## Available Examples

### Basic Examples

#### 1. Simple Game (`examples/simple_game.py`)
A basic game with a player that can move around and collect enemies.

**Features:**
- Player movement with WASD/arrow keys
- Enemy AI with random movement
- Collision detection
- Scoring system

**How to run:**
```bash
python examples/simple_game.py
```

#### 2. Platformer Game (`examples/platformer_game.py`)
A platformer game with physics, jumping, and collectibles.

**Features:**
- Physics-based movement
- Jumping mechanics
- Platform collision
- Collectible coins
- Gravity system

**How to run:**
```bash
python examples/platformer_game.py
```

#### 3. Space Shooter (`examples/space_shooter.py`)
A space shooting game with enemies and projectiles.

**Features:**
- Player ship movement
- Shooting mechanics
- Enemy spawning
- Projectile physics
- Starfield background

**How to run:**
```bash
python examples/space_shooter.py
```

### Simplified Examples

#### 4. Simple Platformer (`platformer_simple.py`)
A simplified version of the platformer game.

**Features:**
- Basic platformer mechanics
- Simplified physics
- Easy to understand code

**How to run:**
```bash
python platformer_simple.py
```

#### 5. Simple Space Shooter (`space_shooter_simple.py`)
A simplified version of the space shooter game.

**Features:**
- Basic shooting mechanics
- Enemy spawning
- Simplified code structure

**How to run:**
```bash
python space_shooter_simple.py
```

## Code Snippets

### Basic Game Setup

```python
from py2d_game import Py2DEngine, GameObject, Scene, Sprite, Color, Vector2

# Create game engine
engine = Py2DEngine(800, 600, "My Game")

# Create scene
scene = Scene("Main Game")
scene.background_color = Color(50, 50, 100)

# Create player
class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite(width=32, height=32, color=Color(0, 255, 0))
        self.speed = 200
    
    def update(self, delta_time):
        super().update(delta_time)
        # Add movement logic here

# Add player to scene
player = Player(400, 300)
scene.add_object(player)

# Run game
engine.add_scene(scene)
engine.set_scene("Main Game")
engine.run()
```

### Input Handling

```python
class Player(GameObject):
    def update(self, delta_time):
        super().update(delta_time)
        
        input_manager = self.scene.game_engine.input_manager
        
        # Check for key presses
        if input_manager.is_key_pressed('left'):
            self.position.x -= self.speed * delta_time
        if input_manager.is_key_pressed('right'):
            self.position.x += self.speed * delta_time
        
        # Get movement vector
        movement = input_manager.get_movement_vector()
        self.position += movement * self.speed * delta_time
```

### Collision Detection

```python
class Player(GameObject):
    def update(self, delta_time):
        super().update(delta_time)
        
        # Check collisions with other objects
        for obj in self.scene.game_objects:
            if isinstance(obj, Enemy):
                distance = self.position.distance_to(obj.position)
                if distance < 30:  # Collision distance
                    # Handle collision
                    obj.visible = False
```

### Physics Integration

```python
from py2d_game import Physics2D, RigidBody2D, Collider2D

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite(width=32, height=32, color=Color(0, 255, 0))
        self.rigid_body = RigidBody2D(mass=1.0, gravity_scale=1.0)
        self.collider = Collider2D(32, 32)
        self.collider.game_object = self
        self.speed = 300
        self.jump_force = 400
    
    def update(self, delta_time):
        super().update(delta_time)
        
        input_manager = self.scene.game_engine.input_manager
        
        # Handle input
        if input_manager.is_key_pressed('left'):
            self.rigid_body.velocity.x = -self.speed
        elif input_manager.is_key_pressed('right'):
            self.rigid_body.velocity.x = self.speed
        
        if input_manager.is_key_just_pressed('space'):
            self.rigid_body.velocity.y = -self.jump_force
        
        # Update position
        self.position += self.rigid_body.velocity * delta_time

# Set up physics
physics = Physics2D(Vector2(0, 500))  # Gravity
physics.add_rigid_body(player.rigid_body)
physics.add_collider(player.collider)
```

### Audio Integration

```python
class Game:
    def __init__(self):
        self.engine = Py2DEngine(800, 600, "My Game")
        self.audio_manager = self.engine.audio_manager
        
        # Load sounds
        self.audio_manager.load_sound("jump", "sounds/jump.wav")
        self.audio_manager.load_sound("collect", "sounds/collect.wav")
        self.audio_manager.load_music("background.mp3")
        
        # Play background music
        self.audio_manager.play_music(loop=-1)
    
    def play_jump_sound(self):
        self.audio_manager.play_sound("jump")
    
    def play_collect_sound(self):
        self.audio_manager.play_sound("collect")
```

### UI Elements

```python
from py2d_game import Button, Label, Panel, Color

class GameUI:
    def __init__(self):
        self.panel = Panel(10, 10, 200, 100, Color(0, 0, 0, 128))
        self.score_label = Label(20, 20, "Score: 0", 16, Color(255, 255, 255))
        self.start_button = Button(20, 50, 100, 30, "Start Game")
        
        # Add elements to panel
        self.panel.add_child(self.score_label)
        self.panel.add_child(self.start_button)
        
        # Set button callback
        self.start_button.set_on_click(self.start_game)
    
    def start_game(self):
        print("Game started!")
    
    def update_score(self, score):
        self.score_label.set_text(f"Score: {score}")
```

## Running Examples

### Prerequisites

Make sure you have Py2D Game Engine installed:

```bash
pip install py2d-game
```

### Running Individual Examples

```bash
# Basic examples
python examples/simple_game.py
python examples/platformer_game.py
python examples/space_shooter.py

# Simplified examples
python platformer_simple.py
python space_shooter_simple.py
```

### Controls

Most examples use these controls:

- **WASD** or **Arrow Keys**: Move player
- **Space**: Jump (in platformer) or Shoot (in shooter)
- **ESC**: Exit game

## Modifying Examples

Feel free to modify the examples to learn and experiment:

1. **Change colors**: Modify the `Color` values in sprite creation
2. **Adjust speed**: Change the `speed` values for different movement
3. **Add features**: Try adding new game mechanics
4. **Modify physics**: Adjust gravity, mass, and other physics properties
5. **Change input**: Add new key bindings or mouse controls

## Learning from Examples

Each example demonstrates different concepts:

- **Simple Game**: Basic game loop, input handling, collision detection
- **Platformer**: Physics integration, jumping mechanics, level design
- **Space Shooter**: Projectile systems, enemy AI, game progression

Study the code to understand how these concepts are implemented and how you can apply them to your own games.

## Need Help?

If you have questions about the examples:

1. Check the [API Reference](../api_reference.md) for detailed documentation
2. Look at the [Troubleshooting](../troubleshooting.md) guide for common issues
3. Contact support: support@py2d-game.com
4. Open an issue on [GitHub](https://github.com/En-Hussain/py2d-game/issues)

## Contributing Examples

Want to contribute an example? We'd love your help! Please see our [Contributing Guide](../../CONTRIBUTING.md) for details.

Happy coding! 🎮