import pygame
import os
from typing import Dict, Optional

class AudioManager:
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music_volume = 0.7
        self.sound_volume = 0.7
        
    def load_sound(self, name: str, file_path: str):
        try:
            if os.path.exists(file_path):
                self.sounds[name] = pygame.mixer.Sound(file_path)
            else:
                print(f"Sound file not found: {file_path}")
        except pygame.error as e:
            print(f"Error loading sound {name}: {e}")
            
    def play_sound(self, name: str, volume: float = 1.0):
        if name in self.sounds:
            sound = self.sounds[name]
            sound.set_volume(self.sound_volume * volume)
            sound.play()
        else:
            print(f"Sound '{name}' not found")
            
    def stop_sound(self, name: str):
        if name in self.sounds:
            self.sounds[name].stop()
            
    def stop_all_sounds(self):
        pygame.mixer.stop()
        
    def load_music(self, file_path: str):
        try:
            if os.path.exists(file_path):
                pygame.mixer.music.load(file_path)
            else:
                print(f"Music file not found: {file_path}")
        except pygame.error as e:
            print(f"Error loading music: {e}")
            
    def play_music(self, loop: int = -1, fade_in: int = 0):
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(loop, fade_ms=fade_in)
        
    def stop_music(self, fade_out: int = 0):
        pygame.mixer.music.fadeout(fade_out)
        
    def pause_music(self):
        pygame.mixer.music.pause()
        
    def unpause_music(self):
        pygame.mixer.music.unpause()
        
    def set_music_volume(self, volume: float):
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
        
    def set_sound_volume(self, volume: float):
        self.sound_volume = max(0.0, min(1.0, volume))
        
    def is_music_playing(self) -> bool:
        return pygame.mixer.music.get_busy()
        
    def get_music_volume(self) -> float:
        return self.music_volume
        
    def get_sound_volume(self) -> float:
        return self.sound_volume
