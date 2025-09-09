import unittest
from py2d_game import Py2DEngine, GameObject, Scene, Vector2, Color

class TestGameObject(unittest.TestCase):
    def setUp(self):
        self.obj = GameObject(100, 200)
    
    def test_initialization(self):
        self.assertEqual(self.obj.position.x, 100)
        self.assertEqual(self.obj.position.y, 200)
        self.assertEqual(self.obj.rotation, 0.0)
        self.assertEqual(self.obj.scale.x, 1.0)
        self.assertEqual(self.obj.scale.y, 1.0)
        self.assertTrue(self.obj.visible)
        self.assertTrue(self.obj.active)
    
    def test_position_update(self):
        self.obj.position = Vector2(150, 250)
        self.assertEqual(self.obj.position.x, 150)
        self.assertEqual(self.obj.position.y, 250)

class TestScene(unittest.TestCase):
    def setUp(self):
        self.scene = Scene("Test Scene")
    
    def test_initialization(self):
        self.assertEqual(self.scene.name, "Test Scene")
        self.assertEqual(len(self.scene.game_objects), 0)
        self.assertIsNotNone(self.scene.camera)
    
    def test_add_object(self):
        obj = GameObject(0, 0)
        self.scene.add_object(obj)
        self.assertEqual(len(self.scene.game_objects), 1)
        self.assertEqual(obj.scene, self.scene)

class TestPy2DEngine(unittest.TestCase):
    def setUp(self):
        self.engine = Py2DEngine(800, 600, "Test Game")
    
    def test_initialization(self):
        self.assertEqual(self.engine.width, 800)
        self.assertEqual(self.engine.height, 600)
        self.assertEqual(self.engine.title, "Test Game")
        self.assertIsNotNone(self.engine.input_manager)
        self.assertIsNotNone(self.engine.audio_manager)
    
    def test_add_scene(self):
        scene = Scene("Test Scene")
        self.engine.add_scene(scene)
        self.assertIn("Test Scene", self.engine.scenes)
        self.assertEqual(scene.game_engine, self.engine)

if __name__ == '__main__':
    unittest.main()
