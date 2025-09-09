from py2d_game import Py2DEngine, GameObject, Scene, Sprite, Color, Vector2, Physics2D, RigidBody2D, Collider2D

class Platform(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.sprite = Sprite(width=width, height=height, color=Color(100, 50, 0))
        self.collider = Collider2D(width, height)
        self.collider.game_object = self

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite(width=24, height=32, color=Color(0, 255, 0))
        self.rigid_body = RigidBody2D(mass=1.0, gravity_scale=1.0)
        self.collider = Collider2D(24, 32)
        self.collider.game_object = self
        self.speed = 300
        self.jump_force = 400
        self.on_ground = False
        
    def update(self, delta_time):
        super().update(delta_time)
        
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
        
        if self.position.x < 12:
            self.position.x = 12
        elif self.position.x > 788:
            self.position.x = 788

class Coin(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite(width=16, height=16, color=Color(255, 255, 0))
        self.collider = Collider2D(16, 16, is_trigger=True)
        self.collider.game_object = self
        self.collected = False
        
    def update(self, delta_time):
        super().update(delta_time)
        if self.collected:
            self.visible = False

def main():
    engine = Py2DEngine(800, 600, "لعبة المنصات - Py2D")
    
    scene = Scene("اللعبة الرئيسية")
    scene.background_color = Color(135, 206, 235)
    
    physics = Physics2D(Vector2(0, 500))
    scene.physics = physics
    
    player = Player(100, 400)
    scene.add_object(player)
    physics.add_rigid_body(player.rigid_body)
    physics.add_collider(player.collider)
    
    platforms = [
        Platform(400, 550, 200, 20),
        Platform(200, 450, 150, 20),
        Platform(600, 450, 150, 20),
        Platform(400, 350, 100, 20),
        Platform(100, 250, 100, 20),
        Platform(700, 250, 100, 20),
    ]
    
    for platform in platforms:
        scene.add_object(platform)
        physics.add_collider(platform.collider)
    
    coins = [
        Coin(400, 500),
        Coin(250, 400),
        Coin(650, 400),
        Coin(400, 300),
        Coin(150, 200),
        Coin(750, 200),
    ]
    
    for coin in coins:
        scene.add_object(coin)
        physics.add_collider(coin.collider)
    
    def collision_callback(collider1, collider2, pos1, pos2):
        if (hasattr(collider1.game_object, 'collected') and 
            hasattr(collider2.game_object, 'collected')):
            if collider1.game_object.collected:
                collider1.game_object.collected = True
            elif collider2.game_object.collected:
                collider2.game_object.collected = True
        elif (hasattr(collider1.game_object, 'on_ground') and 
              hasattr(collider2.game_object, 'sprite')):
            if collider1.game_object.position.y < collider2.game_object.position.y:
                collider1.game_object.on_ground = True
        elif (hasattr(collider2.game_object, 'on_ground') and 
              hasattr(collider1.game_object, 'sprite')):
            if collider2.game_object.position.y < collider1.game_object.position.y:
                collider2.game_object.on_ground = True
    
    physics.add_collision_callback(collision_callback)
    
    def update_scene(delta_time):
        for obj in scene.game_objects:
            obj.update(delta_time)
        physics.update(delta_time, scene.game_objects)
    
    scene.update = update_scene
    
    engine.add_scene(scene)
    engine.set_scene("اللعبة الرئيسية")
    engine.run()

if __name__ == "__main__":
    main()
