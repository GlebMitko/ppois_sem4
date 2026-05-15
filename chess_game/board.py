import pygame
from pieces import *


class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = 'white'  # белые ходят первыми
        self.selected_piece = None
        self.valid_moves = []
        self.setup_board()

    def setup_board(self):
        # Пешки
        for col in range(8):
            self.board[6][col] = Pawn('white', 6, col)
            self.board[1][col] = Pawn('black', 1, col)

        # Ладьи
        self.board[7][0] = Rook('white', 7, 0)
        self.board[7][7] = Rook('white', 7, 7)
        self.board[0][0] = Rook('black', 0, 0)
        self.board[0][7] = Rook('black', 0, 7)

        # Кони
        self.board[7][1] = Knight('white', 7, 1)
        self.board[7][6] = Knight('white', 7, 6)
        self.board[0][1] = Knight('black', 0, 1)
        self.board[0][6] = Knight('black', 0, 6)

        # Слоны
        self.board[7][2] = Bishop('white', 7, 2)
        self.board[7][5] = Bishop('white', 7, 5)
        self.board[0][2] = Bishop('black', 0, 2)
        self.board[0][5] = Bishop('black', 0, 5)

        # Ферзи
        self.board[7][3] = Queen('white', 7, 3)
        self.board[0][3] = Queen('black', 0, 3)

        # Короли
        self.board[7][4] = King('white', 7, 4)
        self.board[0][4] = King('black', 0, 4)

    def get_piece(self, row, col):
        return self.board[row][col]

    def select_piece(self, row, col):
        piece = self.board[row][col]
        if piece and piece.color == self.current_turn:
            self.selected_piece = piece
            self.valid_moves = self.get_valid_moves(piece)
            return True
        return False

    def get_valid_moves(self, piece):
        moves = []
        for row in range(8):
            for col in range(8):
                if piece.is_valid_move(self.board, row, col):
                    # Проверка, не окажется ли король под шахом
                    if self.is_safe_move(piece, row, col):
                        moves.append((row, col))
        return moves

    def is_safe_move(self, piece, new_row, new_col):
        # Временно делаем ход
        old_row, old_col = piece.row, piece.col
        target = self.board[new_row][new_col]

        self.board[new_row][new_col] = piece
        self.board[old_row][old_col] = None
        piece.row, piece.col = new_row, new_col

        # Проверяем, под шахом ли король
        king_pos = self.find_king(piece.color)
        in_check = self.is_square_attacked(king_pos[0], king_pos[1], piece.color)

        # Откатываем ход
        self.board[old_row][old_col] = piece
        self.board[new_row][new_col] = target
        piece.row, piece.col = old_row, old_col

        return not in_check

    def find_king(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and isinstance(piece, King) and piece.color == color:
                    return (row, col)
        return None

    def is_square_attacked(self, row, col, color):
        opponent_color = 'black' if color == 'white' else 'white'
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece.color == opponent_color:
                    if piece.is_valid_move(self.board, row, col):
                        return True
        return False

    def make_move(self, row, col):
        if (row, col) in self.valid_moves:
            # Выполняем ход
            captured = self.board[row][col]
            old_row, old_col = self.selected_piece.row, self.selected_piece.col

            self.board[row][col] = self.selected_piece
            self.board[old_row][old_col] = None
            self.selected_piece.row, self.selected_piece.col = row, col
            self.selected_piece.has_moved = True

            # Проверка на превращение пешки
            promotion_piece = None
            if isinstance(self.selected_piece, Pawn):
                # Белая пешка дошла до 0 ряда, чёрная до 7 ряда
                if (self.selected_piece.color == 'white' and row == 0) or \
                        (self.selected_piece.color == 'black' and row == 7):
                    # Возвращаем информацию, что нужно превращение
                    return True, captured is not None, self.selected_piece

            # Смена хода
            self.current_turn = 'black' if self.current_turn == 'white' else 'white'
            self.selected_piece = None
            self.valid_moves = []

            return True, captured is not None, None

        return False, False, None

    def promote_pawn(self, pawn, piece_type):
        """Превращает пешку в выбранную фигуру"""
        row, col = pawn.row, pawn.col
        color = pawn.color

        # Создаём новую фигуру
        if piece_type == 'queen':
            new_piece = Queen(color, row, col)
        elif piece_type == 'rook':
            new_piece = Rook(color, row, col)
        elif piece_type == 'bishop':
            new_piece = Bishop(color, row, col)
        elif piece_type == 'knight':
            new_piece = Knight(color, row, col)
        else:
            new_piece = Queen(color, row, col)  # По умолчанию ферзь

        # Заменяем пешку на новую фигуру
        self.board[row][col] = new_piece

        # Смена хода
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        self.selected_piece = None
        self.valid_moves = []

    def is_checkmate(self):
        # Проверяем, есть ли у текущего игрока возможные ходы
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == self.current_turn:
                    if self.get_valid_moves(piece):
                        return False
        return True

    def get_board_for_display(self, is_white_bottom):
        """Возвращает доску для отображения с учётом переворота"""
        if is_white_bottom:
            return self.board
        else:
            # Переворачиваем доску для чёрных
            rotated = [[None for _ in range(8)] for _ in range(8)]
            for i in range(8):
                for j in range(8):
                    rotated[7 - i][7 - j] = self.board[i][j]
            return rotated