import pygame
import sys
from pygame import Rect, Surface, font, MOUSEBUTTONDOWN
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, FONT_SIZE, FONT_PATH
import json


class MessageUI:
    def __init__(self, screen: Surface, width=600, height=400):
        self.width = width
        self.height = height
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT // 2 - self.height // 2

        self.hidden = True

        self.font = font.Font(FONT_PATH, FONT_SIZE)

        self.screen = screen
        self.surface = Surface((self.width, self.height))
        self.boarder_surface = Surface((self.width + 10, self.height + 10))

        self.buttons = {
            "ok": {"render": self.font.render("Oк", True, WHITE), "rect": Rect(0, 0, 0, 0)},
            "yes": {"render": self.font.render("Да", True, WHITE), "rect": Rect(0, 0, 0, 0)},
            "no": {"render": self.font.render("Нет", True, WHITE), "rect": Rect(0, 0, 0, 0)},
            "next": {"render": self.font.render("--->", True, WHITE), "rect": Rect(0, 0, 0, 0)},
            "restart": {"render": self.font.render("Начать заново", True, WHITE),
                        "rect": Rect(0, 0, 0, 0)},
            "load": {"render": self.font.render("Загрузить", True, WHITE), "rect": Rect(0, 0, 0, 0)},
            "apply": {"render": self.font.render("Принять", True, WHITE), "rect": Rect(0, 0, 0, 0)}
        }
        self.button_pressed = None

        self.current_message = ""
        self.current_dialog = None
        self.dialog_data = None

    def _load_message(self, dialog_id):
        if dialog_id in self.dialog_data:
            self.current_dialog = self.dialog_data[dialog_id]
            self.current_message = "\n".join(self.current_dialog["messages"])
            self.hidden = False

        else:
            print(f"Dialog {dialog_id} not found!")

    def _load_file_data(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                self.dialog_data = json.load(file)
            return True

        except FileNotFoundError:
            print(f"file {filepath} not found!")
            return False

    def _fill_surfaces(self):
        self.surface.fill(BLACK)
        self.boarder_surface.fill(WHITE)

    def _blit_surfaces(self):
        self.screen.blit(self.boarder_surface, (self.x, self.y))
        self.screen.blit(self.surface, (self.x + 5, self.y + 5))

    def _calculate_button_position(self):
        button_y = self.height - 50
        button_gap = 20
        total_width = sum(
            self.buttons[btn]["render"].get_width() for btn in self.current_dialog["buttons"]) + button_gap * (
                              len(self.current_dialog["buttons"]) - 1)
        button_x = (self.width - total_width) // 2
        return button_x, button_y
    def _render_line(self, text, font_size):
        message_text_render = self.font.render(text, True, WHITE)

        while message_text_render.get_width() > self.width - 30 and font_size >= 30:
            font_size -= 1
            self.font = font.Font(FONT_PATH, font_size)
            message_text_render = self.font.render(text, True, WHITE)

        return message_text_render, font_size

    def _render_button_text(self, button_x, button_y):
        button_gap = 20

        for button_name in self.current_dialog["buttons"]:
            render = self.buttons[button_name]["render"]
            self.surface.blit(render, (button_x, button_y))
            self.buttons[button_name]["rect"] = Rect(
                self.x + button_x,
                self.y + button_y,
                render.get_width(),
                render.get_height()
            )
            button_x += render.get_width() + button_gap

    def _draw_buttons(self):
        if self.current_dialog:
            button_x, button_y = self._calculate_button_position()
            self._render_button_text(button_x, button_y)

    def _draw_messages(self):
        if self.current_dialog:
            message_texts = self.current_message.split("\n")

            y_offset = 20
            current_font_size = FONT_SIZE
            message_text_renders = []

            for message_text in message_texts:
                message_text_render, current_font_size = self._render_line(message_text, current_font_size)

            for message_text in message_texts:
                message_text_render, current_font_size = self._render_line(message_text, current_font_size)
                message_text_renders.append(message_text_render)

            message_height = sum(message_text_render.get_height() + 10 for message_text_render in message_text_renders)

            self.height = message_height + 80
            self.y = SCREEN_HEIGHT // 2 - self.height // 2

            self.surface = Surface((self.width, self.height))
            self.boarder_surface = Surface((self.width + 10, self.height + 10))

            self._fill_surfaces()
            self._draw_buttons()

            for message_text_render in message_text_renders:
                text_x = self.width // 2 - message_text_render.get_width() // 2
                self.surface.blit(message_text_render, (text_x, y_offset))
                y_offset += message_text_render.get_height() + 10

    def _draw(self):
        if not self.hidden:
            self._draw_messages()
            self._blit_surfaces()
            pygame.display.flip()

    def _draw_dialog(self):
        i = 1
        while i <= len(self.dialog_data):
            self.screen.fill(BLACK)

            self._load_message(f"message_{i}")
            self._draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.handle_event(event):
                    i += 1

    def _draw_message(self, restart_game, load_game):
        btn_flag = False

        while not btn_flag:
            self._draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.handle_event(event):
                    if self.button_pressed == "restart":
                        restart_game()
                    if self.button_pressed == "load":
                        load_game()

                    btn_flag = True

    def _get_name_and_draw(self):
        player_name = ""
        btn_flag = False

        while not btn_flag:
            self._load_message("plr_get_name")
            self.current_message = self.current_message.format(player_name=player_name)
            self._draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if len(player_name) > 0:
                            player_name = player_name[:-1]
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB \
                            or event.key == pygame.K_SPACE or event.key == pygame.K_DELETE:
                        pass
                    else:
                        if event.unicode not in "0123456789!@#$%^&*()-_+=<>.,:;/?|'\\\"~`{}[]" and len(player_name) < 8:
                            player_name += event.unicode

                if self.handle_event(event) and len(player_name) > 0:
                    btn_flag = True

        return player_name

    def show_message_ui(self, file_path, message_type: str, message_name="", restart_game=None, load_game=None,
                        monster=None, player=None, fill_black=True):
        if self._load_file_data(file_path):
            if fill_black:
                self.screen.fill(BLACK)
            if message_type == "dialog":
                self._draw_dialog()

            elif message_type == "message":
                self._load_message(f"{message_name}")
                if message_name == "plr_lvl_up":
                    self.current_message = self.current_message.format(
                        hp_bonus=player.level_up_hp_bonus[player.lvl - 2],
                        atk_bonus=player.level_up_atk_bonus[player.lvl - 2])

                elif message_name == "def_cd":
                    self.current_message = self.current_message.format(defense_cd=player.defense_cd)
                elif monster:
                    self.current_message = self.current_message.format(monster_name=monster.name,
                                                                       monster_exp=monster.exp)

                self._draw_message(restart_game, load_game)

            elif message_type == "name":
                player.name = self._get_name_and_draw()
            else:
                print("Unknown message type")

    def _clear(self):
        self.hidden = True
        self.current_message = ""
        self.font = font.Font(FONT_PATH, FONT_SIZE)
        for button_name, button_stats in self.buttons.items():
            button_stats["rect"] = Rect(0, 0, 0, 0)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            for button_name, button_stats in self.buttons.items():
                if button_stats["rect"].collidepoint(event.pos):
                    self.button_pressed = button_name
                    self._clear()
                    return True
            return False
