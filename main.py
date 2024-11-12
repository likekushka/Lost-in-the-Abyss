import pygame
import sys
from monster import Monster
from player import Player
from message_ui import MessageUI
from actionmenu import ActionMenu
from infobox import Infobox
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from save_load import save_game, load_game


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Покинутый в бездне")

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        try:
            self.background_image = pygame.image.load("Sprites/cave_bg.png").convert()
            self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except FileNotFoundError:
            print("Background image not found")

        self.all_sprites = pygame.sprite.Group()

        self.message = MessageUI(self.screen)

        self.action_menu = ActionMenu()
        self.info_box = Infobox()

        self.player = Player()
        self.monster = None

        if self.check_save():
            self.load_game()
        else:
            while True:
                if self.show_start_story():
                    self.create_monster()
                    break
                elif self.monster:
                    break

        self.running = True

    def draw_screen(self):
        frame_time = self.clock.tick(60) / 1000.0
        self.screen.blit(self.background_image, (0, -SCREEN_HEIGHT//2))

        self.action_menu.draw(self.screen)
        self.info_box.draw(self.player, self.monster, self.screen)

        self.all_sprites.update(frame_time)
        self.all_sprites.draw(self.screen)

        self.handle_monster_animation()

        pygame.display.flip()

    def handle_monster_animation(self):
        sprite = self.monster.sprite
        if sprite.current_animation == "hurt" and sprite.current_frame_index == len(sprite.current_frames) - 1:
            sprite.set_animation("attack") if self.monster.hp > 0 else sprite.set_animation("death")
        elif sprite.current_animation == "attack" and sprite.current_frame_index == len(sprite.current_frames) - 1:
            sprite.set_animation("idle")
        elif sprite.current_animation == "death" and sprite.current_frame_index == len(sprite.current_frames) - 1:
            sprite.death_animation_complete = True

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.monster.sprite.current_animation == "idle":
                self.action_menu.handle_event(event, self.player, self.monster, self.message, self.reset_monster,
                                              self.save_game, self.load_game)

    def handle_player_death(self):
        self.message.show_message_ui("jsons/messages.json", "message", message_name="plr_death",
                                     restart_game=self.restart_game, load_game=self.load_game)

    def handle_monster_death(self):
        if self.monster.sprite.death_animation_complete:
            if not self.monster.boss_status:
                self.message.show_message_ui("jsons/messages.json", "message",
                                             message_name="enemy_death", monster=self.monster, fill_black=False)
                if self.player.level_up(self.monster.exp):
                    self.message.show_message_ui("jsons/messages.json", "message",
                                                 message_name="plr_lvl_up", player=self.player, fill_black=False)
                self.reset_monster()
                pygame.event.clear()
            else:
                pygame.time.delay(500)

                for i in range(0, 255, 5):
                    self.screen.fill((i, i, i))
                    pygame.display.flip()
                    self.clock.tick(60)

                self.screen.fill(WHITE)
                pygame.display.flip()
                pygame.time.delay(1500)

                self.message.show_message_ui("jsons/story_part_final.json", "dialog")
                self.message.show_message_ui("jsons/messages.json", "message",
                                             message_name="boss_death", restart_game=self.restart_game,
                                             load_game=self.load_game)

    def restart_game(self):
        self.player = Player()
        self.show_start_story()
        self.reset_monster() if self.monster else self.create_monster()

    def reset_monster(self):
        self.monster.sprite.kill()
        if self.player.lvl < 5:
            self.create_monster()
        else:
            self.create_boss_monster()

    def create_monster(self):
        self.monster = Monster()
        self.all_sprites.add(self.monster.sprite)
        self.message.show_message_ui("jsons/messages.json", "message",
                                     message_name="enemy_greeting", monster=self.monster)

    def create_boss_monster(self):
        self.monster = Monster(boss_status=True)
        self.all_sprites.add(self.monster.sprite)
        self.message.show_message_ui("jsons/story_part_4.json", "dialog")

    def clear_events(self):
        if self.monster.sprite.current_animation in ["hurt", "death"]:
            pygame.event.clear()

    def save_game(self):
        save_game(self.player, self.monster, self.message)

    def load_game(self):
        try:
            self.player, self.monster = load_game(self.message)
            self.all_sprites = pygame.sprite.Group()
            self.all_sprites.add(self.monster.sprite)
        except Exception:
            pass

    def check_save(self):
        try:
            open("save.pkl")
            self.message.show_message_ui("jsons/messages.json", "message",
                                         message_name="load_game_offer")
            return self.message.button_pressed == "yes"
        except FileNotFoundError:
            return False

    def show_start_story(self):
        self.message.show_message_ui("jsons/messages.json", "name", player=self.player)
        self.message.show_message_ui("jsons/story_part_1.json", "dialog")
        self.message.show_message_ui("jsons/story_part_2.1.json", "dialog")
        self.message.show_message_ui("jsons/messages.json", "message",
                                     message_name="part_2_choice")
        if self.message.button_pressed == "no":
            self.message.show_message_ui("jsons/story_bad_ending.json", "dialog")
            self.handle_player_death()
            return False
        elif self.message.button_pressed == "yes":
            self.message.show_message_ui("jsons/story_part_2.2.json", "dialog")
            self.message.show_message_ui("jsons/story_part_3.json", "dialog")
            return True

    def main(self):
        while self.running:
            self.process_events()
            self.clear_events()
            self.draw_screen()

            if self.player.hp <= 0 and self.monster.sprite.current_animation == "idle":
                self.handle_player_death()
            elif self.monster.hp <= 0:
                self.handle_monster_death()

        self.save_game()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.main()
