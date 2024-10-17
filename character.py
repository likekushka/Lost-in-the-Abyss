class Character:
    def __init__(self, name: str, hp: int,
                 atk: int, lvl: int, exp: int):
        self.name = name
        self.hp = hp
        self.max_hp = self.hp
        self.atk = atk
        self.lvl = lvl
        self.exp = exp
        self.defending = False
        self.defense_turns = 0

    def attack(self, target):
        pass
