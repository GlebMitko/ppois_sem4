import pygame
import json
import os


class Menu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font_title = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        self.options = ["Начать игру", "Таблица рекордов", "Справка", "Выход"]
        self.selected = 0

    def draw(self):
        self.screen.fill((30, 30, 40))

        # Заголовок
        title = self.font_title.render("ШАХМАТЫ", True, (255, 215, 0))
        title_rect = title.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title, title_rect)

        # Меню
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i != self.selected else (255, 215, 0)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(self.width // 2, 250 + i * 60))
            self.screen.blit(text, rect)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.selected
        return None


class HighScores:
    def __init__(self):
        self.filename = "highscores.json"
        self.scores = self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return []

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.scores, f, indent=2)

    def add_score(self, name, moves):
        self.scores.append({"name": name, "moves": moves, "date": str(pygame.time.get_ticks())})
        self.scores.sort(key=lambda x: x['moves'])
        self.scores = self.scores[:10]
        self.save()

    def is_high_score(self, moves):
        if len(self.scores) < 10:
            return True
        return moves < self.scores[-1]['moves']

    def draw(self, screen, width, height):
        screen.fill((30, 30, 40))

        title = pygame.font.Font(None, 72).render("ТАБЛИЦА РЕКОРДОВ", True, (255, 215, 0))
        title_rect = title.get_rect(center=(width // 2, 80))
        screen.blit(title, title_rect)

        font = pygame.font.Font(None, 36)
        y = 180
        for i, score in enumerate(self.scores[:10]):
            text = font.render(f"{i + 1}. {score['name']} - {score['moves']} ходов", True, (255, 255, 255))
            rect = text.get_rect(center=(width // 2, y))
            screen.blit(text, rect)
            y += 40

        back = pygame.font.Font(None, 32).render("Нажми ESC для возврата", True, (150, 150, 150))
        back_rect = back.get_rect(center=(width // 2, height - 50))
        screen.blit(back, back_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False
                if event.type == pygame.QUIT:
                    return False
        return True


class HelpScreen:
    def draw(self, screen, width, height):
        screen.fill((30, 30, 40))

        title = pygame.font.Font(None, 72).render("СПРАВКА", True, (255, 215, 0))
        title_rect = title.get_rect(center=(width // 2, 60))
        screen.blit(title, title_rect)

        # Загружаем правила из файла
        font = pygame.font.Font(None, 24)
        y = 120

        try:
            with open("configs/help.txt", 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines[:30]:
                    text = font.render(line.strip(), True, (200, 200, 200))
                    rect = text.get_rect(center=(width // 2, y))
                    screen.blit(text, rect)
                    y += 25
        except:
            # Если файла нет, показываем краткие правила
            rules = [
                "ПРАВИЛА ИГРЫ В ШАХМАТЫ:",
                "",
                "Цель: поставить мат королю противника.",
                "Белые ходят первыми.",
                "После каждого хода доска переворачивается.",
                "",
                "Фигуры:",
                "Пешка - ходит вперёд на 1, бьёт по диагонали",
                "Ладья - по горизонтали и вертикали",
                "Конь - буквой 'Г'",
                "Слон - по диагонали",
                "Ферзь - по всем направлениям",
                "Король - на 1 клетку в любую сторону"
            ]
            for rule in rules:
                text = font.render(rule, True, (200, 200, 200))
                rect = text.get_rect(center=(width // 2, y))
                screen.blit(text, rect)
                y += 25

        back = pygame.font.Font(None, 32).render("Нажми ESC для возврата", True, (150, 150, 150))
        back_rect = back.get_rect(center=(width // 2, height - 50))
        screen.blit(back, back_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False
                if event.type == pygame.QUIT:
                    return False
        return True