import pygame
import sys
from monster import Monster
from player import Player
from message import Message
import actionmenu
import infobar
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from save_load import save_game, load_game


def draw_screen(clock):
    frame_time = clock.tick(60) / 1000.0
    screen.blit(background_image, (0, 0))

    action_menu.draw(screen)
    info_bar.draw(screen, player, monster)

    all_sprites.update(frame_time)
    all_sprites.draw(screen)

    message.draw(screen)

    handle_monster_animation()

    pygame.display.flip()


def handle_monster_animation():
    if (monster.sprite.current_animation == "hurt"
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
            action_menu.handle_event(event, player, monster, reset_monster, save_game_callback, load_game_callback)
        message.handle_event(event)
    return True


def handle_player_death():
    message.current_message = "Вы погибли!\nХотите начать заново?"
    message.show_restart_button = True
    message.hidden = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        message.handle_event(event)
    if message.button_pressed == "exit":
        return False
    elif message.button_pressed == "restart":
        restart_game()
    return True


def handle_monster_death():
    if not monster.sprite.death_animation_started:
        monster.sprite.death_animation_started = True
        monster.sprite.set_animation("death")

    if monster.sprite.death_animation_complete:
        message.current_message = f"Вы получили {monster.exp} опыта!"
        message.hidden = False

    if monster.sprite.death_animation_complete and message.button_pressed == "ok":
        player.exp += monster.exp
        player.level_up(message)

        reset_monster()
        pygame.event.clear()
    return True


def restart_game():
    global player, monster, all_sprites
    player = Player("Likek", 40, 5, 1)
    monster = Monster()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(monster.sprite)
    message.clear()


def reset_monster():
    global monster
    monster.sprite.kill()
    monster = Monster()
    all_sprites.add(monster.sprite)


def clear_events_if_needed():
    if monster.sprite.current_animation in ["hurt", "death"]:
        pygame.event.clear()


def save_game_callback():
    save_game(player, monster, message)


def load_game_callback():
    global player, monster, message, all_sprites
    player, monster, message = load_game()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(monster.sprite)


def main():
    global monster, player, message, all_sprites
    clock = pygame.time.Clock()
    running = True
    while running:
        running = process_events()

        if player.hp <= 0:
            running = handle_player_death()
        elif monster.hp <= 0:
            running = handle_monster_death()

        clear_events_if_needed()

        if message.button_pressed:
            message.clear()

        draw_screen(clock)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Экран битвы")

    background_image = pygame.image.load("Sprites/cave_bg.png").convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    monster = Monster()

    player = Player("Likek", 40, 5, 1)

    message = Message()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(monster.sprite)

    action_menu = actionmenu.ActionMenu()
    info_bar = infobar.Infobar()

    main()
