import pygame
import sys
from animatedsprite import AnimatedSprite
from monster import Monster
from player import Player

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Экран битвы")

background_image = pygame.image.load("Sprites/cave_bg.png").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

monster_sprite_frames = [pygame.image.load(f"Sprites/Skeleton/Idle/Skeleton_idle_{i}.png") for i in range(1, 4)]
for i in range(3):
    monster_sprite_frames[i] = pygame.transform.scale(monster_sprite_frames[i], (450, 450))
monster_sprite = AnimatedSprite(monster_sprite_frames, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
monster = Monster("Skeleton", 20, 5, 1, 100, monster_sprite)

all_sprites = pygame.sprite.Group()
all_sprites.add(monster.sprite)

clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(background_image, (0, 0))

    all_sprites.update(dt)

    screen.blit(background_image, (0, 0))

    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
