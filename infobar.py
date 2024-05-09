import monster
from pygame import font, Surface
from constants import BLACK, WHITE, SCREEN_HEIGHT, SCREEN_WIDTH

class Infobar:
    def __init__(self):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT // 10
        self.x = 0
        self.y = 0
        self.surface = Surface((self.width, self.height))
        self.font = font.Font("Fonts/determination.otf", 21)
        self.stats = ["Здоровье: ", "Уровень: ", "Атака: "]

    def draw(self, screen: Surface, monster: monster.Monster):
        self.surface.fill(BLACK)

        x_offset = 0

        name_text_render = self.font.render(str(monster.name), True, WHITE)
        if name_text_render.get_width() > 147:
            x_offset = name_text_render.get_width() - 120
        hp_text_render = self.font.render(self.stats[0] + str(monster.hp), True, WHITE)
        lvl_text_render = self.font.render(self.stats[1] +str(monster.lvl), True, WHITE)
        atk_text_render = self.font.render(self.stats[2] +str(monster.atk), True, WHITE)

        self.surface.blit(name_text_render, (10, self.height // 2 - name_text_render.get_height() // 2))
        self.surface.blit(hp_text_render, (177 + x_offset, self.height // 2 - hp_text_render.get_height() // 2))
        self.surface.blit(lvl_text_render, (357 + x_offset, self.height // 2 - lvl_text_render.get_height() // 2))
        self.surface.blit(atk_text_render, (517 + x_offset, self.height // 2 - atk_text_render.get_height() // 2))

        screen.blit(self.surface, (self.x, self.y))
