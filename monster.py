from character import Character
from animatedsprite import AnimatedSprite
from pygame import image, transform
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from random import choice


class Monster(Character):
    MONSTER_STATS = [
        {"name": "Скелет", "hp": 30, "atk": 8, "lvl": 1, "exp": 150, "sprite_path": "Sprites/Skeleton/"},
        {"name": "Гоблин", "hp": 15, "atk": 3, "lvl": 1, "exp": 100, "sprite_path": "Sprites/Goblin/"},
        {"name": "Летающий глаз", "hp": 10, "atk": 7, "lvl": 1, "exp": 120, "sprite_path": "Sprites/Eye/"},
    ]

    BOSS_STATS = {"name": "Змей", "hp": 150, "atk": 15, "lvl": 100, "exp": 100000, "sprite_path": "Sprites/SnakeGod/"}

    def __init__(self, boss_status = False):
        stats = choice(self.MONSTER_STATS) if not boss_status else self.BOSS_STATS
        super().__init__(stats["name"], stats["hp"], stats["atk"], stats["lvl"], stats["exp"])
        self.boss_status = boss_status
        self.sprite_path = stats["sprite_path"]
        self.sprite = None
        self.sprite_load(stats["sprite_path"])

    def load_from_save_data(self, data):
        self.name = data["name"]
        self.max_hp = data["max_hp"]
        self.atk = data["atk"]
        self.lvl = data["lvl"]
        self.exp = data["exp"]
        self.hp = data["hp"]
        self.boss_status = data["boss"]
        self.sprite_path = data["sprite_path"]
        self.sprite_load(self.sprite_path)

    def attack(self, target: Character):
        if target.defending:
            damage = self.atk // 2
        else:
            damage = self.atk

        if damage > target.hp:
            target.hp = 0
        else:
            target.hp -= damage

    def sprite_load(self, sprite_path: str):
        idle_frames = self._load_and_scale_frames(f"{sprite_path}_idle_", 4)
        hurt_frames = self._load_and_scale_frames(f"{sprite_path}_hurt_", 4, add_last_frame=True)
        if not self.boss_status:
            death_frames = self._load_and_scale_frames(f"{sprite_path}_death_", 4, add_last_frame=True)
        else:
            death_frames = self._load_and_scale_frames(f"{sprite_path}_death_", 4, double_frames=True,
                                                       add_last_frame=True)
        attack_frames = self._load_and_scale_frames(f"{sprite_path}_attack_", 5, add_last_frame=True)

        self.sprite = AnimatedSprite(idle_frames, hurt_frames, death_frames, attack_frames,
                                     SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

    def _load_and_scale_frames(self, base_path: str, count: int, add_last_frame: bool = False,
                               double_frames: bool = False):
        try:
            frames = [image.load(f"{base_path}{i}.png") for i in range(1, count + 1)]
            frames = [transform.scale(frame, (650, 650)) for frame in frames]

            if double_frames:
                doubled_frames = []
                for i in range(count):
                    doubled_frames.append(frames[i])
                    doubled_frames.append(frames[i])
                frames = doubled_frames
            if add_last_frame:
                frames.append(frames[-1])

            return frames
        except FileNotFoundError:
            print(f"file not found: {base_path}")
