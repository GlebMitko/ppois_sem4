import pygame
import sys
import os
from board import ChessBoard
from menu import Menu, HighScores, HelpScreen


class ChessGame:
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.width = config.get('window.width', 800)
        self.height = config.get('window.height', 800)
        self.cell_size = config.get('board.cell_size', 80)
        self.light_color = config.get('board.light_color', [240, 217, 181])
        self.dark_color = config.get('board.dark_color', [181, 136, 99])

        self.board = ChessBoard()
        self.menu = Menu(screen, self.width, self.height)
        self.high_scores = HighScores()
        self.help_screen = HelpScreen()

        self.running = True
        self.in_game = False
        self.white_bottom = True
        self.move_count = 0

        # Инициализация звуков
        pygame.mixer.init()
        self.sound_move = None
        self.sound_capture = None
        self.sound_enabled = True
        self.music_enabled = True

        self.load_sounds()
        self.play_music()

        # Загружаем изображения фигур
        self.piece_images = self.load_piece_images()

    def load_sounds(self):
        """Загружает звуковые эффекты"""
        base_path = os.path.dirname(__file__)

        # Звук хода
        move_path = os.path.join(base_path, 'sounds', 'move.mp3')
        if os.path.exists(move_path):
            try:
                self.sound_move = pygame.mixer.Sound(move_path)
                self.sound_move.set_volume(0.7)
                print("✓ Звук хода загружен")
            except Exception as e:
                print(f"✗ Ошибка загрузки move.mp3: {e}")
        else:
            print(f"✗ Файл не найден: {move_path}")

        # Звук взятия
        capture_path = os.path.join(base_path, 'sounds', 'beat.mp3')
        if os.path.exists(capture_path):
            try:
                self.sound_capture = pygame.mixer.Sound(capture_path)
                self.sound_capture.set_volume(0.7)
                print("✓ Звук взятия загружен")
            except Exception as e:
                print(f"✗ Ошибка загрузки beat.mp3: {e}")
        else:
            print(f"✗ Файл не найден: {capture_path}")

    def play_music(self):
        """Воспроизводит фоновую музыку"""
        if not self.music_enabled:
            return

        base_path = os.path.dirname(__file__)
        music_path = os.path.join(base_path, 'sounds', 'background.mp3')

        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
                print("✓ Фоновая музыка играет")
            except Exception as e:
                print(f"✗ Ошибка музыки: {e}")
        else:
            print(f"✗ Музыка не найдена: {music_path}")

    def play_move_sound(self):
        """Воспроизводит звук хода (только при перемещении на пустое поле)"""
        if self.sound_enabled and self.sound_move:
            try:
                self.sound_move.play()
                print("Звук хода")  # Для отладки
            except Exception as e:
                print(f"Ошибка воспроизведения move: {e}")

    def play_capture_sound(self):
        """Воспроизводит звук взятия"""
        if self.sound_enabled and self.sound_capture:
            try:
                self.sound_capture.play()
                print("Звук взятия")  # Для отладки
            except Exception as e:
                print(f"Ошибка воспроизведения capture: {e}")

    def load_piece_images(self):
        """Загружает изображения всех фигур"""
        images = {}
        pieces = ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']
        colors = ['white', 'black']

        base_path = os.path.dirname(__file__)

        for color in colors:
            for piece in pieces:
                key = f"{color}_{piece}"
                path = os.path.join(base_path, 'assets', 'pieces', f"{key}.png")

                try:
                    if os.path.exists(path):
                        img = pygame.image.load(path)
                        img = pygame.transform.scale(img, (self.cell_size - 10, self.cell_size - 10))
                        images[key] = img
                    else:
                        # Создаём заглушку
                        surf = pygame.Surface((self.cell_size - 10, self.cell_size - 10), pygame.SRCALPHA)
                        color_val = (255, 255, 255) if color == 'white' else (80, 80, 80)
                        pygame.draw.circle(surf, color_val, (surf.get_width() // 2, surf.get_height() // 2),
                                           surf.get_width() // 3)

                        font = pygame.font.Font(None, 40)
                        letter = {'king': 'K', 'queen': 'Q', 'rook': 'R', 'bishop': 'B', 'knight': 'N', 'pawn': 'P'}[
                            piece]
                        text = font.render(letter, True, (0, 0, 0) if color == 'white' else (255, 255, 255))
                        text_rect = text.get_rect(center=(surf.get_width() // 2, surf.get_height() // 2))
                        surf.blit(text, text_rect)
                        images[key] = surf
                except Exception as e:
                    print(f"Ошибка загрузки {key}: {e}")

        return images

    def draw_board(self):
        display_board = self.board.get_board_for_display(self.white_bottom)

        for row in range(8):
            for col in range(8):
                color = self.light_color if (row + col) % 2 == 0 else self.dark_color
                rect = pygame.Rect(col * self.cell_size, row * self.cell_size,
                                   self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)

                if self.board.selected_piece:
                    actual_row, actual_col = self.board.selected_piece.get_pos()
                    if not self.white_bottom:
                        actual_row, actual_col = 7 - actual_row, 7 - actual_col
                    if (row, col) == (actual_row, actual_col):
                        pygame.draw.rect(self.screen, (255, 255, 0), rect, 5)

                for move in self.board.valid_moves:
                    move_row, move_col = move
                    if not self.white_bottom:
                        move_row, move_col = 7 - move_row, 7 - move_col
                    if (row, col) == (move_row, move_col):
                        s = pygame.Surface((self.cell_size, self.cell_size))
                        s.set_alpha(128)
                        s.fill((0, 255, 0))
                        self.screen.blit(s, (col * self.cell_size, row * self.cell_size))

                piece = display_board[row][col]
                if piece:
                    image_key = f"{piece.color}_{piece.__class__.__name__.lower()}"
                    if image_key in self.piece_images:
                        img = self.piece_images[image_key]
                        x = col * self.cell_size + (self.cell_size - img.get_width()) // 2
                        y = row * self.cell_size + (self.cell_size - img.get_height()) // 2
                        self.screen.blit(img, (x, y))

        turn_text = f"Ход: {'Белые' if self.board.current_turn == 'white' else 'Чёрные'}"
        turn_surface = pygame.font.Font(None, 36).render(turn_text, True, (255, 255, 255))
        self.screen.blit(turn_surface, (10, self.height - 40))

        moves_text = f"Ходов: {self.move_count}"
        moves_surface = pygame.font.Font(None, 36).render(moves_text, True, (255, 255, 255))
        self.screen.blit(moves_surface, (self.width - 120, self.height - 40))

    def show_promotion_dialog(self, color):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        dialog_width = 400
        dialog_height = 150
        dialog_x = (self.width - dialog_width) // 2
        dialog_y = (self.height - dialog_height) // 2

        pygame.draw.rect(self.screen, (50, 50, 50), (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(self.screen, (100, 100, 100), (dialog_x, dialog_y, dialog_width, dialog_height), 3)

        font = pygame.font.Font(None, 28)
        text = font.render(f"Выберите фигуру для превращения пешки ({'Белые' if color == 'white' else 'Чёрные'})",
                           True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.width // 2, dialog_y + 40))
        self.screen.blit(text, text_rect)

        pieces = [
            {'name': 'Ферзь', 'type': 'queen', 'color': (255, 215, 0), 'key': pygame.K_q},
            {'name': 'Ладья', 'type': 'rook', 'color': (150, 150, 150), 'key': pygame.K_r},
            {'name': 'Слон', 'type': 'bishop', 'color': (100, 200, 100), 'key': pygame.K_b},
            {'name': 'Конь', 'type': 'knight', 'color': (200, 150, 100), 'key': pygame.K_n}
        ]

        button_width = 80
        button_height = 40
        start_x = (self.width - (button_width * 4 + 30)) // 2
        buttons = []

        for i, piece in enumerate(pieces):
            x = start_x + i * (button_width + 10)
            y = dialog_y + 80
            rect = pygame.Rect(x, y, button_width, button_height)

            pygame.draw.rect(self.screen, piece['color'], rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)

            btn_font = pygame.font.Font(None, 20)
            btn_text = btn_font.render(piece['name'], True, (0, 0, 0))
            btn_rect = btn_text.get_rect(center=rect.center)
            self.screen.blit(btn_text, btn_rect)

            buttons.append({'rect': rect, 'type': piece['type'], 'key': piece['key']})

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'queen'
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in buttons:
                        if button['rect'].collidepoint(mouse_pos):
                            return button['type']
                elif event.type == pygame.KEYDOWN:
                    for button in buttons:
                        if event.key == button['key']:
                            return button['type']

    def handle_click(self, pos):
        if not self.in_game:
            return

        col = pos[0] // self.cell_size
        row = pos[1] // self.cell_size

        if 0 <= row < 8 and 0 <= col < 8:
            if not self.white_bottom:
                row, col = 7 - row, 7 - col

            if self.board.selected_piece is None:
                # Выбор фигуры - НИКАКОГО ЗВУКА!
                self.board.select_piece(row, col)
            else:
                # Проверяем, будет ли взятие
                target = self.board.board[row][col]
                is_capture = target is not None and target.color != self.board.selected_piece.color

                # Сохраняем старую позицию для проверки
                old_row, old_col = self.board.selected_piece.row, self.board.selected_piece.col

                success, is_capture_result, pawn_to_promote = self.board.make_move(row, col)

                if success:
                    self.move_count += 1

                    # Воспроизводим звук ТОЛЬКО при успешном перемещении
                    if is_capture:
                        print("Взятие!")  # Для отладки
                        self.play_capture_sound()  # Звук взятия
                    else:
                        print("Ход!")  # Для отладки
                        self.play_move_sound()  # Звук хода

                    # Превращение пешки
                    if pawn_to_promote:
                        chosen_piece = self.show_promotion_dialog(pawn_to_promote.color)
                        self.board.promote_pawn(pawn_to_promote, chosen_piece)

                    self.white_bottom = not self.white_bottom

                    # Проверка на мат
                    if self.board.is_checkmate():
                        winner = "Чёрные" if self.board.current_turn == 'white' else "Белые"
                        self.end_game(winner)
                else:
                    # Если кликнули на другую свою фигуру - выбираем её
                    self.board.select_piece(row, col)

    def end_game(self, winner):
        self.in_game = False

        font = pygame.font.Font(None, 48)
        text = font.render(f"ПОБЕДА! {winner} выиграли!", True, (255, 215, 0))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)

        if self.high_scores.is_high_score(self.move_count):
            self.enter_name_for_record()

        self.board = ChessBoard()
        self.white_bottom = True
        self.move_count = 0

    def enter_name_for_record(self):
        font = pygame.font.Font(None, 36)
        input_text = ""
        active = True

        while active:
            self.screen.fill((30, 30, 40))

            title = font.render(f"НОВЫЙ РЕКОРД! {self.move_count} ходов", True, (255, 215, 0))
            title_rect = title.get_rect(center=(self.width // 2, self.height // 2 - 100))
            self.screen.blit(title, title_rect)

            prompt = font.render("Введите ваше имя:", True, (255, 255, 255))
            prompt_rect = prompt.get_rect(center=(self.width // 2, self.height // 2 - 30))
            self.screen.blit(prompt, prompt_rect)

            name_surface = font.render(input_text, True, (255, 255, 255))
            name_rect = name_surface.get_rect(center=(self.width // 2, self.height // 2 + 20))
            pygame.draw.rect(self.screen, (100, 100, 100),
                             (name_rect.x - 10, name_rect.y - 5, name_rect.width + 20, name_rect.height + 10))
            self.screen.blit(name_surface, name_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and input_text:
                        self.high_scores.add_score(input_text, self.move_count)
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        active = False
                    else:
                        if len(input_text) < 20:
                            input_text += event.unicode

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            if not self.in_game:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        choice = self.menu.handle_event(event)
                        if choice == 0:
                            self.in_game = True
                            self.board = ChessBoard()
                            self.white_bottom = True
                            self.move_count = 0
                        elif choice == 1:
                            if not self.high_scores.draw(self.screen, self.width, self.height):
                                self.running = False
                        elif choice == 2:
                            if not self.help_screen.draw(self.screen, self.width, self.height):
                                self.running = False
                        elif choice == 3:
                            self.running = False

                self.menu.draw()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_click(event.pos)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.in_game = False

                self.screen.fill((0, 0, 0))
                self.draw_board()
                pygame.display.flip()

            clock.tick(60)

        pygame.quit()
        sys.exit()