import pickle
from character import Character
from player import Player
from monster import Monster
from message_ui import MessageUI


def save_game(player: Character, monster: Character, message: MessageUI):
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
            "defense_cd": player.defense_cd,
        },
        "monster": {
            "name": monster.name,
            "max_hp": monster.max_hp,
            "hp": monster.hp,
            "atk": monster.atk,
            "lvl": monster.lvl,
            "exp": monster.exp,
            "boss": monster.boss_status,
            "sprite_path": monster.sprite_path,
        }
    }
    try:
        with open("save.pkl", "wb") as file:
            pickle.dump(save_data, file)

        message.show_message_ui("jsons/messages.json", "message", message_name="save_success")
    except FileNotFoundError:
        message.show_message_ui("jsons/messages.json", "message", message_name="save_error")


def load_game(message: MessageUI):
    try:
        with open("save.pkl", "rb") as file:
            save_data = pickle.load(file)
        player_data = save_data["player"]
        monster_data = save_data["monster"]

        player = Player(player_data["name"], player_data["max_hp"], player_data["atk"], player_data["lvl"])
        player.load_from_save_data(player_data)

        monster = Monster()
        monster.load_from_save_data(monster_data)

        message.show_message_ui("jsons/messages.json", "message", message_name="load_success")

        return player, monster
    except FileNotFoundError:
        message.show_message_ui("jsons/messages.json", "message", message_name="load_error")
