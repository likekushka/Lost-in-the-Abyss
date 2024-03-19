from character import Character


class Player(Character):
    def __init__(self, name: str, hp: int,
                 atk: int, lvl: int):
        super().__init__(name, hp, atk, lvl)

    def attack(self, target: Character):
        target.hp -= self.atk

