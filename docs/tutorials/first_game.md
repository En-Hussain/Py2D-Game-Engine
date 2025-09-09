# Your First Game

This tutorial will guide you through creating your first game with Py2D Game Engine. You'll learn the basics of the engine and create a simple game where a player can move around the screen.

## What You'll Learn

- How to set up a basic game project
- How to create a game engine and scene
- How to create a player object
- How to handle input for movement
- How to run your game

## Prerequisites

- Python 3.7 or higher
- Py2D Game Engine installed (`pip install py2d-game`)
- Basic Python knowledge

## Step 1: Project Setup

Create a new directory for your game:

```bash
mkdir my_first_game
cd my_first_game
```

Create a new Python file called `main.py`:

```python
from py2d_game import Py2DEngine, GameObject, Scene, Sprite, Color, Vector2

def main():
    print("Starting My First Game...")
    
    # Create the game engine
    engine = Py2DEngine(800, 600, "My First Game")
    
    # Create a scene
    scene = Scene("Main Game")
    scene.background_color = Color(50, 50, 100)
    
    # Add scene to engine and run
    engine.add_scene(scene)
    engine.set_scene("Main Game")
    engine.run()

if __name__ == "__main__":
    main()
```

Run your game:

```bash
python main.py
```

You should see a window with a blue background. Press ESC or close the window to exit.

## Step 2: Create a Player

Now let's add a player that can move around the screen. Update your `main.py`:

```python
from py2d_game import Py2DEngine, GameObject, Scene, Sprite, Color, Vector2

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        # Create a green square for the player
        self.sprite = Sprite(width=32, height=32, color=Color(0, 255, 0))
        self.speed = 200  # pixels per second
    
    def update(self, delta_time):
        super().update(delta_time)
        
        # Get input from the input manager
        input_manager = self.scene.game_engine.input_manager
        movement = input_manager.get_movement_vector()
        
        # Move the player
        self.position += movement * self.speed * delta_time
        
        # Keep player on screen
        if self.position.x < 16:
            self.position.x = 16
        elif self.position.x > 784:
            self.position.x = 784
            
        if self.position.y < 16:
            self.position.y = 16
        elif self.position.y > 584:
            self.position.y = 584

def main():
    print("Starting My First Game...")
    print("Use WASD or arrow keys to move")
    print("Press ESC to exit")
    
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

Run your game again:

```bash
python main.py
```

Now you should see a green square that you can move around using WASD keys or arrow keys!

## Step 3: Add Some Enemies

Let's add some enemies that move around the screen:

```python
from py2d_game import Py2DEngine, GameObject, Scene, Sprite, Color, Vector2
import random

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
        
        # Keep player on screen
        if self.position.x < 16:
            self.position.x = 16
        elif self.position.x > 784:
            self.position.x = 784
            
        if self.position.y < 16:
            self.position.y = 16
        elif self.position.y > 584:
            self.position.y = 584

class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite(width=24, height=24, color=Color(255, 0, 0))
        self.speed = random.uniform(50, 150)
        self.direction = Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.direction = self.direction.normalized()
    
    def update(self, delta_time):
        super().update(delta_time)
        
        # Move in random direction
        self.position += self.direction * self.speed * delta_time
        
        # Bounce off screen edges
        if self.position.x < 12 or self.position.x > 788:
            self.direction.x *= -1
        if self.position.y < 12 or self.position.y > 588:
            self.direction.y *= -1
        
        # Keep enemy on screen
        if self.position.x < 12:
            self.position.x = 12
        elif self.position.x > 788:
            self.position.x = 788
            
        if self.position.y < 12:
            self.position.y = 12
        elif self.position.y > 588:
            self.position.y = 588

def main():
    print("Starting My First Game...")
    print("Use WASD or arrow keys to move")
    print("Avoid the red enemies!")
    print("Press ESC to exit")
    
    # Create the game engine
    engine = Py2DEngine(800, 600, "My First Game")
    
    # Create a scene
    scene = Scene("Main Game")
    scene.background_color = Color(50, 50, 100)
    
    # Create a player
    player = Player(400, 300)
    scene.add_object(player)
    
    # Create some enemies
    for i in range(5):
        enemy = Enemy(
            random.uniform(100, 700),
            random.uniform(100, 500)
        )
        scene.add_object(enemy)
    
    # Add scene to engine and run
    engine.add_scene(scene)
    engine.set_scene("Main Game")
    engine.run()

if __name__ == "__main__":
    main()
```

Run your game:

```bash
python main.py
```

Now you have a game with a green player and red enemies moving around!

## Step 4: Add Collision Detection

Let's add collision detection so the player can "collect" enemies:

```python
from py2d_game import Py2DEngine, GameObject, Scene, Sprite, Color, Vector2
import random

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite(width=32, height=32, color=Color(0, 255, 0))
        self.speed = 200
        self.score = 0
    
    def update(self, delta_time):
        super().update(delta_time)
        
        input_manager = self.scene.game_engine.input_manager
        movement = input_manager.get_movement_vector()
        
        self.position += movement * self.speed * delta_time
        
        # Keep player on screen
        if self.position.x < 16:
            self.position.x = 16
        elif self.position.x > 784:
            self.position.x = 784
            
        if self.position.y < 16:
            self.position.y = 16
        elif self.position.y > 584:
            self.position.y = 584
        
        # Check for collisions with enemies
        for obj in self.scene.game_objects:
            if isinstance(obj, Enemy) and obj.visible:
                distance = self.position.distance_to(obj.position)
                if distance < 30:  # Collision distance
                    obj.visible = False
                    self.score += 1
                    print(f"Score: {self.score}")

class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite(width=24, height=24, color=Color(255, 0, 0))
        self.speed = random.uniform(50, 150)
        self.direction = Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.direction = self.direction.normalized()
    
    def update(self, delta_time):
        super().update(delta_time)
        
        if not self.visible:
            return
        
        # Move in random direction
        self.position += self.direction * self.speed * delta_time
        
        # Bounce off screen edges
        if self.position.x < 12 or self.position.x > 788:
            self.direction.x *= -1
        if self.position.y < 12 or self.position.y > 588:
            self.direction.y *= -1
        
        # Keep enemy on screen
        if self.position.x < 12:
            self.position.x = 12
        elif self.position.x > 788:
            self.position.x = 788
            
        if self.position.y < 12:
            self.position.y = 12
        elif self.position.y > 588:
            self.position.y = 588

def main():
    print("Starting My First Game...")
    print("Use WASD or arrow keys to move")
    print("Collect the red enemies to score points!")
    print("Press ESC to exit")
    
    # Create the game engine
    engine = Py2DEngine(800, 600, "My First Game")
    
    # Create a scene
    scene = Scene("Main Game")
    scene.background_color = Color(50, 50, 100)
    
    # Create a player
    player = Player(400, 300)
    scene.add_object(player)
    
    # Create some enemies
    for i in range(5):
        enemy = Enemy(
            random.uniform(100, 700),
            random.uniform(100, 500)
        )
        scene.add_object(enemy)
    
    # Add scene to engine and run
    engine.add_scene(scene)
    engine.set_scene("Main Game")
    engine.run()

if __name__ == "__main__":
    main()
```

Run your game:

```bash
python main.py
```

Now you can collect enemies by touching them, and your score will increase!

## Step 5: Add More Features

Let's add some final touches to make the game more interesting:

```python
from py2d_game import Py2DEngine, GameObject, Scene, Sprite, Color, Vector2, Text
import random

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite(width=32, height=32, color=Color(0, 255, 0))
        self.speed = 200
        self.score = 0
        self.lives = 3
    
    def update(self, delta_time):
        super().update(delta_time)
        
        input_manager = self.scene.game_engine.input_manager
        movement = input_manager.get_movement_vector()
        
        self.position += movement * self.speed * delta_time
        
        # Keep player on screen
        if self.position.x < 16:
            self.position.x = 16
        elif self.position.x > 784:
            self.position.x = 784
            
        if self.position.y < 16:
            self.position.y = 16
        elif self.position.y > 584:
            self.position.y = 584
        
        # Check for collisions with enemies
        for obj in self.scene.game_objects:
            if isinstance(obj, Enemy) and obj.visible:
                distance = self.position.distance_to(obj.position)
                if distance < 30:  # Collision distance
                    obj.visible = False
                    self.score += 1
                    print(f"Score: {self.score}")
        
        # Check for collisions with power-ups
        for obj in self.scene.game_objects:
            if isinstance(obj, PowerUp) and obj.visible:
                distance = self.position.distance_to(obj.position)
                if distance < 25:  # Collision distance
                    obj.visible = False
                    self.lives += 1
                    print(f"Lives: {self.lives}")

class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite(width=24, height=24, color=Color(255, 0, 0))
        self.speed = random.uniform(50, 150)
        self.direction = Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.direction = self.direction.normalized()
    
    def update(self, delta_time):
        super().update(delta_time)
        
        if not self.visible:
            return
        
        # Move in random direction
        self.position += self.direction * self.speed * delta_time
        
        # Bounce off screen edges
        if self.position.x < 12 or self.position.x > 788:
            self.direction.x *= -1
        if self.position.y < 12 or self.position.y > 588:
            self.direction.y *= -1
        
        # Keep enemy on screen
        if self.position.x < 12:
            self.position.x = 12
        elif self.position.x > 788:
            self.position.x = 788
            
        if self.position.y < 12:
            self.position.y = 12
        elif self.position.y > 588:
            self.position.y = 588

class PowerUp(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite(width=20, height=20, color=Color(255, 255, 0))
        self.speed = 50
        self.direction = Vector2(0, 1)  # Move down
    
    def update(self, delta_time):
        super().update(delta_time)
        
        if not self.visible:
            return
        
        # Move down
        self.position += self.direction * self.speed * delta_time
        
        # Remove if off screen
        if self.position.y > 600:
            self.visible = False

def main():
    print("Starting My First Game...")
    print("Use WASD or arrow keys to move")
    print("Collect red enemies to score points!")
    print("Collect yellow power-ups to gain lives!")
    print("Press ESC to exit")
    
    # Create the game engine
    engine = Py2DEngine(800, 600, "My First Game")
    
    # Create a scene
    scene = Scene("Main Game")
    scene.background_color = Color(50, 50, 100)
    
    # Create a player
    player = Player(400, 300)
    scene.add_object(player)
    
    # Create some enemies
    for i in range(5):
        enemy = Enemy(
            random.uniform(100, 700),
            random.uniform(100, 500)
        )
        scene.add_object(enemy)
    
    # Create some power-ups
    for i in range(3):
        powerup = PowerUp(
            random.uniform(100, 700),
            random.uniform(-100, -50)
        )
        scene.add_object(powerup)
    
    # Add scene to engine and run
    engine.add_scene(scene)
    engine.set_scene("Main Game")
    engine.run()

if __name__ == "__main__":
    main()
```

Run your final game:

```bash
python main.py
```

## Congratulations!

You've created your first game with Py2D Game Engine! Your game now has:

- A player that can move around
- Enemies that move randomly
- Power-ups that fall from the top
- Collision detection
- Scoring system
- Lives system

## What's Next?

Now that you've completed your first game, you can:

1. **Add more features**: Try adding sound effects, animations, or more game mechanics
2. **Learn more**: Check out the other tutorials to learn about graphics, physics, and more
3. **Experiment**: Try modifying the code to see what happens
4. **Build something new**: Use what you've learned to create your own game

## Key Concepts Learned

- **Game Engine**: The main engine that manages the game loop
- **Scene**: A container for game objects
- **GameObject**: The base class for all game entities
- **Sprite**: Visual representation of objects
- **Input**: Handling keyboard and mouse input
- **Collision Detection**: Checking when objects touch
- **Game Loop**: The main update and render cycle

## Troubleshooting

If you run into any issues:

1. Check the [Troubleshooting](../troubleshooting.md) guide
2. Make sure you have the latest version of Py2D Game Engine
3. Check your Python version (3.7+ required)
4. Contact support: support@py2d-game.com

Happy game development! 🎮
