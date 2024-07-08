import pickle
from player import Player
from monster import Monster
from message import Message


def save_game(player, monster, message):
    save_data = {
        "player": {
            "name": player.name,
            "max_hp": player.max_hp,
            "hp": player.hp,
            "atk": player.atk,
            "lvl": player.lvl,
            "exp": player.exp,
            "defending": player.defending,
            "defense_turns": player.defense_turns,
        },
        "monster": {
            "name": monster.name,
            "max_hp": monster.max_hp,
            "hp": monster.hp,
            "atk": monster.atk,
            "lvl": monster.lvl,
            "exp": monster.exp,
            "sprite_path": monster.sprite_path,
        },
        "message": {
            "current_message": message.current_message,
            "hidden": message.hidden,
        }
    }

    with open("savegame.pkl", "wb") as file:
        pickle.dump(save_data, file)

def load_game():
    with open("savegame.pkl", "rb") as file:
        save_data = pickle.load(file)

    player_data = save_data["player"]
    monster_data = save_data["monster"]
    message_data = save_data["message"]

    player = Player(player_data["name"], player_data["max_hp"], player_data["atk"], player_data["lvl"])
    player.hp = player_data["hp"]
    player.exp = player_data["exp"]
    player.defending = player_data["defending"]
    player.defense_turns = player_data["defense_turns"]

    monster = Monster.load_from_save_data(monster_data)

    message = Message()
    message.current_message = message_data["current_message"]
    message.hidden = message_data["hidden"]

    return player, monster, message
