from character import Character
from animatedsprite import AnimatedSprite


class Monster(Character):
    def __init__(self, name: str, hp: int,
                 atk: int, lvl: int, exp: int, sprite: AnimatedSprite):
        super().__init__(name, hp, atk, lvl)
        self.exp = exp
        self.sprite = sprite

    def attack(self, target: Character):
        target.hp -= self.atk
