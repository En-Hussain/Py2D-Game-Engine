import sys
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Py2D - مكتبة Python للألعاب ثنائية الأبعاد")
    parser.add_argument("--version", action="version", version="Py2D 1.0.0")
    parser.add_argument("--create-project", type=str, help="إنشاء مشروع جديد")
    parser.add_argument("--run-example", type=str, help="تشغيل مثال")
    
    args = parser.parse_args()
    
    if args.create_project:
        create_project(args.create_project)
    elif args.run_example:
        run_example(args.run_example)
    else:
        print("Py2D - مكتبة Python للألعاب ثنائية الأبعاد")
        print("استخدم --help لرؤية الخيارات المتاحة")

def create_project(project_name):
    """إنشاء مشروع جديد"""
    if os.path.exists(project_name):
        print(f"المجلد '{project_name}' موجود بالفعل!")
        return
        
    os.makedirs(project_name)
    
    # إنشاء ملف اللعبة الرئيسي
    main_file = f"{project_name}/main.py"
    with open(main_file, "w", encoding="utf-8") as f:
        f.write('''from py2d import Py2DEngine, GameObject, Scene, Sprite, Color, Vector2

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
    engine = Py2DEngine(800, 600, "لعبتي الجديدة")
    
    scene = Scene("اللعبة الرئيسية")
    scene.background_color = Color(50, 50, 100)
    
    player = Player(400, 300)
    scene.add_object(player)
    
    engine.add_scene(scene)
    engine.set_scene("اللعبة الرئيسية")
    engine.run()

if __name__ == "__main__":
    main()
''')
    
    # إنشاء ملف requirements
    requirements_file = f"{project_name}/requirements.txt"
    with open(requirements_file, "w", encoding="utf-8") as f:
        f.write("py2d>=1.0.0\n")
    
    print(f"تم إنشاء المشروع '{project_name}' بنجاح!")
    print(f"انتقل إلى المجلد: cd {project_name}")
    print(f"ثم شغل اللعبة: python main.py")

def run_example(example_name):
    """تشغيل مثال"""
    examples = {
        "simple": "examples/simple_game.py",
        "platformer": "examples/platformer_game.py", 
        "shooter": "examples/space_shooter.py"
    }
    
    if example_name not in examples:
        print(f"المثال '{example_name}' غير موجود!")
        print(f"الأمثلة المتاحة: {', '.join(examples.keys())}")
        return
        
    example_file = examples[example_name]
    if not os.path.exists(example_file):
        print(f"ملف المثال '{example_file}' غير موجود!")
        return
        
    print(f"تشغيل المثال: {example_name}")
    os.system(f"python {example_file}")

if __name__ == "__main__":
    main()
