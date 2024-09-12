import pygame
import sys
from monster import Monster
from player import Player
from message_ui import MessageUI
from actionmenu import ActionMenu
from infobox import Infobox
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN
from save_load import save_game, load_game


def draw_screen(clock):
    frame_time = clock.tick(60) / 1000.0
    SCREEN.blit(background_image, (0, 0))

    action_menu.draw()
    info_box.draw(player, monster)

    all_sprites.update(frame_time)
    all_sprites.draw(SCREEN)

    handle_monster_animation()

    pygame.display.flip()


def handle_monster_animation():
    if (monster.sprite.current_animation == "hurt"
            and monster.sprite.current_frame_index == len(monster.sprite.current_frames) - 1):
        monster.sprite.set_animation("attack")
    elif (monster.sprite.current_animation == "attack"
          and monster.sprite.current_frame_index == len(monster.sprite.current_frames) - 1):
        monster.sprite.set_animation("idle")
    elif (monster.sprite.current_animation == "death"
          and monster.sprite.current_frame_index == len(monster.sprite.current_frames) - 1):
        monster.sprite.death_animation_complete = True


def process_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if monster.sprite.current_animation == "idle":
            action_menu.handle_event(event, player, monster, message, reset_monster, save_game_callback,
                                     load_game_callback)
    return True


def handle_player_death():
    message.show_message_ui("jsons/messages.json", "message", message_name="plr_death",
                            restart_game=restart_game, load_game=load_game_callback)


def handle_monster_death():
    if not monster.sprite.death_animation_started:
        monster.sprite.death_animation_started = True
        monster.sprite.set_animation("death")

    if monster.sprite.death_animation_complete:
        message.show_message_ui("jsons/messages.json", "message", message_name="enemy_death",
                                monster=monster, fill_black=False)
        if player.level_up(monster.exp):
            message.show_message_ui("jsons/messages.json", "message", message_name="plr_lvl_up",
                                    player=player, fill_black=False)

        reset_monster()
        pygame.event.clear()


def handle_final_cond():
    if player.lvl == 5:
        pass


def start_final_part():
    message.show_message_ui("jsons/story_part_final.json", "dialogue")


def restart_game():
    show_start_story()
    create_monster()


def reset_monster():
    monster.sprite.kill()

    create_monster()


def create_monster():
    global monster
    monster = Monster()
    all_sprites.add(monster.sprite)

    message.show_message_ui("jsons/messages.json", "message", message_name="enemy_greeting",
                            monster=monster)


def clear_events_if_needed():
    if monster.sprite.current_animation in ["hurt", "death"]:
        pygame.event.clear()


def save_game_callback():
    save_game(player, monster)


def load_game_callback():
    global player, monster, all_sprites
    try:
        player, monster = load_game()
        all_sprites = pygame.sprite.Group()
        all_sprites.add(monster.sprite)
    except Exception:
        pass


def check_save_file():
    try:
        open("save.pkl")
        message.show_message_ui("jsons/messages.json", "message", message_name="load_game_offer")
        if message.button_pressed == "yes":
            return True
        else:
            return False
    except FileNotFoundError:
        return False


def show_start_story():
    message.show_message_ui("jsons/messages.json", "name", player=player)

    message.show_message_ui("jsons/story_part_1.json", "dialog")
    message.show_message_ui("jsons/story_part_2.1.json", "dialog")

    message.show_message_ui("jsons/messages.json", "message", message_name="part_2_choice")
    if message.button_pressed == "no":
        message.show_message_ui("jsons/story_ending_1.json", "dialog")
        handle_player_death()
    elif message.button_pressed == "yes":
        message.show_message_ui("jsons/story_part_2.2.json", "dialog")
        message.show_message_ui("jsons/story_part_3.json", "dialog")


def main():
    global running
    clock = pygame.time.Clock()
    while running:
        running = process_events()

        if player.hp <= 0:
            handle_player_death()
        elif monster.hp <= 0:
            handle_monster_death()

        clear_events_if_needed()

        draw_screen(clock)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    pygame.init()

    pygame.display.set_caption("Моя игруха")

    try:
        background_image = pygame.image.load("Sprites/cave_bg.png").convert()
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except FileNotFoundError:
        print("background image not found")

    all_sprites = pygame.sprite.Group()

    player = Player()
    monster = Monster()

    message = MessageUI()

    action_menu = ActionMenu()
    info_box = Infobox()

    if check_save_file():
        load_game_callback()
    else:
        show_start_story()
        create_monster()

    running = True
    main()
