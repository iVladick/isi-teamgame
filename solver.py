from enum import Enum
from game import Game
import time

class SolverMode(Enum):
    DFS = 0
    BACKTRACKING = 1
    FORWARD_CHECKING = 2

class Solver:
    def __init__(self, game: Game, stop_event, get_delay_callable, mode: SolverMode = SolverMode.BACKTRACKING):
        self.game = game
        self.mode = mode
        self.stop_event = stop_event
        self.get_delay = get_delay_callable  # Callable to get current delay

    def solve(self):
        match self.mode:
            case SolverMode.DFS:
                self._dfs()
            case SolverMode.BACKTRACKING:
                self._backtracking2()
            case SolverMode.FORWARD_CHECKING:
                self._forward_checking2()

    def _dfs(self):
        if self.stop_event.is_set():
            return True

        game = self.game
        pos = game.get_first_empty_cell()

        if pos is None:
            return game.is_field_valid()

        place_x, place_y = pos

        for number in range(1, game.size + 1):
            game.place_number(place_x, place_y, number)
            time.sleep(self.get_delay())

            if self._dfs():
                return True

            game.place_number(place_x, place_y, 0)
            time.sleep(self.get_delay())

        return False

    def _backtracking2(self):
        if self.stop_event.is_set():
            return True

        game = self.game

        if not game.is_field_valid():
            return False

        pos = game.get_first_empty_cell()

        if pos is None:
            return True

        place_x, place_y = pos

        for number in range(1, game.size + 1):
            game.place_number(place_x, place_y, number)
            time.sleep(self.get_delay())

            if self._backtracking2():
                return True

            game.place_number(place_x, place_y, 0)
            time.sleep(self.get_delay())

        return False

    def _backtracking(self):
        if self.stop_event.is_set():
            return False

        game = self.game
        pos = game.get_first_empty_cell()

        if pos is None:
            return True

        place_x, place_y = pos

        for number in range(1, game.size + 1):
            if self.stop_event.is_set():
                return False

            if game.is_place_valid(place_x, place_y, number):
                game.place_number(place_x, place_y, number)

                time.sleep(self.get_delay())

                if self._backtracking():
                    return True

                if self.stop_event.is_set():
                    return False

                game.place_number(place_x, place_y, 0)
                time.sleep(self.get_delay())

        return False

    def _forward_checking(self):
        if self.stop_event.is_set():
            return False

        game = self.game
        pos = game.get_first_empty_cell()

        if pos is None:
            return True

        place_x, place_y = pos

        for number in range(1, game.size + 1):
            if self.stop_event.is_set():
                return False

            if game.is_place_valid(place_x, place_y, number):
                game.place_number(place_x, place_y, number)
                time.sleep(self.get_delay())
                forward_pos = game.get_first_empty_cell()
                if forward_pos is None:
                    return True
                if self.stop_event.is_set():
                    return False
                forward_place_x, forward_place_y = forward_pos

                possible = False
                for forward_number in range(1, game.size + 1):
                    if game.is_place_valid(forward_place_x, forward_place_y, forward_number):
                        possible = True
                        break

                if possible and self._forward_checking():
                    return True
                if self.stop_event.is_set():
                    return False

                game.place_number(place_x, place_y, 0)
                time.sleep(self.get_delay())

        return False

    def _forward_checking2(self):
        if self.stop_event.is_set():
            return True

        game = self.game
        pos = game.get_first_empty_cell()

        if pos is None:
            return True

        place_x, place_y = pos

        for number in range(1, game.size + 1):
            if game.is_place_valid(place_x, place_y, number):
                game.place_number(place_x, place_y, number)
                time.sleep(self.get_delay())

                if self._forward_checking2():
                    return True

                game.place_number(place_x, place_y, 0)
                time.sleep(self.get_delay())

        return False
