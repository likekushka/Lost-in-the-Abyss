from abc import ABC, abstractmethod


class Character(ABC):
    def __init__(self, name: str, hp: int,
                 atk: int, lvl: int):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.lvl = lvl

    @abstractmethod
    def attack(self, target):
        pass