from characters import Character


class Monster(Character):
    def __init__(self, name: str, hp: int,
                 atk: int, lvl: int, exp: int):
        super().__init__(name, hp, atk, lvl)
        self.exp = exp

    def attack(self, target: Character):
        target.hp -= self.atk