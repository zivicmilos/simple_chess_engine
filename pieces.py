from abc import *


class Piece(object):
    """
    Apstraktna klasa za sahovske figure.
    """

    def __init__(self, board, row, col, side):
        self.board = board
        self.row = row
        self.col = col
        self.side = side

    @abstractmethod
    def get_legal_moves(self):
        """
        Apstraktna metoda koja treba da za konkretnu figuru vrati moguce sledece poteze (pozicije).
        """
        pass

    def get_value(self):
        """
        Vrednost figure modifikovana u odnosu na igraca.
        Figure crnog (MAX igrac) imaju pozivitnu vrednost, a belog (MIN igrac) negativnu.
        :return: float
        """
        return self.get_value_() if self.side == 'b' else self.get_value_() * -1.

    @abstractmethod
    def get_value_(self):
        """
        Apstraktna metoda koja treba da vrati vrednost za konkretnu figuru.
        """
        pass


class Pawn(Piece):
    """
    Pijun
    """

    def get_legal_moves(self):
        row = self.row
        col = self.col
        side = self.side
        legal_moves = []
        d_rows = []
        d_cols = []

        if side == 'w':  # beli pijun
            # jedan unapred, ako je polje prazno
            if row > 0 and self.board.data[row - 1][col] == '.':
                d_rows.append(-1)
                d_cols.append(0)
            # dva unapred, ako je pocetna pozicija i ako je polje prazno
            if row == self.board.rows - 2 and self.board.data[row - 1][col] == '.' and self.board.data[row - 2][
                col] == '.':
                d_rows.append(-2)
                d_cols.append(0)
            # ukoso levo, jede crnog
            if col > 0 and row > 0 and self.board.data[row - 1][col - 1].startswith('b'):
                d_rows.append(-1)
                d_cols.append(-1)
            # ukoso desno, jede crnog
            if col < self.board.cols - 1 and row > 0 and self.board.data[row - 1][col + 1].startswith('b'):
                d_rows.append(-1)
                d_cols.append(1)
            if col > 0 and row == 3 and self.board.data[row][col - 1] == 'bp' and self.board.prev_board.data \
                    [row - 2][col - 1] == 'bp' and self.board.data[row - 2][col - 1] == '.':
                d_rows.append(-1)
                d_cols.append(-1)
            if col < self.board.cols - 1 and row == 3 and self.board.data[row][col + 1] == 'bp' and self.board.prev_board \
                    .data[row - 2][col + 1] == 'bp' and self.board.data[row - 2][col + 1] == '.':
                d_rows.append(-1)
                d_cols.append(1)
        else:  # crni pijun
            # TODO 2: Implementirati moguce sledece poteze za crnog pijuna
            # jedan unapred, ako je polje prazno
            if row < self.board.rows - 1 and self.board.data[row + 1][col] == '.':
                d_rows.append(1)
                d_cols.append(0)
            # dva unapred, ako je pocetna pozicija i ako je polje prazno
            if row == self.board.rows - 7 and self.board.data[row + 1][col] == '.' and self.board.data[row + 2][
                col] == '.':
                d_rows.append(2)
                d_cols.append(0)
            # ukoso levo, jede belog
            if col < self.board.cols - 1 and row < self.board.rows - 1 and self.board.data[row + 1][col + 1].startswith(
                    'w'):
                d_rows.append(1)
                d_cols.append(1)
            # ukoso desno, jede belog
            if col > 0 and row < self.board.rows - 1 and self.board.data[row + 1][col - 1].startswith('w'):
                d_rows.append(1)
                d_cols.append(-1)
            if col > 0 and row == 4 and self.board.data[row][col - 1] == 'wp' and self.board.prev_board.data \
                    [row + 2][col - 1] == 'wp' and self.board.data[row + 2][col - 1] == '.':
                d_rows.append(1)
                d_cols.append(-1)
            if col < self.board.cols - 1 and row == 4 and self.board.data[row][col + 1] == 'wp' and self.board.prev_board \
                    .data[row + 2][col + 1] == 'wp' and self.board.data[row + 2][col + 1] == '.':
                d_rows.append(1)
                d_cols.append(1)

        for d_row, d_col in zip(d_rows, d_cols):
            new_row = row + d_row
            new_col = col + d_col
            if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols:
                if new_row == 0 or new_row == 7:
                    legal_moves.append((new_row, new_col, 'promotion'))
                elif abs(d_row) == 1 and abs(d_col) == 1 and self.board.data[new_row][new_col] == '.':
                    legal_moves.append((new_row, new_col, 'en passant'))
                else:
                    legal_moves.append((new_row, new_col))

        return legal_moves

    @staticmethod
    def get_value_():
        return 1.  # pijun ima vrednost 1


class Knight(Piece):
    """
    Konj
    """

    def get_legal_moves(self):
        row = self.row
        col = self.col
        side = self.side
        legal_moves = []
        d_rows = []
        d_cols = []

        if row + 2 < self.board.rows and col + 1 < self.board.cols and not self.board.data[row + 2][col + 1].startswith(
                side):
            d_rows.append(2)
            d_cols.append(1)
        if row + 2 < self.board.rows and col > 0 and not self.board.data[row + 2][col - 1].startswith(side):
            d_rows.append(2)
            d_cols.append(-1)
        if row - 2 >= 0 and col + 1 < self.board.cols and not self.board.data[row - 2][col + 1].startswith(side):
            d_rows.append(-2)
            d_cols.append(1)
        if row - 2 >= 0 and col > 0 and not self.board.data[row - 2][col - 1].startswith(side):
            d_rows.append(-2)
            d_cols.append(-1)
        if row + 1 < self.board.rows and col + 2 < self.board.cols and not self.board.data[row + 1][col + 2].startswith(
                side):
            d_rows.append(1)
            d_cols.append(2)
        if row + 1 < self.board.rows and col > 1 and not self.board.data[row + 1][col - 2].startswith(side):
            d_rows.append(1)
            d_cols.append(-2)
        if row - 1 >= 0 and col + 2 < self.board.cols and not self.board.data[row - 1][col + 2].startswith(side):
            d_rows.append(-1)
            d_cols.append(2)
        if row - 1 >= 0 and col > 1 and not self.board.data[row - 1][col - 2].startswith(side):
            d_rows.append(-1)
            d_cols.append(-2)

        for d_row, d_col in zip(d_rows, d_cols):
            new_row = row + d_row
            new_col = col + d_col
            if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols:
                legal_moves.append((new_row, new_col))

        return legal_moves

    @staticmethod
    def get_value_():
        return 3.2


class Bishop(Piece):
    """
    Lovac
    """

    def get_legal_moves(self):
        row = self.row
        col = self.col
        side = self.side
        legal_moves = []
        d_rows = []
        d_cols = []

        for i in range(1, self.board.rows):
            if row + i > self.board.rows - 1 or col + i > self.board.cols - 1 or self.board.data[row + i][
                    col + i].startswith(side):
                break
            d_rows.append(i)
            d_cols.append(i)
            if not self.board.data[row + i][col + i] == '.':
                break

        for i in range(1, self.board.rows):
            if row + i > self.board.rows - 1 or col - i < 0 or self.board.data[row + i][col - i].startswith(side):
                break
            d_rows.append(i)
            d_cols.append(-i)
            if not self.board.data[row + i][col - i] == '.':
                break

        for i in range(1, self.board.rows):
            if row - i < 0 or col + i > self.board.cols - 1 or self.board.data[row - i][col + i].startswith(side):
                break
            d_rows.append(-i)
            d_cols.append(i)
            if not self.board.data[row - i][col + i] == '.':
                break

        for i in range(1, self.board.rows):
            if row - i < 0 or col - i < 0 or self.board.data[row - i][col - i].startswith(side):
                break
            d_rows.append(-i)
            d_cols.append(-i)
            if not self.board.data[row - i][col - i] == '.':
                break

        for d_row, d_col in zip(d_rows, d_cols):
            new_row = row + d_row
            new_col = col + d_col
            if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols:
                legal_moves.append((new_row, new_col))

        return legal_moves

    @staticmethod
    def get_value_():
        return 3.33


class Rook(Piece):
    """
    Top
    """

    def get_legal_moves(self):
        row = self.row
        col = self.col
        side = self.side
        legal_moves = []
        d_rows = []
        d_cols = []

        for i in range(1, self.board.rows):
            if row + i > self.board.rows - 1 or self.board.data[row + i][col].startswith(side):
                break
            d_rows.append(i)
            d_cols.append(0)
            if not self.board.data[row + i][col] == '.':
                break

        for i in range(1, self.board.rows):
            if col + i > self.board.cols - 1 or self.board.data[row][col + i].startswith(side):
                break
            d_rows.append(0)
            d_cols.append(i)
            if not self.board.data[row][col + i] == '.':
                break

        for i in range(1, self.board.rows):
            if row - i < 0 or self.board.data[row - i][col].startswith(side):
                break
            d_rows.append(-i)
            d_cols.append(0)
            if not self.board.data[row - i][col] == '.':
                break

        for i in range(1, self.board.rows):
            if col - i < 0 or self.board.data[row][col - i].startswith(side):
                break
            d_rows.append(0)
            d_cols.append(-i)
            if not self.board.data[row][col - i] == '.':
                break

        for d_row, d_col in zip(d_rows, d_cols):
            new_row = row + d_row
            new_col = col + d_col
            if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols:
                legal_moves.append((new_row, new_col))
                """if col == 0 and side == 'w':
                    self.board.wr1_moved = True
                elif col == 0 and side == 'b':
                    self.board.br1_moved = True
                elif col == self.board.cols - 1 and side == 'w':
                    self.board.wr2_moved = True
                elif col == self.board.cols - 1 and side == 'b':
                    self.board.br2_moved = True"""

        return legal_moves

    @staticmethod
    def get_value_():
        return 5.1


class Queen(Piece):
    """
    Kraljica
    """

    def get_legal_moves(self):
        row = self.row
        col = self.col
        side = self.side
        legal_moves = []
        d_rows = []
        d_cols = []

        for i in range(1, self.board.rows):
            if row + i > self.board.rows - 1 or col + i > self.board.cols - 1 or self.board.data[row + i][
                    col + i].startswith(side):
                break
            d_rows.append(i)
            d_cols.append(i)
            if not self.board.data[row + i][col + i] == '.':
                break

        for i in range(1, self.board.rows):
            if row + i > self.board.rows - 1 or col - i < 0 or self.board.data[row + i][col - i].startswith(side):
                break
            d_rows.append(i)
            d_cols.append(-i)
            if not self.board.data[row + i][col - i] == '.':
                break

        for i in range(1, self.board.rows):
            if row - i < 0 or col + i > self.board.cols - 1 or self.board.data[row - i][col + i].startswith(side):
                break
            d_rows.append(-i)
            d_cols.append(i)
            if not self.board.data[row - i][col + i] == '.':
                break

        for i in range(1, self.board.rows):
            if row - i < 0 or col - i < 0 or self.board.data[row - i][col - i].startswith(side):
                break
            d_rows.append(-i)
            d_cols.append(-i)
            if not self.board.data[row - i][col - i] == '.':
                break

        for i in range(1, self.board.rows):
            if row + i > self.board.rows - 1 or self.board.data[row + i][col].startswith(side):
                break
            d_rows.append(i)
            d_cols.append(0)
            if not self.board.data[row + i][col] == '.':
                break

        for i in range(1, self.board.rows):
            if col + i > self.board.cols - 1 or self.board.data[row][col + i].startswith(side):
                break
            d_rows.append(0)
            d_cols.append(i)
            if not self.board.data[row][col + i] == '.':
                break

        for i in range(1, self.board.rows):
            if row - i < 0 or self.board.data[row - i][col].startswith(side):
                break
            d_rows.append(-i)
            d_cols.append(0)
            if not self.board.data[row - i][col] == '.':
                break

        for i in range(1, self.board.rows):
            if col - i < 0 or self.board.data[row][col - i].startswith(side):
                break
            d_rows.append(0)
            d_cols.append(-i)
            if not self.board.data[row][col - i] == '.':
                break

        for d_row, d_col in zip(d_rows, d_cols):
            new_row = row + d_row
            new_col = col + d_col
            if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols:
                legal_moves.append((new_row, new_col))

        return legal_moves

    @staticmethod
    def get_value_():
        return 8.8


class King(Piece):
    """
    Kralj
    """

    def get_legal_moves(self):
        row = self.row
        col = self.col
        side = self.side
        legal_moves = []
        d_rows = []
        d_cols = []

        if row + 1 < self.board.rows and not self.board.data[row + 1][col].startswith(side):
            d_rows.append(1)
            d_cols.append(0)
        if row + 1 < self.board.rows and col + 1 < self.board.cols and not self.board.data[row + 1][col + 1].startswith(
                side):
            d_rows.append(1)
            d_cols.append(1)
        if col + 1 < self.board.cols and not self.board.data[row][col + 1].startswith(side):
            d_rows.append(0)
            d_cols.append(1)
        if row - 1 >= 0 and col + 1 < self.board.cols and not self.board.data[row - 1][col + 1].startswith(side):
            d_rows.append(-1)
            d_cols.append(1)
        if row - 1 >= 0 and not self.board.data[row - 1][col].startswith(side):
            d_rows.append(-1)
            d_cols.append(0)
        if row - 1 >= 0 and col - 1 >= 0 and col + 1 < self.board.cols and not self.board.data[row - 1][
                col - 1].startswith(side):
            d_rows.append(-1)
            d_cols.append(-1)
        if col - 1 >= 0 and not self.board.data[row][col - 1].startswith(side):
            d_rows.append(0)
            d_cols.append(-1)
        if row + 1 < self.board.rows and col - 1 >= 0 and not self.board.data[row + 1][col - 1].startswith(side):
            d_rows.append(1)
            d_cols.append(-1)

        if side == 'w' and row == self.board.rows - 1 and self.board.data[row][self.board.cols - 1] == 'wr' and \
                self.board.data[row][self.board.cols - 2] == '.' and self.board.data[row][self.board.cols - 3] == '.' \
                and not self.board.wk_moved and not self.board.wr2_moved:
            d_rows.append(0)
            d_cols.append(2)
        if side == 'w' and row == self.board.rows - 1 and self.board.data[row][0] == 'wr' and \
                self.board.data[row][1] == '.' and self.board.data[row][2] == '.' and self.board.data[row][3] == '.'\
                and not self.board.wk_moved and not self.board.wr1_moved:
            d_rows.append(0)
            d_cols.append(-2)
        if side == 'b' and row == 0 and self.board.data[row][self.board.cols - 1] == 'br' and \
                self.board.data[row][self.board.cols - 2] == '.' and self.board.data[row][self.board.cols - 3] == '.' \
                and not self.board.bk_moved and not self.board.br2_moved:
            d_rows.append(0)
            d_cols.append(2)
        if side == 'b' and row == 0 and self.board.data[row][0] == 'br' and \
                self.board.data[row][1] == '.' and self.board.data[row][2] == '.' and self.board.data[row][3] == '.'\
                and not self.board.bk_moved and not self.board.br1_moved:
            d_rows.append(0)
            d_cols.append(-2)

        for d_row, d_col in zip(d_rows, d_cols):
            new_row = row + d_row
            new_col = col + d_col
            if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols:
                if abs(d_col) == 2:
                    legal_moves.append((new_row, new_col, 'castling'))
                else:
                    legal_moves.append((new_row, new_col))
                """if side == 'w':
                    self.board.wk_moved = True
                else:
                    self.board.bk_moved = True"""

        return legal_moves

    @staticmethod
    def get_value_():
        return 1000.
