import pygame


class Piece:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.has_moved = False
        self.image = None
        self.image_name = ""

    def load_image(self):
        if self.image is None:
            try:
                self.image = pygame.image.load(f"assets/pieces/{self.image_name}.png")
                self.image = pygame.transform.scale(self.image, (80, 80))
            except:
                print(f"Не удалось загрузить {self.image_name}")

    def get_pos(self):
        return (self.row, self.col)


class Pawn(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.image_name = f"{color}_pawn"
        self.load_image()

    def is_valid_move(self, board, new_row, new_col):
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1

        if new_col == self.col and new_row == self.row + direction and board[new_row][new_col] is None:
            return True

        if (new_col == self.col and new_row == self.row + 2 * direction and
                self.row == start_row and board[new_row][new_col] is None and
                board[self.row + direction][self.col] is None):
            return True

        if abs(new_col - self.col) == 1 and new_row == self.row + direction:
            target = board[new_row][new_col]
            if target and target.color != self.color:
                return True

        return False


class Rook(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.image_name = f"{color}_rook"
        self.load_image()

    def is_valid_move(self, board, new_row, new_col):
        if self.row != new_row and self.col != new_col:
            return False

        if self.row == new_row:
            step = 1 if new_col > self.col else -1
            for c in range(self.col + step, new_col, step):
                if board[new_row][c] is not None:
                    return False
        else:
            step = 1 if new_row > self.row else -1
            for r in range(self.row + step, new_row, step):
                if board[r][self.col] is not None:
                    return False

        target = board[new_row][new_col]
        return target is None or target.color != self.color


class Knight(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.image_name = f"{color}_knight"
        self.load_image()

    def is_valid_move(self, board, new_row, new_col):
        dr = abs(new_row - self.row)
        dc = abs(new_col - self.col)
        valid = (dr == 2 and dc == 1) or (dr == 1 and dc == 2)

        if valid:
            target = board[new_row][new_col]
            return target is None or target.color != self.color
        return False


class Bishop(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.image_name = f"{color}_bishop"
        self.load_image()

    def is_valid_move(self, board, new_row, new_col):
        if abs(new_row - self.row) != abs(new_col - self.col):
            return False

        step_r = 1 if new_row > self.row else -1
        step_c = 1 if new_col > self.col else -1

        r, c = self.row + step_r, self.col + step_c
        while (r, c) != (new_row, new_col):
            if board[r][c] is not None:
                return False
            r += step_r
            c += step_c

        target = board[new_row][new_col]
        return target is None or target.color != self.color


class Queen(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.image_name = f"{color}_queen"
        self.load_image()

    def is_valid_move(self, board, new_row, new_col):
        if self.row == new_row or self.col == new_col:
            if self.row == new_row:
                step = 1 if new_col > self.col else -1
                for c in range(self.col + step, new_col, step):
                    if board[new_row][c] is not None:
                        return False
            else:
                step = 1 if new_row > self.row else -1
                for r in range(self.row + step, new_row, step):
                    if board[r][self.col] is not None:
                        return False
        elif abs(new_row - self.row) == abs(new_col - self.col):
            step_r = 1 if new_row > self.row else -1
            step_c = 1 if new_col > self.col else -1
            r, c = self.row + step_r, self.col + step_c
            while (r, c) != (new_row, new_col):
                if board[r][c] is not None:
                    return False
                r += step_r
                c += step_c
        else:
            return False

        target = board[new_row][new_col]
        return target is None or target.color != self.color


class King(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.image_name = f"{color}_king"
        self.load_image()

    def is_valid_move(self, board, new_row, new_col):
        dr = abs(new_row - self.row)
        dc = abs(new_col - self.col)

        if max(dr, dc) == 1:
            target = board[new_row][new_col]
            return target is None or target.color != self.color

        if dr == 0 and dc == 2 and not self.has_moved:
            rook_col = 0 if new_col == 2 else 7
            rook = board[self.row][rook_col]
            if rook and isinstance(rook, Rook) and not rook.has_moved:
                step = 1 if new_col > self.col else -1
                for c in range(self.col + step, new_col, step):
                    if board[self.row][c] is not None:
                        return False
                return True

        return False