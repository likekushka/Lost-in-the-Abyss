from character import Character
from animatedsprite import AnimatedSprite
from pygame import image, transform
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import random


class Monster(Character):
    MONSTER_STATS = [
        {"name": "Скелет", "hp": 20, "atk": 5, "lvl": 1, "exp": 100, "sprite_path": "Sprites/Skeleton/"},
        {"name": "Зомби", "hp": 25, "atk": 3, "lvl": 1, "exp": 120, "sprite_path": "Sprites/Zombie/"},
        {"name": "Вампир", "hp": 30, "atk": 7, "lvl": 2, "exp": 150, "sprite_path": "Sprites/Vampire/"},
        # Добавьте больше монстров здесь
    ]

    def __init__(self):
        stats = random.choice(self.MONSTER_STATS)
        super().__init__(stats["name"], stats["hp"], stats["atk"], stats["lvl"], stats["exp"])
        self.sprite_path = stats["sprite_path"]
        self.sprite = None
        self.sprite_load(stats["sprite_path"])

    @classmethod
    def load_from_save_data(cls, data):
        monster = cls.__new__(cls)
        super(Monster, monster).__init__(data["name"], data["max_hp"], data["atk"], data["lvl"], data["exp"])
        monster.hp = data["hp"]
        monster.sprite_path = data["sprite_path"]
        monster.sprite_load(monster.sprite_path)
        return monster

    def attack(self, target: Character):
        if target.defending:
            damage = self.atk // 2
        else:
            damage = self.atk
        target.hp -= damage

    def sprite_load(self, sprite_path: str):
        idle_frames = self._load_and_scale_frames(f"{sprite_path}_idle_", 4)
        hurt_frames = self._load_and_scale_frames(f"{sprite_path}_hurt_", 4, add_last_frame=True)
        death_frames = self._load_and_scale_frames(f"{sprite_path}_death_", 4, add_last_frame=True)

        self.sprite = AnimatedSprite(idle_frames, hurt_frames, death_frames,
                                     SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

    def _load_and_scale_frames(self, base_path: str, count: int, add_last_frame: bool = False):
        frames = [image.load(f"{base_path}{i}.png") for i in range(1, count + 1)]
        frames = [transform.scale(frame, (450, 450)) for frame in frames]

        if add_last_frame:
            frames.append(frames[-1])

        return frames
