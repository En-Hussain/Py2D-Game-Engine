from py2d_game import Py2DEngine, GameObject, Scene, Sprite, Color, Vector2, Physics2D, RigidBody2D, Collider2D, Text, Timer
import random
import math

class Platform(GameObject):
    def __init__(self, x, y, width, height, color=None):
        super().__init__(x, y)
        if color is None:
            color = Color(100, 50, 0)
        self.sprite = Sprite(width=width, height=height, color=color)
        self.collider = Collider2D(width, height)
        self.collider.game_object = self

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite(width=24, height=32, color=Color(0, 255, 0))
        self.rigid_body = RigidBody2D(mass=1.0, gravity_scale=1.5)
        self.collider = Collider2D(24, 32)
        self.collider.game_object = self
        self.speed = 300
        self.jump_force = 450
        self.on_ground = False
        self.score = 0
        self.lives = 3
        self.invulnerable = False
        self.invulnerability_timer = Timer(1.0)
        
    def update(self, delta_time):
        super().update(delta_time)
        
        # Update invulnerability timer
        if self.invulnerable:
            self.invulnerability_timer.update(delta_time)
            if self.invulnerability_timer.is_finished:
                self.invulnerable = False
                self.invulnerability_timer.reset()
        
        # Update sprite color based on invulnerability
        if self.invulnerable:
            self.sprite.color = Color(255, 255, 0)  # Yellow when invulnerable
        else:
            self.sprite.color = Color(0, 255, 0)  # Green when normal
        
        input_manager = self.scene.game_engine.input_manager
        
        if input_manager.is_key_pressed('left') or input_manager.is_key_pressed('a'):
            self.rigid_body.velocity.x = -self.speed
        elif input_manager.is_key_pressed('right') or input_manager.is_key_pressed('d'):
            self.rigid_body.velocity.x = self.speed
        else:
            self.rigid_body.velocity.x *= 0.8
            
        if (input_manager.is_key_just_pressed('space') or input_manager.is_key_just_pressed('w')) and self.on_ground:
            self.rigid_body.velocity.y = -self.jump_force
            self.on_ground = False
            
        self.position += self.rigid_body.velocity * delta_time
        
        # Keep player on screen horizontally
        if self.position.x < 12:
            self.position.x = 12
        elif self.position.x > 788:
            self.position.x = 788
            
        # Check if player fell off the screen (death)
        if self.position.y > 650:
            self.take_damage()
            self.position = Vector2(400, 400)  # Reset position
            self.rigid_body.velocity = Vector2(0, 0)
    
    def take_damage(self):
        if not self.invulnerable:
            self.lives -= 1
            self.invulnerable = True
            self.invulnerability_timer.start()
            print(f"Lives: {self.lives}")
            
            if self.lives <= 0:
                print("Game Over!")
                self.scene.game_engine.quit()
    
    def add_score(self, points):
        self.score += points
        print(f"Score: {self.score}")

class Coin(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite(width=16, height=16, color=Color(255, 255, 0))
        self.collider = Collider2D(16, 16, is_trigger=True)
        self.collider.game_object = self
        self.collected = False
        self.bob_timer = 0
        
    def update(self, delta_time):
        super().update(delta_time)
        if self.collected:
            self.visible = False
        else:
            # Bobbing animation
            self.bob_timer += delta_time
            self.position.y += math.sin(self.bob_timer * 5) * 0.5

class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite(width=20, height=20, color=Color(255, 0, 0))
        self.collider = Collider2D(20, 20)
        self.collider.game_object = self
        self.speed = 50
        self.direction = 1
        self.start_x = x
        
    def update(self, delta_time):
        super().update(delta_time)
        
        # Move back and forth
        self.position.x += self.direction * self.speed * delta_time
        
        # Reverse direction at edges
        if self.position.x > self.start_x + 100 or self.position.x < self.start_x - 100:
            self.direction *= -1

class PowerUp(GameObject):
    def __init__(self, x, y, power_type="jump"):
        super().__init__(x, y)
        self.power_type = power_type
        if power_type == "jump":
            self.sprite = Sprite(width=18, height=18, color=Color(0, 255, 255))
        elif power_type == "speed":
            self.sprite = Sprite(width=18, height=18, color=Color(255, 0, 255))
        elif power_type == "life":
            self.sprite = Sprite(width=18, height=18, color=Color(255, 100, 100))
        
        self.collider = Collider2D(18, 18, is_trigger=True)
        self.collider.game_object = self
        self.collected = False
        self.rotation_timer = 0
        
    def update(self, delta_time):
        super().update(delta_time)
        if self.collected:
            self.visible = False
        else:
            # Rotation animation
            self.rotation_timer += delta_time
            self.rotation = math.sin(self.rotation_timer * 3) * 10

class Star(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite(width=12, height=12, color=Color(255, 255, 255))
        self.collider = Collider2D(12, 12, is_trigger=True)
        self.collider.game_object = self
        self.collected = False
        self.twinkle_timer = 0
        
    def update(self, delta_time):
        super().update(delta_time)
        if self.collected:
            self.visible = False
        else:
            # Twinkling animation
            self.twinkle_timer += delta_time
            alpha = int(128 + 127 * math.sin(self.twinkle_timer * 8))
            self.sprite.color = Color(255, 255, 255, alpha)

class UI(GameObject):
    def __init__(self):
        super().__init__(0, 0)
        self.score_text = Text("Score: 0", 24, Color(255, 255, 255))
        self.lives_text = Text("Lives: 3", 24, Color(255, 255, 255))
        self.instructions_text = Text("WASD to move, SPACE to jump", 16, Color(200, 200, 200))
        
    def update(self, delta_time):
        super().update(delta_time)
        
    def render(self, screen, camera=None):
        # Render UI elements
        self.score_text.render(screen, Vector2(10, 10))
        self.lives_text.render(screen, Vector2(10, 40))
        self.instructions_text.render(screen, Vector2(10, 70))
        
    def update_score(self, score):
        self.score_text.set_text(f"Score: {score}")
        
    def update_lives(self, lives):
        self.lives_text.set_text(f"Lives: {lives}")

def main():
    print("🏃 لعبة المنصات المحسنة - Py2D Game")
    print("استخدم WASD للتحرك")
    print("اضغط SPACE للقفز")
    print("اجمع العملات الذهبية والنجوم!")
    print("تجنب الأعداء الحمراء!")
    print("اجمع القوى الخاصة!")
    print("اضغط ESC للخروج")
    
    engine = Py2DEngine(800, 600, "لعبة المنصات المحسنة")
    
    scene = Scene("اللعبة الرئيسية")
    scene.background_color = Color(135, 206, 235)  # Sky blue
    
    physics = Physics2D(Vector2(0, 800))
    scene.physics = physics
    
    player = Player(400, 400)
    scene.add_object(player)
    physics.add_rigid_body(player.rigid_body)
    physics.add_collider(player.collider)
    
    # Create UI
    ui = UI()
    scene.add_object(ui)
    
    # Create platforms with different colors
    platforms = [
        # Real ground - Multiple ground platforms for better physics
        Platform(0, 580, 200, 40, Color(50, 25, 0)),    # Left ground
        Platform(200, 580, 200, 40, Color(50, 25, 0)),  # Center-left ground
        Platform(400, 580, 200, 40, Color(50, 25, 0)),  # Center ground
        Platform(600, 580, 200, 40, Color(50, 25, 0)),  # Center-right ground
        Platform(800, 580, 200, 40, Color(50, 25, 0)),  # Right ground
        
        # Side walls to prevent falling off
        Platform(-20, 300, 40, 600, Color(100, 50, 0)),  # Left wall
        Platform(780, 300, 40, 600, Color(100, 50, 0)),  # Right wall
        
        # Starting platform for player (center) - bigger platform
        Platform(400, 560, 200, 30, Color(0, 150, 0)),  # Green starting platform
        
        # Additional center platform
        Platform(400, 480, 150, 20, Color(0, 200, 0)),  # Bright green platform
        
        # Other platforms
        Platform(400, 500, 200, 20, Color(100, 50, 0)),  # Brown
        Platform(200, 400, 150, 20, Color(50, 100, 50)),  # Green
        Platform(600, 400, 150, 20, Color(50, 50, 100)),  # Blue
        Platform(400, 300, 100, 20, Color(100, 50, 100)),  # Purple
        Platform(100, 200, 100, 20, Color(100, 100, 50)),  # Yellow
        Platform(700, 200, 100, 20, Color(50, 100, 100)),  # Cyan
        Platform(400, 100, 80, 20, Color(150, 50, 50)),   # Red
        Platform(200, 50, 120, 20, Color(50, 150, 50)),  # Bright Green
    ]
    
    for platform in platforms:
        scene.add_object(platform)
        physics.add_collider(platform.collider)
    
    # Create coins
    coins = [
        Coin(400, 530),  # On starting platform
        Coin(400, 450),  # On additional center platform
        Coin(400, 430),  # On brown platform
        Coin(250, 350),  # On green platform
        Coin(650, 350),  # On blue platform
        Coin(400, 250),  # On purple platform
        Coin(150, 150),  # On yellow platform
        Coin(750, 150),  # On cyan platform
        Coin(400, 50),   # On red platform
        Coin(250, 0),    # On bright green platform
    ]
    
    for coin in coins:
        scene.add_object(coin)
        physics.add_collider(coin.collider)
    
    # Create enemies
    enemies = [
        Enemy(300, 350),  # On green platform
        Enemy(500, 250),  # On purple platform
        Enemy(150, 150),  # On yellow platform
        Enemy(650, 50),   # On red platform
    ]
    
    for enemy in enemies:
        scene.add_object(enemy)
        physics.add_collider(enemy.collider)
    
    # Create power-ups
    powerups = [
        PowerUp(400, 430, "jump"),  # On brown platform
        PowerUp(250, 330, "speed"), # On green platform
        PowerUp(650, 330, "life"),  # On blue platform
        PowerUp(400, 230, "jump"),  # On purple platform
        PowerUp(150, 130, "speed"), # On yellow platform
        PowerUp(750, 130, "life"),  # On cyan platform
    ]
    
    for powerup in powerups:
        scene.add_object(powerup)
        physics.add_collider(powerup.collider)
    
    # Create stars
    stars = [
        Star(350, 430),  # On brown platform
        Star(450, 430),  # On brown platform
        Star(200, 330),  # On green platform
        Star(300, 330),  # On green platform
        Star(500, 330),  # On blue platform
        Star(600, 330),  # On blue platform
        Star(400, 230),  # On purple platform
        Star(100, 130),  # On yellow platform
        Star(200, 130),  # On yellow platform
        Star(700, 130),  # On cyan platform
        Star(800, 130),  # On cyan platform
    ]
    
    for star in stars:
        scene.add_object(star)
        physics.add_collider(star.collider)
    
    def collision_callback(collider1, collider2, pos1, pos2):
        obj1 = collider1.game_object
        obj2 = collider2.game_object
        
        # Player collision with collectibles
        if isinstance(obj1, Player):
            if isinstance(obj2, Coin) and not obj2.collected:
                obj2.collected = True
                obj1.add_score(10)
                ui.update_score(obj1.score)
            elif isinstance(obj2, Star) and not obj2.collected:
                obj2.collected = True
                obj1.add_score(50)
                ui.update_score(obj1.score)
            elif isinstance(obj2, PowerUp) and not obj2.collected:
                obj2.collected = True
                if obj2.power_type == "jump":
                    obj1.jump_force = 600
                    print("Jump power increased!")
                elif obj2.power_type == "speed":
                    obj1.speed = 450
                    print("Speed increased!")
                elif obj2.power_type == "life":
                    obj1.lives += 1
                    ui.update_lives(obj1.lives)
                    print("Extra life!")
                obj1.add_score(25)
                ui.update_score(obj1.score)
            elif isinstance(obj2, Enemy) and not obj1.invulnerable:
                obj1.take_damage()
                ui.update_lives(obj1.lives)
            elif hasattr(obj2, 'sprite') and not isinstance(obj2, (Coin, Star, PowerUp, Enemy)):
                # Platform collision - Better physics (no shaking)
                if obj1.position.y < obj2.position.y - 10:  # Player above platform
                    obj1.on_ground = True
                    obj1.rigid_body.velocity.y = 0
                    obj1.position.y = obj2.position.y - 32  # Snap to platform
                elif obj1.position.x < obj2.position.x and obj1.position.y > obj2.position.y - 20:  # Left side collision
                    obj1.position.x = obj2.position.x - 24
                    obj1.rigid_body.velocity.x = 0
                elif obj1.position.x > obj2.position.x and obj1.position.y > obj2.position.y - 20:  # Right side collision
                    obj1.position.x = obj2.position.x + obj2.sprite.width + 24
                    obj1.rigid_body.velocity.x = 0
        elif isinstance(obj2, Player):
            if isinstance(obj1, Coin) and not obj1.collected:
                obj1.collected = True
                obj2.add_score(10)
                ui.update_score(obj2.score)
            elif isinstance(obj1, Star) and not obj1.collected:
                obj1.collected = True
                obj2.add_score(50)
                ui.update_score(obj2.score)
            elif isinstance(obj1, PowerUp) and not obj1.collected:
                obj1.collected = True
                if obj1.power_type == "jump":
                    obj2.jump_force = 600
                    print("Jump power increased!")
                elif obj1.power_type == "speed":
                    obj2.speed = 450
                    print("Speed increased!")
                elif obj1.power_type == "life":
                    obj2.lives += 1
                    ui.update_lives(obj2.lives)
                    print("Extra life!")
                obj2.add_score(25)
                ui.update_score(obj2.score)
            elif isinstance(obj1, Enemy) and not obj2.invulnerable:
                obj2.take_damage()
                ui.update_lives(obj2.lives)
            elif hasattr(obj1, 'sprite') and not isinstance(obj1, (Coin, Star, PowerUp, Enemy)):
                # Platform collision - Better physics
                if obj2.position.y < obj1.position.y - 10:  # Player above platform
                    obj2.on_ground = True
                    obj2.rigid_body.velocity.y = 0
                    obj2.position.y = obj1.position.y - 32  # Snap to platform
                elif obj2.position.x < obj1.position.x and obj2.position.y > obj1.position.y - 20:  # Left side collision
                    obj2.position.x = obj1.position.x - 24
                    obj2.rigid_body.velocity.x = 0
                elif obj2.position.x > obj1.position.x and obj2.position.y > obj1.position.y - 20:  # Right side collision
                    obj2.position.x = obj1.position.x + obj1.sprite.width + 24
                    obj2.rigid_body.velocity.x = 0
    
    physics.add_collision_callback(collision_callback)
    
    def update_scene(delta_time):
        for obj in scene.game_objects:
            obj.update(delta_time)
        physics.update(delta_time, scene.game_objects)
        
        # Update UI
        ui.update_score(player.score)
        ui.update_lives(player.lives)
    
    scene.update = update_scene
    
    engine.add_scene(scene)
    engine.set_scene("اللعبة الرئيسية")
    engine.run()

if __name__ == "__main__":
    main()
