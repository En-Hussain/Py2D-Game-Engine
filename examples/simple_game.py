from py2d_game import Py2DEngine, GameObject, Scene, Sprite, Color, Vector2, InputManager

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
        self.speed = 100
        self.direction = Vector2(1, 0)
        
    def update(self, delta_time):
        super().update(delta_time)
        
        self.position += self.direction * self.speed * delta_time
        
        if self.position.x <= 12 or self.position.x >= 788:
            self.direction.x *= -1
        if self.position.y <= 12 or self.position.y >= 588:
            self.direction.y *= -1

def main():
    engine = Py2DEngine(800, 600, "لعبة بسيطة - Py2D")
    
    scene = Scene("اللعبة الرئيسية")
    scene.background_color = Color(50, 50, 100)
    
    player = Player(400, 300)
    scene.add_object(player)
    
    for i in range(5):
        enemy = Enemy(100 + i * 150, 100)
        scene.add_object(enemy)
    
    engine.add_scene(scene)
    engine.set_scene("اللعبة الرئيسية")
    engine.run()

if __name__ == "__main__":
    main()
