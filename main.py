from player import Player
from monster import Monster

player = Player("likek", 20, 5, 1)
monster = Monster("Vampire", 20, 5, 1, 200)

player.attack(monster)
monster.attack(player)

print(player.hp, monster.hp)