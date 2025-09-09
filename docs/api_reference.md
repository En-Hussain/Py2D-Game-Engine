# API Reference

This document provides a comprehensive reference for all classes and methods in Py2D Game Engine.

## Core Classes

### Py2DEngine

The main game engine class.

```python
engine = Py2DEngine(width=800, height=600, title="My Game")
```

#### Methods

- `add_scene(scene: Scene)` - Add a scene to the engine
- `set_scene(scene_name: str)` - Set the active scene
- `run()` - Start the game loop
- `quit()` - Stop the game loop

#### Properties

- `width: int` - Window width
- `height: int` - Window height
- `title: str` - Window title
- `fps: int` - Target frames per second
- `input_manager: InputManager` - Input manager instance
- `audio_manager: AudioManager` - Audio manager instance

### GameObject

Base class for all game entities.

```python
obj = GameObject(x=100, y=200)
```

#### Methods

- `update(delta_time: float)` - Update the object
- `render(screen, camera)` - Render the object
- `add_child(child: GameObject)` - Add a child object
- `remove_child(child: GameObject)` - Remove a child object
- `get_world_position() -> Vector2` - Get world position

#### Properties

- `position: Vector2` - Object position
- `rotation: float` - Object rotation in degrees
- `scale: Vector2` - Object scale
- `visible: bool` - Object visibility
- `active: bool` - Object activity
- `sprite: Sprite` - Object sprite
- `children: List[GameObject]` - Child objects
- `parent: GameObject` - Parent object

### Scene

Represents a game level or screen.

```python
scene = Scene("Level 1")
```

#### Methods

- `add_object(obj: GameObject)` - Add an object to the scene
- `remove_object(obj: GameObject)` - Remove an object from the scene
- `get_objects_by_name(name: str) -> List[GameObject]` - Get objects by name
- `update(delta_time: float)` - Update the scene
- `render(screen)` - Render the scene

#### Properties

- `name: str` - Scene name
- `game_objects: List[GameObject]` - Scene objects
- `camera: Camera` - Scene camera
- `background_color: Color` - Background color

### Camera

Manages the viewport and transformations.

```python
camera = Camera(x=0, y=0, zoom=1.0)
```

#### Methods

- `world_to_screen(world_pos: Vector2) -> Vector2` - Convert world to screen coordinates
- `screen_to_world(screen_pos: Vector2) -> Vector2` - Convert screen to world coordinates

#### Properties

- `position: Vector2` - Camera position
- `zoom: float` - Camera zoom level
- `rotation: float` - Camera rotation in degrees

## Graphics System

### Sprite

Represents visual elements in the game.

```python
sprite = Sprite(image_path="player.png", width=32, height=32)
```

#### Methods

- `load_image(image_path: str)` - Load image from file
- `create_colored_surface()` - Create colored surface
- `render(screen, position, rotation, scale, camera)` - Render the sprite

#### Properties

- `image: pygame.Surface` - Sprite image
- `width: int` - Sprite width
- `height: int` - Sprite height
- `color: Color` - Sprite color

### Animation

Manages sprite animations.

```python
animation = Animation(frames, frame_duration=0.1)
```

#### Methods

- `play()` - Start animation
- `stop()` - Stop animation
- `pause()` - Pause animation
- `update(delta_time: float)` - Update animation
- `get_current_frame() -> pygame.Surface` - Get current frame

#### Properties

- `frames: List[pygame.Surface]` - Animation frames
- `frame_duration: float` - Duration per frame
- `current_frame: int` - Current frame index
- `is_playing: bool` - Animation playing state
- `loop: bool` - Loop animation

### Text

Renders text on screen.

```python
text = Text("Hello World", font_size=24, color=Color(255, 255, 255))
```

#### Methods

- `set_text(text: str)` - Set text content
- `set_color(color: Color)` - Set text color
- `set_font_size(size: int)` - Set font size
- `update_surface()` - Update text surface
- `render(screen, position, camera)` - Render text

#### Properties

- `text: str` - Text content
- `font_size: int` - Font size
- `color: Color` - Text color
- `font: pygame.font.Font` - Font object
- `surface: pygame.Surface` - Text surface

### Shape

Draws geometric shapes.

```python
shape = Shape("rectangle", width=100, height=50, color=Color(255, 0, 0))
```

#### Methods

- `create_surface()` - Create shape surface
- `render(screen, position, rotation, scale, camera)` - Render shape

#### Properties

- `shape_type: str` - Shape type ("rectangle", "circle", "ellipse")
- `width: int` - Shape width
- `height: int` - Shape height
- `color: Color` - Shape color
- `surface: pygame.Surface` - Shape surface

### TileMap

Manages tile-based maps.

```python
tilemap = TileMap(tile_width=32, tile_height=32, map_width=20, map_height=15)
```

#### Methods

- `set_tile(x: int, y: int, tile_id: int)` - Set tile at position
- `get_tile(x: int, y: int) -> int` - Get tile at position
- `add_tile_sprite(tile_id: int, sprite: Sprite)` - Add tile sprite
- `render(screen, camera, offset)` - Render tilemap

#### Properties

- `tile_width: int` - Tile width
- `tile_height: int` - Tile height
- `map_width: int` - Map width in tiles
- `map_height: int` - Map height in tiles
- `tiles: dict` - Tile data
- `tile_sprites: dict` - Tile sprites

## Physics System

### Physics2D

Main physics engine.

```python
physics = Physics2D(gravity=Vector2(0, 500))
```

#### Methods

- `add_rigid_body(rigid_body: RigidBody2D)` - Add rigid body
- `remove_rigid_body(rigid_body: RigidBody2D)` - Remove rigid body
- `add_collider(collider: Collider2D)` - Add collider
- `remove_collider(collider: Collider2D)` - Remove collider
- `add_collision_callback(callback: Callable)` - Add collision callback
- `update(delta_time: float, game_objects: List)` - Update physics
- `check_collisions(game_objects: List)` - Check collisions

#### Properties

- `gravity: Vector2` - Gravity vector
- `rigid_bodies: List[RigidBody2D]` - Rigid bodies
- `colliders: List[Collider2D]` - Colliders
- `collision_callbacks: List[Callable]` - Collision callbacks

### RigidBody2D

Represents a physics body.

```python
rigid_body = RigidBody2D(mass=1.0, gravity_scale=1.0)
```

#### Methods

- `add_force(force: Vector2)` - Add force
- `add_impulse(impulse: Vector2)` - Add impulse
- `set_velocity(velocity: Vector2)` - Set velocity
- `set_angular_velocity(angular_velocity: float)` - Set angular velocity

#### Properties

- `mass: float` - Body mass
- `velocity: Vector2` - Body velocity
- `angular_velocity: float` - Angular velocity
- `gravity_scale: float` - Gravity scale
- `drag: float` - Linear drag
- `angular_drag: float` - Angular drag
- `is_kinematic: bool` - Kinematic state
- `freeze_position_x: bool` - Freeze X position
- `freeze_position_y: bool` - Freeze Y position
- `freeze_rotation: bool` - Freeze rotation

### Collider2D

Represents a collision shape.

```python
collider = Collider2D(width=32, height=32, is_trigger=False)
```

#### Methods

- `get_bounds(position: Vector2) -> pygame.Rect` - Get collision bounds
- `check_collision(other: Collider2D, pos1: Vector2, pos2: Vector2) -> bool` - Check collision
- `get_collision_normal(other: Collider2D, pos1: Vector2, pos2: Vector2) -> Vector2` - Get collision normal

#### Properties

- `width: float` - Collider width
- `height: float` - Collider height
- `is_trigger: bool` - Trigger state
- `offset: Vector2` - Collider offset
- `game_object: GameObject` - Associated game object

## Input System

### InputManager

Manages keyboard and mouse input.

```python
input_manager = engine.input_manager
```

#### Methods

- `update()` - Update input state
- `is_key_pressed(key)` - Check if key is pressed
- `is_key_just_pressed(key)` - Check if key was just pressed
- `is_key_just_released(key)` - Check if key was just released
- `is_mouse_button_pressed(button: int)` - Check if mouse button is pressed
- `is_mouse_button_just_pressed(button: int)` - Check if mouse button was just pressed
- `is_mouse_button_just_released(button: int)` - Check if mouse button was just released
- `get_mouse_position() -> Vector2` - Get mouse position
- `get_mouse_delta() -> Vector2` - Get mouse movement delta
- `get_mouse_wheel() -> int` - Get mouse wheel delta
- `get_movement_vector() -> Vector2` - Get movement vector

#### Properties

- `keys_pressed: Set[int]` - Currently pressed keys
- `keys_just_pressed: Set[int]` - Keys pressed this frame
- `keys_just_released: Set[int]` - Keys released this frame
- `mouse_buttons_pressed: Set[int]` - Currently pressed mouse buttons
- `mouse_buttons_just_pressed: Set[int]` - Mouse buttons pressed this frame
- `mouse_buttons_just_released: Set[int]` - Mouse buttons released this frame
- `mouse_position: Vector2` - Mouse position
- `mouse_delta: Vector2` - Mouse movement delta
- `mouse_wheel: int` - Mouse wheel delta

## Audio System

### AudioManager

Manages sound and music.

```python
audio_manager = engine.audio_manager
```

#### Methods

- `load_sound(name: str, file_path: str)` - Load sound effect
- `play_sound(name: str, volume: float = 1.0)` - Play sound effect
- `stop_sound(name: str)` - Stop sound effect
- `stop_all_sounds()` - Stop all sounds
- `load_music(file_path: str)` - Load music
- `play_music(loop: int = -1, fade_in: int = 0)` - Play music
- `stop_music(fade_out: int = 0)` - Stop music
- `pause_music()` - Pause music
- `unpause_music()` - Unpause music
- `set_music_volume(volume: float)` - Set music volume
- `set_sound_volume(volume: float)` - Set sound volume
- `is_music_playing() -> bool` - Check if music is playing
- `get_music_volume() -> float` - Get music volume
- `get_sound_volume() -> float` - Get sound volume

#### Properties

- `sounds: Dict[str, pygame.mixer.Sound]` - Loaded sounds
- `music_volume: float` - Music volume
- `sound_volume: float` - Sound volume

## Utility Classes

### Vector2

Represents a 2D vector.

```python
vec = Vector2(x=100, y=200)
```

#### Methods

- `magnitude() -> float` - Get vector magnitude
- `normalized() -> Vector2` - Get normalized vector
- `rotate(angle_degrees: float) -> Vector2` - Rotate vector
- `dot(other: Vector2) -> float` - Dot product
- `distance_to(other: Vector2) -> float` - Distance to other vector
- `to_tuple() -> Tuple[float, float]` - Convert to tuple

#### Properties

- `x: float` - X component
- `y: float` - Y component

### Color

Represents a color.

```python
color = Color(r=255, g=0, b=0, a=255)
```

#### Methods

- `lerp(other: Color, t: float) -> Color` - Linear interpolation

#### Properties

- `r: int` - Red component
- `g: int` - Green component
- `b: int` - Blue component
- `a: int` - Alpha component
- `rgba: Tuple[int, int, int, int]` - RGBA tuple
- `rgb: Tuple[int, int, int]` - RGB tuple

### Timer

Manages timed events.

```python
timer = Timer(duration=5.0)
```

#### Methods

- `start()` - Start timer
- `stop()` - Stop timer
- `reset()` - Reset timer
- `update(delta_time: float)` - Update timer

#### Properties

- `duration: float` - Timer duration
- `current_time: float` - Current time
- `is_finished: bool` - Timer finished state
- `is_running: bool` - Timer running state

### Math2D

Static math utilities.

```python
result = Math2D.lerp(0, 100, 0.5)  # 50
```

#### Static Methods

- `lerp(a: float, b: float, t: float) -> float` - Linear interpolation
- `clamp(value: float, min_val: float, max_val: float) -> float` - Clamp value
- `angle_between_vectors(v1: Vector2, v2: Vector2) -> float` - Angle between vectors
- `distance_point_to_line(point: Vector2, line_start: Vector2, line_end: Vector2) -> float` - Distance from point to line

## UI System

### UIElement

Base class for UI elements.

```python
element = UIElement(x=100, y=100, width=200, height=50)
```

#### Methods

- `add_child(child: UIElement)` - Add child element
- `remove_child(child: UIElement)` - Remove child element
- `get_world_position() -> Vector2` - Get world position
- `contains_point(point: Vector2) -> bool` - Check if point is inside
- `update(delta_time: float)` - Update element
- `render(screen)` - Render element

#### Properties

- `position: Vector2` - Element position
- `size: Vector2` - Element size
- `visible: bool` - Element visibility
- `active: bool` - Element activity
- `parent: UIElement` - Parent element
- `children: List[UIElement]` - Child elements

### Button

Interactive button element.

```python
button = Button(x=100, y=100, width=200, height=50, text="Click Me")
```

#### Methods

- `set_text(text: str)` - Set button text
- `set_on_click(callback: Callable)` - Set click callback
- `handle_mouse_input(mouse_pos: Vector2, mouse_pressed: bool)` - Handle mouse input

#### Properties

- `text: Text` - Button text
- `background_color: Color` - Background color
- `hover_color: Color` - Hover color
- `pressed_color: Color` - Pressed color
- `border_color: Color` - Border color
- `border_width: int` - Border width
- `is_hovered: bool` - Hover state
- `is_pressed: bool` - Pressed state
- `on_click: Callable` - Click callback

### Label

Text label element.

```python
label = Label(x=100, y=100, text="Hello World", font_size=16)
```

#### Methods

- `set_text(text: str)` - Set label text
- `set_color(color: Color)` - Set text color
- `set_font_size(size: int)` - Set font size
- `update_size()` - Update label size

#### Properties

- `text: Text` - Label text
- `color: Color` - Text color
- `font_size: int` - Font size

### Panel

Container panel element.

```python
panel = Panel(x=100, y=100, width=300, height=200, background_color=Color(50, 50, 50))
```

#### Properties

- `background_color: Color` - Background color
- `border_color: Color` - Border color
- `border_width: int` - Border width
