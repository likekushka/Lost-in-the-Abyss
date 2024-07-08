from character import Character
from message import Message


class Player(Character):
    def __init__(self, name: str, hp: int,
                 atk: int, lvl: int):
        super().__init__(name, hp, atk, lvl, exp=0)

        self.level_up_exp = [100, 400, 700, 1000, 1500, 2000, 3000, 4000, 6000, 8000, 11000]
        self.defending = False
        self.defense_turns = 0

    def level_up(self, message: Message):
        if self.exp >= self.level_up_exp[self.lvl - 1]:
            self.exp = self.exp - self.level_up_exp[self.lvl - 1]
            self.lvl += 1

            self.max_hp += 50
            self.hp = self.max_hp
            self.atk += 1

            message.clear()
            message.current_message = "Вы повысили уровень!\nВаше здоровье повышено на 50!\nВаша атака повышена на 1!"
            message.hidden = False

    def attack(self, target: Character):
        if self.atk > target.hp:
            target.hp = 0
        else:
            target.hp -= self.atk

    def defend(self):
        self.defending = True
        self.defense_turns = 2

    def update_defense_status(self):
        if self.defending:
            self.defense_turns -= 1
            if self.defense_turns <= 0:
                self.defending = False
