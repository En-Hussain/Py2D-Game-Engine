# Troubleshooting

This guide helps you resolve common issues with Py2D Game Engine.

## Common Issues

### Installation Issues

#### "ModuleNotFoundError: No module named 'py2d_game'"

**Solution:**
```bash
pip install py2d-game
```

If you're using a virtual environment, make sure it's activated:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### "pygame not found" error

**Solution:**
```bash
pip install pygame>=2.0.0
```

### Runtime Issues

#### Game window doesn't appear

**Possible causes:**
1. Display issues
2. pygame initialization problems
3. Graphics driver issues

**Solutions:**
1. Check if you have a display available
2. Try running in headless mode for testing
3. Update your graphics drivers
4. Check pygame installation

#### "TypeError: unsupported operand type(s) for -: 'tuple' and 'int'"

This error occurs when there's a type mismatch in vector operations.

**Solution:**
Make sure you're using Vector2 objects for position calculations:
```python
# Correct
position = Vector2(100, 200)
position += Vector2(10, 0)

# Incorrect
position = (100, 200)  # This is a tuple
position += Vector2(10, 0)  # This will cause the error
```

#### Game objects not moving

**Possible causes:**
1. Input not being processed
2. Objects not being added to scene
3. Update method not being called

**Solutions:**
1. Check if input manager is being updated
2. Ensure objects are added to the scene
3. Make sure the update method is being called

#### Performance issues

**Solutions:**
1. Reduce the number of objects
2. Use object pooling
3. Optimize rendering
4. Check for memory leaks

### Input Issues

#### Keys not responding

**Solutions:**
1. Check if the window has focus
2. Verify key mappings
3. Ensure input manager is being updated

#### Mouse input not working

**Solutions:**
1. Check mouse button numbers (0=left, 1=right, 2=middle)
2. Verify mouse position calculations
3. Ensure mouse events are being processed

### Graphics Issues

#### Sprites not appearing

**Solutions:**
1. Check sprite visibility
2. Verify sprite position
3. Ensure sprite is being rendered
4. Check camera settings

#### Text not displaying

**Solutions:**
1. Check font loading
2. Verify text color
3. Ensure text is being rendered
4. Check text position

### Physics Issues

#### Collisions not working

**Solutions:**
1. Check collider setup
2. Verify collision callbacks
3. Ensure physics is being updated
4. Check collider positions

#### Objects falling through ground

**Solutions:**
1. Check collider sizes
2. Verify collision detection
3. Ensure physics is being updated
4. Check object positions

### Audio Issues

#### Sounds not playing

**Solutions:**
1. Check audio file format
2. Verify audio file path
3. Ensure audio is being loaded
4. Check volume settings

#### Music not playing

**Solutions:**
1. Check music file format
2. Verify music file path
3. Ensure music is being loaded
4. Check music volume

## Debugging Tips

### Enable Debug Mode

Add debug prints to your code:
```python
def update(self, delta_time):
    print(f"Position: {self.position}")
    print(f"Velocity: {self.velocity}")
    super().update(delta_time)
```

### Check Object States

```python
def update(self, delta_time):
    if not self.active:
        print("Object is not active")
        return
    
    if not self.visible:
        print("Object is not visible")
        return
    
    super().update(delta_time)
```

### Monitor Performance

```python
import time

class PerformanceMonitor:
    def __init__(self):
        self.last_time = time.time()
        self.frame_count = 0
    
    def update(self):
        current_time = time.time()
        self.frame_count += 1
        
        if current_time - self.last_time >= 1.0:
            fps = self.frame_count / (current_time - self.last_time)
            print(f"FPS: {fps}")
            self.frame_count = 0
            self.last_time = current_time
```

## Getting Help

If you're still having issues:

1. **Check the documentation**: Look at the [API Reference](api_reference.md)
2. **Search existing issues**: Check [GitHub Issues](https://github.com/En-Hussain/py2d-game/issues)
3. **Create a new issue**: Provide detailed information about your problem
4. **Contact support**: Email support@py2d-game.com

### When Reporting Issues

Please include:

1. **Python version**: `python --version`
2. **Py2D Game version**: `import py2d_game; print(py2d_game.__version__)`
3. **Operating system**: Windows, macOS, or Linux
4. **Error message**: Full error traceback
5. **Code**: Minimal code that reproduces the issue
6. **Expected behavior**: What you expected to happen
7. **Actual behavior**: What actually happened

### Example Issue Report

```
**Environment:**
- Python 3.9.7
- Py2D Game 1.0.0
- Windows 10
- pygame 2.1.0

**Error:**
```
TypeError: unsupported operand type(s) for -: 'tuple' and 'int'
```

**Code:**
```python
from py2d_game import Py2DEngine, GameObject, Vector2

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.position = (x, y)  # This should be Vector2(x, y)

player = Player(100, 200)
```

**Expected:** Player should be created at position (100, 200)
**Actual:** TypeError when trying to use position in calculations
```

## Performance Optimization

### Reduce Object Count

Instead of creating many objects, reuse them:
```python
class ObjectPool:
    def __init__(self, object_class, max_size=100):
        self.objects = []
        self.max_size = max_size
        self.object_class = object_class
    
    def get_object(self):
        if self.objects:
            return self.objects.pop()
        return self.object_class()
    
    def return_object(self, obj):
        if len(self.objects) < self.max_size:
            self.objects.append(obj)
```

### Optimize Rendering

Only render visible objects:
```python
def render(self, screen, camera):
    if not self.visible:
        return
    
    # Check if object is in camera view
    screen_pos = camera.world_to_screen(self.position)
    if (screen_pos.x < -100 or screen_pos.x > screen.get_width() + 100 or
        screen_pos.y < -100 or screen_pos.y > screen.get_height() + 100):
        return
    
    # Render object
    super().render(screen, camera)
```

### Memory Management

Clean up unused objects:
```python
def update(self, delta_time):
    super().update(delta_time)
    
    # Remove objects that are off-screen
    if self.position.y > 1000:
        self.scene.remove_object(self)
```

## Common Patterns

### Game State Management

```python
class GameState:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

class Game:
    def __init__(self):
        self.state = GameState.MENU
        self.engine = Py2DEngine(800, 600, "My Game")
    
    def update(self, delta_time):
        if self.state == GameState.PLAYING:
            # Update game logic
            pass
        elif self.state == GameState.PAUSED:
            # Handle pause logic
            pass
```

### Event Handling

```python
class EventHandler:
    def __init__(self):
        self.events = []
    
    def add_event(self, event):
        self.events.append(event)
    
    def process_events(self):
        for event in self.events:
            event.execute()
        self.events.clear()
```

### Resource Management

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
    
    def load_image(self, name, path):
        if name not in self.images:
            self.images[name] = pygame.image.load(path)
        return self.images[name]
```

Remember: If you're still having trouble, don't hesitate to reach out for help!
