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
                self._backtracking()
            case SolverMode.FORWARD_CHECKING:
                self._forward_checking()

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

    def _backtracking(self):
        if self.stop_event.is_set():
            return True

        game = self.game

        if not game.is_field_valid():
            return False

        pos = game.get_first_empty_cell()

        if pos is None:
            return game.is_field_valid()

        place_x, place_y = pos

        for number in range(1, game.size + 1):
            game.place_number(place_x, place_y, number)
            time.sleep(self.get_delay())

            if self._backtracking():
                return True

            game.place_number(place_x, place_y, 0)
            time.sleep(self.get_delay())

        return False

    def _forward_checking(self):
        # Initialize domains (possible values) for all empty cells
        domains = self._init_domains()

        return self._fc2_backtrack(domains)

    def _fc2_backtrack(self, domains):
        if self.stop_event.is_set():
            return True

        # If there are no empty cells, we've solved the puzzle
        pos = self._select_unassigned_variable(domains)
        if pos is None:
            return True

        place_x, place_y = pos
        game = self.game

        # Try each possible value in the domain of the selected cell
        for number in sorted(domains[pos]):
            if game.is_place_valid(place_x, place_y, number):
                # Place the number
                old_value = game.field[place_y][place_x]
                game.place_number(place_x, place_y, number)
                time.sleep(self.get_delay())

                # Update domains based on this assignment
                new_domains = self._update_domains(domains, pos, number)
                if new_domains is not None:
                    # If no domain is empty after assignment, continue search
                    if self._fc2_backtrack(new_domains):
                        return True

                # Backtrack: revert the assignment
                game.place_number(place_x, place_y, old_value)
                time.sleep(self.get_delay())

        return False

        # Helper method to initialize domains for each empty cell

    def _init_domains(self):
        game = self.game
        domains = {}

        for y in range(game.size):
            for x in range(game.size):
                if game.field[y][x] == 0:
                    # Cell is empty, compute possible values
                    possible_values = set(range(1, game.size + 1))
                    # Remove values that are not valid due to row, col, or box conflicts
                    for num in range(1, game.size + 1):
                        if not game.is_place_valid(x, y, num):
                            if num in possible_values:
                                possible_values.remove(num)
                    domains[(x, y)] = possible_values

        return domains

        # Select unassigned variable (cell) with the smallest domain (MRV heuristic)

    def _select_unassigned_variable(self, domains):
        # Filter only empty cells (keys in domains)
        if not domains:
            return None
        # Pick the cell with the smallest number of possible values
        pos, _ = min(domains.items(), key=lambda item: len(item[1]))
        return pos

        # Update domains after placing a particular number in a cell

    def _update_domains(self, domains, assigned_pos, assigned_number):
        game = self.game
        x, y = assigned_pos
        new_domains = {}

        # The assigned cell is no longer empty, so we skip it
        # and only copy domains for other cells
        for pos, dom in domains.items():
            if pos == assigned_pos:
                # This cell is now filled
                continue
            # Create a copy of the domain for future modification
            new_dom = set(dom)

            # If in the same row, column, or box, remove the assigned number
            if pos[1] == y or pos[0] == x or self._in_same_section(pos, assigned_pos):
                if assigned_number in new_dom:
                    new_dom.remove(assigned_number)

            # If any domain becomes empty, return None to indicate failure
            if len(new_dom) == 0:
                return None

            new_domains[pos] = new_dom

        return new_domains

    def _in_same_section(self, pos_a, pos_b):
        game = self.game
        sec_size = game.section_size
        ax, ay = pos_a
        bx, by = pos_b
        return (ax // sec_size == bx // sec_size) and (ay // sec_size == by // sec_size)