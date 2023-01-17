from abc import *
from state import State
import sys

MAX_FLOAT = sys.float_info.max
MIN_FLOAT = -MAX_FLOAT


class AdversarialSearch(object):
    """
    Apstraktna klasa za suparnicku/protivnicku pretragu.
    """

    def __init__(self, board, max_depth):
        """
        :param board: tabla koja predstavlja pocetno stanje.
        :param max_depth: maksimalna dubina pretrage (koliko poteza unapred).
        :return:
        """
        self.initial_state = State(board, parent=None)
        self.max_depth = max_depth

    @abstractmethod
    def perform_adversarial_search(self):
        """
        Apstraktna metoda koja vrsi pretragu i vraca sledece stanje.
        """
        pass


class Minimax(AdversarialSearch):
    def perform_adversarial_search(self):
        # TODO 1: Implementirati minimax algoritam
        best_value, best_state = self.minimax(self.initial_state, 0, True)
        return best_state

    def minimax(self, state, depth, max_player):
        if depth == self.max_depth:
            return state.calculate_value(), state

        if max_player:
            best_value = MIN_FLOAT
            best_state = None
            new_states = state.generate_next_states(True)
            for new_state in new_states:
                value, b_state = self.minimax(new_state, depth + 1, False)
                if value > best_value:
                    best_value = value
                    best_state = new_state
            return best_value, best_state
        else:
            best_value = MAX_FLOAT
            best_state = None
            new_states = state.generate_next_states(False)
            for new_state in new_states:
                value, b_state = self.minimax(new_state, depth + 1, True)
                if value < best_value:
                    best_value = value
                    best_state = new_state
            return best_value, best_state


class AlphaBeta(AdversarialSearch):
    num = 0
    pruned = 0
    def perform_adversarial_search(self):
        # TODO 4: Implementirati alpha-beta algoritam

        best_value, best_state = self.alphabeta(self.initial_state, 0, MIN_FLOAT, MAX_FLOAT, True)
        return best_state

    def alphabeta(self, state, depth, alpha, beta, max_player):
        if depth == self.max_depth:
            return state.calculate_value(), state

        if max_player:
            best_value = MIN_FLOAT
            best_state = None
            new_states = state.generate_next_states(True)
            for new_state in new_states:
                value, b_state = self.alphabeta(new_state, depth + 1, alpha, beta, False)
                if value > best_value:
                    best_value = value
                    best_state = new_state
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value, best_state
        else:
            best_value = MAX_FLOAT
            best_state = None
            new_states = state.generate_next_states(False)
            for new_state in new_states:
                value, b_state = self.alphabeta(new_state, depth + 1, alpha, beta, True)
                if value < best_value:
                    best_value = value
                    best_state = new_state
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value, best_state
