from enum import Enum

from game import Game


class SolverMode(Enum):
    DFS = 0,
    BACKTRACKING = 1,
    FORWARD_CHECKING = 2


class Solver:
    def __init__(self, game: Game, mode: SolverMode = SolverMode.DFS):
        self.game = game
        self.mode = mode

    def solve(self):
        match self.mode:
            case SolverMode.DFS:
                self._dfs()
            case SolverMode.BACKTRACKING:
                self._backtraking()
            case SolverMode.FORWARD_CHECKING:
                self._forward_cheking()

    def _sub_dfs(self, number):
        game = self.game

        pos = game.get_first_empty_cell()

        if pos is None:
            return True

        place_x, place_y = pos

        if game.is_place_valid(place_x, place_y, number):
            game.place_number(place_x, place_y, number)
            return True

        return False

    def _dfs(self):
        game = self.game

        pos = game.get_first_empty_cell()

        if pos is None:
            return True

        place_x, place_y = pos

        for number in range(1, game.size + 1):
            pass

        return False

    def _backtraking(self):
        game = self.game

        pos = game.get_first_empty_cell()

        if pos is None:
            return True

        place_x, place_y = pos

        for number in range(1, game.size + 1):
            if game.is_place_valid(place_x, place_y, number):
                game.place_number(place_x, place_y, number)

                if self._backtraking():
                    return True

                game.place_number(place_x, place_y, 0)

        return False

    def _forward_cheking(self):
        pass
