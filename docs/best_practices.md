# Best Practices

This guide covers best practices for developing games with Py2D Game Engine.

## Code Organization

### Project Structure

Organize your project with a clear structure:

```
my_game/
├── main.py              # Entry point
├── game/                # Game logic
│   ├── __init__.py
│   ├── player.py        # Player class
│   ├── enemy.py         # Enemy classes
│   ├── level.py         # Level management
│   └── ui.py            # UI elements
├── assets/              # Game assets
│   ├── images/
│   ├── sounds/
│   └── fonts/
├── config/              # Configuration
│   └── settings.py
└── tests/               # Unit tests
    └── test_game.py
```

### Class Design

Keep classes focused and single-purpose:

```python
# Good: Single responsibility
class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite(width=32, height=32, color=Color(0, 255, 0))
        self.speed = 200
        self.health = 100
    
    def update(self, delta_time):
        super().update(delta_time)
        self.handle_input(delta_time)
        self.update_health()
    
    def handle_input(self, delta_time):
        # Input handling logic
        pass
    
    def update_health(self):
        # Health update logic
        pass

# Bad: Multiple responsibilities
class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite(width=32, height=32, color=Color(0, 255, 0))
        self.speed = 200
        self.health = 100
        self.enemies = []
        self.ui_elements = []
        self.sound_manager = SoundManager()
    
    def update(self, delta_time):
        super().update(delta_time)
        # Too many responsibilities in one class
        self.handle_input(delta_time)
        self.update_health()
        self.update_enemies(delta_time)
        self.update_ui(delta_time)
        self.update_sounds(delta_time)
```

## Performance Optimization

### Object Pooling

Reuse objects instead of creating new ones:

```python
class BulletPool:
    def __init__(self, max_bullets=100):
        self.bullets = []
        self.max_bullets = max_bullets
        self.active_bullets = []
    
    def get_bullet(self):
        if self.bullets:
            bullet = self.bullets.pop()
            bullet.active = True
            bullet.visible = True
        else:
            bullet = Bullet(0, 0)
        
        self.active_bullets.append(bullet)
        return bullet
    
    def return_bullet(self, bullet):
        if bullet in self.active_bullets:
            self.active_bullets.remove(bullet)
            bullet.active = False
            bullet.visible = False
            if len(self.bullets) < self.max_bullets:
                self.bullets.append(bullet)
```

### Efficient Rendering

Only render what's visible:

```python
class OptimizedSprite(Sprite):
    def render(self, screen, position, rotation=0, scale=None, camera=None):
        if not self.visible:
            return
        
        # Cull objects outside camera view
        if camera:
            screen_pos = camera.world_to_screen(position)
            if (screen_pos.x < -100 or screen_pos.x > screen.get_width() + 100 or
                screen_pos.y < -100 or screen_pos.y > screen.get_height() + 100):
                return
        
        super().render(screen, position, rotation, scale, camera)
```

### Memory Management

Clean up unused resources:

```python
class ResourceManager:
    def __init__(self):
        self.sounds = {}
        self.images = {}
        self.fonts = {}
    
    def load_sound(self, name, path):
        if name not in self.sounds:
            self.sounds[name] = pygame.mixer.Sound(path)
        return self.sounds[name]
    
    def unload_sound(self, name):
        if name in self.sounds:
            del self.sounds[name]
    
    def cleanup(self):
        self.sounds.clear()
        self.images.clear()
        self.fonts.clear()
```

## Input Handling

### Centralized Input

Create a centralized input system:

```python
class InputSystem:
    def __init__(self, input_manager):
        self.input_manager = input_manager
        self.actions = {}
        self.bindings = {
            'move_left': ['left', 'a'],
            'move_right': ['right', 'd'],
            'move_up': ['up', 'w'],
            'move_down': ['down', 's'],
            'jump': ['space'],
            'shoot': ['space', 'left_click'],
        }
    
    def is_action_pressed(self, action):
        if action not in self.bindings:
            return False
        
        for binding in self.bindings[action]:
            if binding in ['left_click', 'right_click', 'middle_click']:
                button = {'left_click': 0, 'right_click': 1, 'middle_click': 2}[binding]
                if self.input_manager.is_mouse_button_pressed(button):
                    return True
            else:
                if self.input_manager.is_key_pressed(binding):
                    return True
        
        return False
    
    def get_movement_vector(self):
        movement = Vector2(0, 0)
        
        if self.is_action_pressed('move_left'):
            movement.x -= 1
        if self.is_action_pressed('move_right'):
            movement.x += 1
        if self.is_action_pressed('move_up'):
            movement.y -= 1
        if self.is_action_pressed('move_down'):
            movement.y += 1
        
        return movement.normalized() if movement.magnitude() > 0 else Vector2(0, 0)
```

## State Management

### Game States

Implement a state machine for game states:

```python
class GameState:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

class StateManager:
    def __init__(self):
        self.current_state = GameState.MENU
        self.states = {}
        self.transitions = {}
    
    def add_state(self, state_name, state_class):
        self.states[state_name] = state_class()
    
    def change_state(self, new_state):
        if new_state in self.states:
            if self.current_state in self.states:
                self.states[self.current_state].exit()
            
            self.current_state = new_state
            self.states[self.current_state].enter()
    
    def update(self, delta_time):
        if self.current_state in self.states:
            self.states[self.current_state].update(delta_time)
    
    def render(self, screen):
        if self.current_state in self.states:
            self.states[self.current_state].render(screen)
```

### Object States

Manage object states efficiently:

```python
class ObjectState:
    IDLE = "idle"
    MOVING = "moving"
    ATTACKING = "attacking"
    DEAD = "dead"

class StatefulObject(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.state = ObjectState.IDLE
        self.state_timer = 0
        self.state_duration = 0
    
    def change_state(self, new_state, duration=0):
        self.state = new_state
        self.state_timer = 0
        self.state_duration = duration
    
    def update(self, delta_time):
        super().update(delta_time)
        
        self.state_timer += delta_time
        
        if self.state_duration > 0 and self.state_timer >= self.state_duration:
            self.on_state_timeout()
        
        self.update_state(delta_time)
    
    def update_state(self, delta_time):
        if self.state == ObjectState.IDLE:
            self.update_idle(delta_time)
        elif self.state == ObjectState.MOVING:
            self.update_moving(delta_time)
        elif self.state == ObjectState.ATTACKING:
            self.update_attacking(delta_time)
        elif self.state == ObjectState.DEAD:
            self.update_dead(delta_time)
    
    def on_state_timeout(self):
        # Handle state timeout
        pass
```

## Error Handling

### Graceful Error Handling

Handle errors gracefully:

```python
class SafeGameObject(GameObject):
    def update(self, delta_time):
        try:
            super().update(delta_time)
            self.update_logic(delta_time)
        except Exception as e:
            print(f"Error updating {self.__class__.__name__}: {e}")
            # Handle error gracefully
    
    def update_logic(self, delta_time):
        # Game logic here
        pass
```

### Resource Loading

Handle resource loading errors:

```python
class SafeResourceLoader:
    @staticmethod
    def load_sound(name, path):
        try:
            return pygame.mixer.Sound(path)
        except pygame.error as e:
            print(f"Failed to load sound {name}: {e}")
            return None
    
    @staticmethod
    def load_image(name, path):
        try:
            return pygame.image.load(path)
        except pygame.error as e:
            print(f"Failed to load image {name}: {e}")
            return None
```

## Testing

### Unit Testing

Write tests for your game logic:

```python
import unittest
from py2d_game import GameObject, Vector2, Color

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(100, 200)
    
    def test_initialization(self):
        self.assertEqual(self.player.position.x, 100)
        self.assertEqual(self.player.position.y, 200)
        self.assertEqual(self.player.health, 100)
    
    def test_movement(self):
        initial_pos = self.player.position
        self.player.move(Vector2(10, 0))
        self.assertEqual(self.player.position.x, initial_pos.x + 10)
    
    def test_health_damage(self):
        initial_health = self.player.health
        self.player.take_damage(20)
        self.assertEqual(self.player.health, initial_health - 20)
```

### Integration Testing

Test game systems together:

```python
class TestGameIntegration(unittest.TestCase):
    def setUp(self):
        self.engine = Py2DEngine(800, 600, "Test Game")
        self.scene = Scene("Test Scene")
        self.engine.add_scene(self.scene)
    
    def test_player_enemy_collision(self):
        player = Player(100, 100)
        enemy = Enemy(100, 100)
        
        self.scene.add_object(player)
        self.scene.add_object(enemy)
        
        # Test collision detection
        self.assertTrue(player.check_collision(enemy))
    
    def test_scene_management(self):
        self.engine.set_scene("Test Scene")
        self.assertEqual(self.engine.current_scene.name, "Test Scene")
```

## Configuration

### Settings Management

Create a configuration system:

```python
class GameSettings:
    def __init__(self):
        self.window_width = 800
        self.window_height = 600
        self.window_title = "My Game"
        self.fps = 60
        self.volume = 0.7
        self.fullscreen = False
    
    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.window_width = data.get('window_width', self.window_width)
                self.window_height = data.get('window_height', self.window_height)
                self.window_title = data.get('window_title', self.window_title)
                self.fps = data.get('fps', self.fps)
                self.volume = data.get('volume', self.volume)
                self.fullscreen = data.get('fullscreen', self.fullscreen)
        except FileNotFoundError:
            print(f"Settings file {filename} not found, using defaults")
        except json.JSONDecodeError:
            print(f"Invalid JSON in settings file {filename}")
    
    def save_to_file(self, filename):
        data = {
            'window_width': self.window_width,
            'window_height': self.window_height,
            'window_title': self.window_title,
            'fps': self.fps,
            'volume': self.volume,
            'fullscreen': self.fullscreen
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
```

## Documentation

### Code Documentation

Document your code clearly:

```python
class Player(GameObject):
    """
    Represents the player character in the game.
    
    The player can move around the screen, jump, and interact with other objects.
    It has health, can take damage, and can collect items.
    """
    
    def __init__(self, x, y):
        """
        Initialize the player.
        
        Args:
            x (float): Initial x position
            y (float): Initial y position
        """
        super().__init__(x, y)
        self.sprite = Sprite(width=32, height=32, color=Color(0, 255, 0))
        self.speed = 200
        self.health = 100
        self.max_health = 100
    
    def move(self, direction, delta_time):
        """
        Move the player in the given direction.
        
        Args:
            direction (Vector2): Direction to move (normalized)
            delta_time (float): Time since last frame
        """
        self.position += direction * self.speed * delta_time
    
    def take_damage(self, amount):
        """
        Reduce player health by the given amount.
        
        Args:
            amount (int): Amount of damage to take
        """
        self.health = max(0, self.health - amount)
```

## Conclusion

Following these best practices will help you create maintainable, performant, and reliable games with Py2D Game Engine. Remember to:

1. **Organize your code** with clear structure and single-purpose classes
2. **Optimize performance** with object pooling and efficient rendering
3. **Handle input** with a centralized system
4. **Manage state** with state machines
5. **Handle errors** gracefully
6. **Write tests** for your game logic
7. **Document your code** clearly
8. **Use configuration** for game settings

For more help, check out the [Troubleshooting](troubleshooting.md) guide or contact support at support@py2d-game.com.
