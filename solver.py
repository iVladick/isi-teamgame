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
        self.get_delay = get_delay_callable

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
        domains = self._init_domains()

        return self._fc2_backtrack(domains)

    def _fc2_backtrack(self, domains):
        if self.stop_event.is_set():
            return True

        pos = self._select_unassigned_variable(domains)
        if pos is None:
            return True

        place_x, place_y = pos
        game = self.game

        for number in sorted(domains[pos]):
            if game.is_place_valid(place_x, place_y, number):
                old_value = game.field[place_y][place_x]
                game.place_number(place_x, place_y, number)
                time.sleep(self.get_delay())

                new_domains = self._update_domains(domains, pos, number)
                if new_domains is not None:
                    if self._fc2_backtrack(new_domains):
                        return True

                game.place_number(place_x, place_y, old_value)
                time.sleep(self.get_delay())

        return False


    def _init_domains(self):
        game = self.game
        domains = {}

        for y in range(game.size):
            for x in range(game.size):
                if game.field[y][x] == 0:
                    possible_values = set(range(1, game.size + 1))
                    for num in range(1, game.size + 1):
                        if not game.is_place_valid(x, y, num):
                            if num in possible_values:
                                possible_values.remove(num)
                    domains[(x, y)] = possible_values

        return domains


    def _select_unassigned_variable(self, domains):
        if not domains:
            return None
        pos, _ = min(domains.items(), key=lambda item: len(item[1]))
        return pos


    def _update_domains(self, domains, assigned_pos, assigned_number):
        x, y = assigned_pos
        new_domains = {}

        for pos, dom in domains.items():
            if pos == assigned_pos:
                continue
            new_dom = set(dom)

            if pos[1] == y or pos[0] == x or self._in_same_section(pos, assigned_pos):
                if assigned_number in new_dom:
                    new_dom.remove(assigned_number)

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