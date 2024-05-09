import pygame
import sys
import monster
import actionmenu
import infobar
from player import Player
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Экран битвы")

background_image = pygame.image.load("Sprites/cave_bg.png").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

skeleton = monster.Monster("Скелет", 20, 5, 1, 100)
skeleton.sprite_load("Sprites/Skeleton/")

player = Player("Likek", 10, 5, 1)

all_sprites = pygame.sprite.Group()
all_sprites.add(skeleton.sprite)

action_menu = actionmenu.ActionMenu()
info_bar = infobar.Infobar()


def draw_screen(clock):
    frame_time = clock.tick(60) / 1000.0

    screen.blit(background_image, (0, 0))

    all_sprites.update(frame_time)
    all_sprites.draw(screen)

    action_menu.draw(screen)
    info_bar.draw(screen, skeleton)

    pygame.display.flip()


def main():
    global skeleton
    clock = pygame.time.Clock()
    running = True
    while running:
        if skeleton.hp <= 0:
            skeleton.sprite.kill()
            skeleton = monster.Monster("Скелет", 20, 5, 1, 100)
            skeleton.sprite_load("Sprites/Skeleton/")
            all_sprites.add(skeleton.sprite)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            action_menu.handle_event(event, player, skeleton)
        draw_screen(clock)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
