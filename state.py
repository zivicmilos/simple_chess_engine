import copy
import random
import ujson
import pickle

from pieces import *


class State(object):
    """
    Klasa koja opisuje stanje table.
    """

    def __init__(self, board, parent=None):
        """
        :param board: Board (tabla)
        :param parent: roditeljsko stanje
        :return:
        """
        self.board = board  # sahovska tabla koja opisuje trenutno stanje
        self.parent = parent  # roditeljsko stanje
        self.value = 0.  # "vrednost" stanja - racuna ga evaluaciona funkcija calculate_value()

    def generate_next_states(self, max_player):
        """
        Generise moguca sledeca stanja (table) na osnovu svih mogucih poteza (u zavisnosti koji je igrac na potezu).
        :param max_player: bool. Da li je MAX igrac (crni)?
        :return: list. Lista mogucih sledecih stanja.
        """
        next_states = []
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                piece = self.board.determine_piece(row, col)  # odredi koja je figura
                if piece is None:
                    continue
                # generisi za crne ako je max igrac na potezu, generisi za bele ako je min igrac na potezu
                if (max_player and piece.side == 'b') or (not max_player and piece.side == 'w'):
                    if piece.board.data[7][4] != 'wk':
                        piece.board.wk_moved = True
                    if piece.board.data[0][4] != 'bk':
                        piece.board.bk_moved = True
                    if piece.board.data[7][0] != 'wr':
                        piece.board.wr1_moved = True
                    if piece.board.data[7][7] != 'wr':
                        piece.board.wr2_moved = True
                    if piece.board.data[0][0] != 'br':
                        piece.board.br1_moved = True
                    if piece.board.data[0][7] != 'br':
                        piece.board.br2_moved = True
                    legal_moves = piece.get_legal_moves()  # svi moguci potezi za figuru
                    for legal_move in legal_moves:
                        #new_board = copy.deepcopy(self.board)
                        #new_board = ujson.loads(ujson.dumps(self.board))
                        new_board = pickle.loads(pickle.dumps(self.board, -1))

                        new_board.move_piece(row, col, legal_move[0], legal_move[1])

                        if len(legal_move) == 3:
                            if legal_move[2] == 'promotion':
                                new_board.data[legal_move[0]][legal_move[1]] = piece.side + 'q'
                            elif legal_move[2] == 'en passant':
                                if piece.side == 'b':
                                    new_board.data[legal_move[0] - 1][legal_move[1]] = '.'
                                else:
                                    new_board.data[legal_move[0] + 1][legal_move[1]] = '.'
                            elif legal_move[2] == 'castling':
                                if legal_move[1] == self.board.cols - 2:
                                    new_board.move_piece(legal_move[0], self.board.cols - 1, legal_move[0],
                                                         self.board.cols - 3)
                                elif legal_move[1] == 2:
                                    new_board.move_piece(legal_move[0], 0, legal_move[0], 3)

                        next_state = State(new_board, self)
                        next_states.append(next_state)

        # TODO 5: Izmesati listu moguca sledeca stanja (da ne budu uvek u istom redosledu)
        random.shuffle(next_states)
        #next_states.sort(reverse=True, key=lambda state: state.calculate_value())

        return next_states

    def calculate_value(self):
        """
        Evaluaciona funkcija za stanje.
        :return:
        """
        # TODO 3: Implementirati jednostavnu evaluacionu funkciju (suma vrednosti svih figura na tabli)
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                if self.board.data[row][col].startswith('b'):
                    if self.board.data[row][col].endswith('p'):
                        self.value += Pawn.get_value_()
                    elif self.board.data[row][col].endswith('n'):
                        self.value += Knight.get_value_()
                    elif self.board.data[row][col].endswith('b'):
                        self.value += Bishop.get_value_()
                    elif self.board.data[row][col].endswith('q'):
                        self.value += Queen.get_value_()
                    elif self.board.data[row][col].endswith('k'):
                        self.value += King.get_value_()
                elif self.board.data[row][col].startswith('w'):
                    if self.board.data[row][col].endswith('p'):
                        self.value -= Pawn.get_value_()
                    elif self.board.data[row][col].endswith('n'):
                        self.value -= Knight.get_value_()
                    elif self.board.data[row][col].endswith('b'):
                        self.value -= Bishop.get_value_()
                    elif self.board.data[row][col].endswith('q'):
                        self.value -= Queen.get_value_()
                    elif self.board.data[row][col].endswith('k'):
                        self.value -= King.get_value_()

        # zauzet centar
        if self.board.data[4][3] == 'wp':
            self.value -= 0.3
        if self.board.data[4][4] == 'wp':
            self.value -= 0.3
        if self.board.data[3][3] == 'bp':
            self.value += 0.3
        if self.board.data[3][4] == 'bp':
            self.value += 0.3

        # bishop pair
        w_bishop_pair = 0
        b_bishop_pair = 0
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                if self.board.data[row][col] == 'wb':
                    w_bishop_pair += 1
                elif self.board.data[row][col] == 'bb':
                    b_bishop_pair += 1

        if w_bishop_pair == 2:
            self.value -= 0.5
        if b_bishop_pair == 2:
            self.value += 0.5

        # bezbedan kralj
        if self.board.data[7][2] == 'wk' or self.board.data[7][6] == 'wk':
            self.value -= 0.3
        if self.board.data[0][2] == 'bk' or self.board.data[0][6] == 'bk':
            self.value += 0.3

        # konj u blizini centra table
        for row in range(2, 6):
            for col in range(2, 6):
                if self.board.data[row][col] == 'wn':
                    self.value -= 0.1
                elif self.board.data[row][col] == 'bn':
                    self.value += 0.1

        return self.value
