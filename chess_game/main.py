import pygame
import sys
from config import config
from game import ChessGame


def main():
    # Инициализация pygame
    pygame.init()

    # Получаем настройки
    width = config.get('window.width', 800)
    height = config.get('window.height', 800)
    title = config.get('window.title', 'Шахматы')

    # Создаём окно
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)

    # Запускаем игру
    game = ChessGame(screen, config)
    game.run()


if __name__ == "__main__":
    main()