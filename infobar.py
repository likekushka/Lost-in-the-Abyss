from monster import Monster
from player import Player
from pygame import font, Surface
from constants import BLACK, WHITE, SCREEN_HEIGHT, SCREEN_WIDTH


class Infobar:
    def __init__(self):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT // 10

        self.x = 0
        self.y = 0

        self.monster_surface = Surface((self.width, self.height))
        self.player_surface = Surface((self.width, self.height))
        self.surface = Surface((self.width, self.height))

        self.font = font.Font("Fonts/determination.otf", 21)
        self.stats = ["Здоровье: ", "Уровень: ", "Атака: ", "Опыт: "]

    def draw(self, screen: Surface, player: Player, monster: Monster):
        self._draw_character_info(screen, player, is_player=True)
        self._draw_character_info(screen, monster, is_player=False)

    def _draw_character_info(self, screen: Surface, character, is_player: bool):
        self.surface.fill(BLACK)

        name_text_render = self._render_text(str(character.name))
        hp_text_render = self._render_text(f"{self.stats[0]}{character.hp}/{character.max_hp}")
        lvl_text_render = self._render_text(f"{self.stats[1]}{character.lvl}")
        atk_text_render = self._render_text(f"{self.stats[2]}{character.atk}")
        exp_text_render = self._render_text(
            f"{self.stats[3]}{character.exp}/{character.level_up_exp[character.lvl - 1]}"
            if is_player else f"{self.stats[3]}{character.exp}"
        )

        total_width, gap_width = self._calculate_widths(
            name_text_render, hp_text_render, lvl_text_render, atk_text_render, exp_text_render
        )

        self._blit_texts(name_text_render, hp_text_render, lvl_text_render, atk_text_render, exp_text_render, gap_width)

        self.y = SCREEN_HEIGHT - self.height if is_player else 0
        screen.blit(self.surface, (self.x, self.y))

    def _render_text(self, text: str) -> Surface:
        return self.font.render(text, True, WHITE)

    def _calculate_widths(self, *renders) -> tuple:
        widths = [render.get_width() for render in renders]
        total_width = sum(widths)
        gap_width = (self.width - total_width) // 5
        return total_width, gap_width

    def _blit_texts(self, name_render, hp_render, lvl_render, atk_render, exp_render, gap_width):
        x_offset = 10
        renders = [name_render, hp_render, atk_render, lvl_render, exp_render]
        for render in renders:
            self.surface.blit(render, (x_offset, self.height // 2 - render.get_height() // 2))
            x_offset += render.get_width() + gap_width
