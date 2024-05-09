from character import Character
from animatedsprite import AnimatedSprite
from pygame import image, transform
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Monster(Character):
    def __init__(self, name: str, hp: int,
                 atk: int, lvl: int, exp: int):
        super().__init__(name, hp, atk, lvl)
        self.exp = exp
        self.sprite = None

    def attack(self, target: Character):
        target.hp -= self.atk

    def sprite_load(self, sprite_path: str):
        sprite_frames = [image.load(f"{sprite_path}_idle_{i}.png") for i in range(1, 5)]
        for i in range(4):
            sprite_frames[i] = transform.scale(sprite_frames[i], (450, 450))
        self.sprite = AnimatedSprite(sprite_frames, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
