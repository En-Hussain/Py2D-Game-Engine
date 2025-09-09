from py2d_game import Py2DEngine, GameObject, Scene, Sprite, Color, Vector2, Animation, AudioManager
import random
import pygame

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite(width=40, height=40, color=Color(0, 255, 255))
        self.speed = 300
        self.shoot_timer = 0
        self.shoot_cooldown = 0.2
        
    def update(self, delta_time):
        super().update(delta_time)
        
        input_manager = self.scene.game_engine.input_manager
        
        if input_manager.is_key_pressed('left') or input_manager.is_key_pressed('a'):
            self.position.x -= self.speed * delta_time
        if input_manager.is_key_pressed('right') or input_manager.is_key_pressed('d'):
            self.position.x += self.speed * delta_time
        if input_manager.is_key_pressed('up') or input_manager.is_key_pressed('w'):
            self.position.y -= self.speed * delta_time
        if input_manager.is_key_pressed('down') or input_manager.is_key_pressed('s'):
            self.position.y += self.speed * delta_time
            
        if self.position.x < 20:
            self.position.x = 20
        elif self.position.x > 780:
            self.position.x = 780
        if self.position.y < 20:
            self.position.y = 20
        elif self.position.y > 580:
            self.position.y = 580
            
        self.shoot_timer += delta_time
        if (input_manager.is_key_pressed('space') and 
            self.shoot_timer >= self.shoot_cooldown):
            self.shoot()
            self.shoot_timer = 0

    def shoot(self):
        bullet = Bullet(self.position.x, self.position.y - 20, Vector2(0, -1))
        self.scene.add_object(bullet)

class Bullet(GameObject):
    def __init__(self, x, y, direction):
        super().__init__(x, y)
        self.sprite = Sprite(width=4, height=8, color=Color(255, 255, 0))
        self.direction = direction
        self.speed = 500
        
    def update(self, delta_time):
        super().update(delta_time)
        self.position += self.direction * self.speed * delta_time
        
        if (self.position.y < -10 or self.position.y > 610 or 
            self.position.x < -10 or self.position.x > 810):
            self.scene.remove_object(self)

class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite(width=30, height=30, color=Color(255, 0, 0))
        self.speed = random.uniform(50, 150)
        self.shoot_timer = 0
        self.shoot_cooldown = random.uniform(1, 3)
        
    def update(self, delta_time):
        super().update(delta_time)
        self.position.y += self.speed * delta_time
        
        self.shoot_timer += delta_time
        if self.shoot_timer >= self.shoot_cooldown:
            self.shoot()
            self.shoot_timer = 0
            
        if self.position.y > 620:
            self.scene.remove_object(self)

    def shoot(self):
        bullet = EnemyBullet(self.position.x, self.position.y + 20, Vector2(0, 1))
        self.scene.add_object(bullet)

class EnemyBullet(GameObject):
    def __init__(self, x, y, direction):
        super().__init__(x, y)
        self.sprite = Sprite(width=4, height=8, color=Color(255, 100, 100))
        self.direction = direction
        self.speed = 300
        
    def update(self, delta_time):
        super().update(delta_time)
        self.position += self.direction * self.speed * delta_time
        
        if (self.position.y < -10 or self.position.y > 610 or 
            self.position.x < -10 or self.position.x > 810):
            self.scene.remove_object(self)

class StarField:
    def __init__(self, width, height, num_stars=100):
        self.width = width
        self.height = height
        self.stars = []
        for _ in range(num_stars):
            self.stars.append({
                'x': random.uniform(0, width),
                'y': random.uniform(0, height),
                'speed': random.uniform(20, 100)
            })
    
    def update(self, delta_time):
        for star in self.stars:
            star['y'] += star['speed'] * delta_time
            if star['y'] > self.height:
                star['y'] = 0
                star['x'] = random.uniform(0, self.width)
    
    def render(self, screen):
        for star in self.stars:
            pygame.draw.circle(screen, (255, 255, 255), 
                             (int(star['x']), int(star['y'])), 1)

def main():
    engine = Py2DEngine(800, 600, "مطلق النار الفضائي - Py2D")
    
    scene = Scene("اللعبة الرئيسية")
    scene.background_color = Color(0, 0, 20)
    
    star_field = StarField(800, 600)
    
    player = Player(400, 500)
    scene.add_object(player)
    
    enemy_spawn_timer = 0
    enemy_spawn_cooldown = 2.0
    
    def update_scene(delta_time):
        nonlocal enemy_spawn_timer, enemy_spawn_cooldown
        
        for obj in scene.game_objects:
            obj.update(delta_time)
        star_field.update(delta_time)
        
        enemy_spawn_timer += delta_time
        if enemy_spawn_timer >= enemy_spawn_cooldown:
            enemy = Enemy(random.uniform(50, 750), -30)
            scene.add_object(enemy)
            enemy_spawn_timer = 0
            enemy_spawn_cooldown = random.uniform(0.5, 2.0)
    
    def render_scene(screen):
        screen.fill(scene.background_color.rgba)
        star_field.render(screen)
        
        for obj in scene.game_objects:
            obj.render(screen, scene.camera)
    
    scene.update = update_scene
    scene.render = render_scene
    
    engine.add_scene(scene)
    engine.set_scene("اللعبة الرئيسية")
    engine.run()

if __name__ == "__main__":
    main()
