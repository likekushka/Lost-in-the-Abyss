from character import Character


class Player(Character):
    def __init__(self, name="Likek", hp=40,
                 atk=5, lvl=1):
        super().__init__(name, hp, atk, lvl, exp=0)

        self.level_up_exp = [100, 400, 700, 1000, 1500, 2000, 3000, 4000, 6000, 8000, 11000]
        self.level_up_hp_bonus = [10, 20, 30, 40, 50, 60, 70, 80]
        self.level_up_atk_bonus = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.defending = False
        self.defense_cd = 0
        self.defense_turns = 0

    def level_up(self, exp: int):
        self.exp += exp
        if self.exp >= self.level_up_exp[self.lvl - 1]:
            self.exp = self.exp - self.level_up_exp[self.lvl - 1]
            self.lvl += 1

            self.max_hp += self.level_up_hp_bonus[self.lvl - 1]
            self.hp = self.max_hp
            self.atk += self.level_up_atk_bonus[self.lvl - 1]

            return True

    def attack(self, target: Character):
        if self.atk > target.hp:
            target.hp = 0
        else:
            target.hp -= self.atk

    def defend(self):
        self.defending = True
        self.defense_turns = 2
        self.defense_cd = 7

    def update_defense_status(self):
        if self.defending:
            self.defense_turns -= 1
            if self.defense_turns <= 0:
                self.defending = False

        self.defense_cd -= 1
        if self.defense_cd <= 0:
            self.defense_cd = 0

    def load_from_save_data(self, data):
        self.exp = data["exp"]
        self.hp = data["hp"]
        self.defending = data["defending"]
        self.defense_turns = data["defense_turns"]
        self.defense_cd = data["defense_cd"]