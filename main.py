import pygame
import sys

# Инициализация Pygame
pygame.init()

# Определение размеров окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Создание окна Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("UTP")

# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Здесь будет ваш игровой код

    # Отображение изменений
    pygame.display.flip()

# Выход из игры
pygame.quit()
sys.exit()
