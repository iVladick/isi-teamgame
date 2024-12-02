from enum import Enum
from tkinter.ttk import Treeview

from game import Game


class SolverMode(Enum):
    DFS = 0,
    BACKTRACKING = 1,
    FORWARD_CHECKING = 2


class Solver:
    def __init__(self, game: Game, mode: SolverMode = SolverMode.BACKTRACKING):
        self.game = game
        self.mode = mode

    def solve(self):
        match self.mode:
            case SolverMode.DFS:
                self._dfs()
            case SolverMode.BACKTRACKING:
                self._backtracking()
            case SolverMode.FORWARD_CHECKING:
                self._forward_checking()

    def _dfs(self):
        game = self.game

        pos = game.get_first_empty_cell()

        if pos is None:
            return game.is_field_valid()

        place_x, place_y = pos

        for number in range(1, game.size + 1):
            if game.is_place_valid(place_x, place_y, number):
                game.place_number(place_x, place_y, number)

                if self._dfs():
                    return True

                game.place_number(place_x, place_y, 0)

        game.place_number(place_x, place_y, 1)

        if self._dfs():
            return True

        game.place_number(place_x, place_y, 0)

        return False

    def _backtracking(self):
        game = self.game

        pos = game.get_first_empty_cell()

        if pos is None:
            return True

        place_x, place_y = pos

        for number in range(1, game.size + 1):
            if game.is_place_valid(place_x, place_y, number):
                game.place_number(place_x, place_y, number)

                if self._backtracking():
                    return True

                game.place_number(place_x, place_y, 0)

        return False

    def _forward_checking(self):
        game = self.game

        pos = game.get_first_empty_cell()

        if pos is None:
            return True

        place_x, place_y = pos

        for number in range(1, game.size + 1):
            if game.is_place_valid(place_x, place_y, number):
                game.place_number(place_x, place_y, number)

                forward_pos = game.get_first_empty_cell()

                if forward_pos is None:
                    return True

                forward_place_x, forward_place_y = forward_pos

                possible = False
                for forward_number in range(1, game.size + 1):
                    if game.is_place_valid(forward_place_x, forward_place_y, forward_number):
                        possible = True
                        break

                if possible and self._forward_checking():
                    return True

                game.place_number(place_x, place_y, 0)

        return False
