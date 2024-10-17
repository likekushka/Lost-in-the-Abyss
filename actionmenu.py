from pygame import font, Surface, Rect, MOUSEBUTTONDOWN
from monster import Monster
from player import Player
from constants import BLACK, WHITE, SCREEN_HEIGHT, SCREEN_WIDTH
from message_ui import MessageUI


class ActionMenu:
    def __init__(self):

        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT // 2
        self.x = 0
        self.y = SCREEN_HEIGHT // 2
        self.font = font.Font("Fonts/determination.otf", 40)
        self.surface = Surface((self.width, self.height))
        self.buttons = {
            "atk": {"render": self.font.render("Атака", True, WHITE), "rect": Rect(0, 0, 0, 0)},
            "def": {"render": self.font.render("Защита", True, WHITE), "rect": Rect(0, 0, 0, 0)},
            "esc": {"render": self.font.render("Сбежать", True, WHITE), "rect": Rect(0, 0, 0, 0)},
            "save": {"render": self.font.render("Сохранить", True, WHITE), "rect": Rect(0, 0, 0, 0)},
            "load": {"render": self.font.render("Загрузить", True, WHITE), "rect": Rect(0, 0, 0, 0)}
        }

    def draw(self, screen):
        self.surface.fill(BLACK)

        y_offset = 50
        for button_name, button_data in self.buttons.items():
            text_render = button_data["render"]
            self.surface.blit(text_render, (10, y_offset))
            button_data["rect"] = Rect(
                self.x + 10,
                self.y + y_offset,
                text_render.get_width(),
                text_render.get_height()
            )
            y_offset += 50

        screen.blit(self.surface, (self.x, self.y))

    def handle_event(self, event, player: Player, monster: Monster, message: MessageUI,
                     reset_monster, save_game_callback, load_game_callback):
        if event.type == MOUSEBUTTONDOWN:
            for button_name, button_data in self.buttons.items():
                if button_data["rect"].collidepoint(event.pos):
                    if button_name == "atk":
                        player.attack(monster)
                        monster.sprite.set_animation("hurt")

                        if monster.hp > 0:
                            monster.attack(player)
                            player.update_defense_status()

                    elif button_name == "def":
                        if not player.defense_cd:
                            player.defend()
                            message.show_message_ui("jsons/messages.json", "message",
                                                    message_name="def_start", fill_black=False)
                        else:
                            message.show_message_ui("jsons/messages.json", "message",
                                                    message_name="def_cd", fill_black=False, player=player)

                    elif button_name == "esc":
                        message.show_message_ui("jsons/messages.json", "message",
                                                message_name="escape")
                        reset_monster()

                    elif button_name == "save":
                        save_game_callback()

                    elif button_name == "load":
                        load_game_callback()

        if player.defense_cd:
            self.buttons['def']['render'] = self.font.render(f"Защита ({player.defense_cd})", True,
                                                             (150, 150, 150))
        else:
            self.buttons['def']['render'] = self.font.render("Защита", True, WHITE)