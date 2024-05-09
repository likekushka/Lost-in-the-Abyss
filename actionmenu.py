from pygame import font, Surface, Rect, MOUSEBUTTONDOWN
from monster import Monster
from player import Player
from constants import BLACK, WHITE, SCREEN_HEIGHT, SCREEN_WIDTH

class ActionMenu:
    def __init__(self):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT // 2
        self.x = 0
        self.y = SCREEN_HEIGHT // 2
        self.font = font.Font("Fonts/determination.otf", 40)
        self.surface = Surface((self.width, self.height))
        self.buttons = [
            {"text": "Атака", "rect": None},
            {"text": "Защита", "rect": None},
            {"text": "Сбежать", "rect": None}]

    def draw(self, screen: Surface):
        self.surface.fill(BLACK)

        y_offset = 50
        for button in self.buttons:
            text_render = self.font.render(button["text"], True, WHITE)
            self.surface.blit(text_render, (10, y_offset))
            button["rect"] = Rect(10, self.y + y_offset, text_render.get_width(), text_render.get_height())
            y_offset += 50

        screen.blit(self.surface, (self.x, self.y))

    def handle_event(self, event, player: Player, monster: Monster):
        if event.type == MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    if button["text"] == "Атака":
                        player.attack(monster)
