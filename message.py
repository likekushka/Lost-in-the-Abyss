from constants import SCREEN_HEIGHT, SCREEN_WIDTH, BLACK, WHITE
from pygame import Rect, Surface, font, MOUSEBUTTONDOWN


class Message:
    def __init__(self):
        self.width = 500
        self.height = 400

        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT // 2 - self.height // 2

        self.hidden = True
        self.current_message = ""
        self.show_restart_button = False

        self.font = font.Font("Fonts/determination.otf", 40)

        self.surface = Surface((self.width, self.height))
        self.boarder_surface = Surface((self.width + 10, self.height + 10))

        self.buttons = {
            "ok": {"render": self.font.render("OK", True, WHITE), "rect": Rect(0, 0, 0, 0)},
            "restart": {"render": self.font.render("Заново", True, WHITE), "rect": Rect(0, 0, 0, 0)},
            "exit": {"render": self.font.render("Выйти", True, WHITE), "rect": Rect(0, 0, 0, 0)}
        }
        self.button_pressed = None

    def draw(self, screen):
        if not self.hidden:
            self._fill_surfaces()
            self._draw_buttons()
            self._draw_messages()
            self._blit_surfaces(screen)

    def _fill_surfaces(self):
        self.surface.fill(BLACK)
        self.boarder_surface.fill(WHITE)

    def _draw_buttons(self):
        button_y = self.height - self.buttons["ok"]["render"].get_height() // 2 - 30

        if self.show_restart_button:
            # Calculate positions for restart and exit buttons
            restart_button_width = self.buttons["restart"]["render"].get_width()
            exit_button_width = self.buttons["exit"]["render"].get_width()
            gap = 100 # Gap between buttons
            total_buttons_width = restart_button_width + exit_button_width + gap
            restart_x = self.width // 2 - total_buttons_width // 2
            exit_x = restart_x + restart_button_width + gap

            # Draw and set rects for buttons
            self.surface.blit(self.buttons["restart"]["render"], (restart_x, button_y))
            self.surface.blit(self.buttons["exit"]["render"], (exit_x, button_y))

            self.buttons["restart"]["rect"] = Rect(
                self.x + restart_x,
                self.y + button_y,
                restart_button_width,
                self.buttons["restart"]["render"].get_height()
            )
            self.buttons["exit"]["rect"] = Rect(
                self.x + exit_x,
                self.y + button_y,
                exit_button_width,
                self.buttons["exit"]["render"].get_height()
            )
        else:
            ok_x = self.width // 2 - self.buttons["ok"]["render"].get_width() // 2
            self.surface.blit(self.buttons["ok"]["render"], (ok_x, button_y))

            self.buttons["ok"]["rect"] = Rect(
                self.x + ok_x,
                self.y + button_y,
                self.buttons["ok"]["render"].get_width(),
                self.buttons["ok"]["render"].get_height()
            )

    def _draw_messages(self):
        message_texts = self.current_message.split("\n")
        y_offset = -50 if len(message_texts) > 1 else 0

        current_font_size = 40

        for message_text in message_texts:
            message_text_render = self._render_message_text(message_text, current_font_size)
            text_x = self.width // 2 - message_text_render.get_width() // 2
            text_y = self.height // 2 + y_offset - message_text_render.get_height() // 2
            self.surface.blit(message_text_render, (text_x, text_y))
            y_offset += 50

    def _render_message_text(self, text, font_size):
        message_text_render = self.font.render(text, True, WHITE)
        while message_text_render.get_width() > self.width - 10 and font_size > 25:
            font_size -= 1
            self.font = font.Font("Fonts/determination.otf", font_size)
            message_text_render = self.font.render(text, True, WHITE)
        return message_text_render

    def _blit_surfaces(self, screen):
        screen.blit(self.boarder_surface, (self.x, self.y))
        screen.blit(self.surface, (self.x + 5, self.y + 5))

    def clear(self):
        self.hidden = True
        self.current_message = ""
        self.show_restart_button = False
        self.font = font.Font("Fonts/determination.otf", 40)
        self.buttons["ok"]["rect"] = Rect(0, 0, 0, 0)
        self.buttons["restart"]["rect"] = Rect(0, 0, 0, 0)
        self.buttons["exit"]["rect"] = Rect(0, 0, 0, 0)
        self.button_pressed = None

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.buttons["ok"]["rect"].collidepoint(event.pos):
                self.button_pressed = "ok"
            elif self.buttons["restart"]["rect"].collidepoint(event.pos):
                self.button_pressed = "restart"
            elif self.buttons["exit"]["rect"].collidepoint(event.pos):
                self.button_pressed = "exit"

