from enum import Enum
import random
import copy

class FieldType(Enum):
    f9x9 = {
        'size': 9,
        'section_size': 3,
        'filled_range': range(25, 31)
    }
    f4x4 = {
        'size': 4,
        'section_size': 2,
        'filled_range': range(4, 7)
    }

class Game:
    def __init__(self, callback_on_place, field_type=FieldType.f9x9):
        self.field_type = field_type.value
        self.size = self.field_type['size']
        self.section_size = self.field_type['section_size']
        self.filled_range = self.field_type['filled_range']
        self.field = self._create_empty_field()
        self.fill_grid_backtracking()
        self.remove_numbers_from_grid()

        self.field_start = copy.deepcopy(self.field)
        self.callback_on_place = callback_on_place
        self.place_counter = 0

    def _create_empty_field(self):
        return [[0] * self.size for _ in range(self.size)]

    def is_section_contains(self, x: int, y: int, num: int) -> bool:
        sec_x, sec_y = x // self.section_size, y // self.section_size
        for i in range(sec_y * self.section_size, (sec_y + 1) * self.section_size):
            for j in range(sec_x * self.section_size, (sec_x + 1) * self.section_size):
                if self.field[i][j] == num:
                    return True
        return False

    def is_col_row_contains(self, x: int, y: int, num: int) -> bool:
        for i in range(self.size):
            if self.field[y][i] == num or self.field[i][x] == num:
                return True
        return False

    def is_place_valid(self, x: int, y: int, num: int) -> bool:
        if not (0 <= x < self.size and 0 <= y < self.size and 1 <= num <= self.size):
            return False
        return not (self.is_section_contains(x, y, num) or self.is_col_row_contains(x, y, num))

    def place_number(self, x: int, y: int, num: int):
        self.field[y][x] = num
        self.place_counter += 1
        self.callback_on_place()

    def fill_grid_backtracking(self) -> bool:
        empty = self.get_first_empty_cell()
        if empty is None:
            return True
        x, y = empty

        numbers = list(range(1, self.size + 1))
        random.shuffle(numbers)

        for num in numbers:
            if self.is_place_valid(x, y, num):
                self.field[y][x] = num
                if self.fill_grid_backtracking():
                    return True
                self.field[y][x] = 0

        return False

    def remove_numbers_from_grid(self):
        num_removed = 0
        num_to_remove = self.get_num_to_remove()

        attempts = num_to_remove * 2

        while num_removed < num_to_remove and attempts > 0:
            y = random.randint(0, self.size - 1)
            x = random.randint(0, self.size - 1)

            if self.field[y][x] != 0:
                backup = self.field[y][x]
                self.field[y][x] = 0

                grid_copy = copy.deepcopy(self.field)
                solutions = []
                self.count_solutions(grid_copy, solutions)

                if len(solutions) != 1:
                    self.field[y][x] = backup
                else:
                    num_removed += 1
            attempts -= 1

        if num_removed < num_to_remove:
            print(f"Removed {num_removed} numbers out of requested {num_to_remove}")

    def get_num_to_remove(self):
        num_filled = random.choice(self.filled_range)
        return self.size ** 2 - num_filled

    def count_solutions(self, grid, solutions, limit=2):
        empty = self.find_empty_location_grid(grid)
        if not empty:
            solutions.append(copy.deepcopy(grid))
            return
        y, x = empty

        for num in range(1, self.size + 1):
            if self.is_place_valid_grid(grid, x, y, num):
                grid[y][x] = num
                self.count_solutions(grid, solutions, limit)
                grid[y][x] = 0
                if len(solutions) >= limit:
                    return

    def find_empty_location_grid(self, grid):
        for y in range(self.size):
            for x in range(self.size):
                if grid[y][x] == 0:
                    return y, x
        return None

    def is_place_valid_grid(self, grid, x, y, num):
        for i in range(self.size):
            if grid[y][i] == num or grid[i][x] == num:
                return False

        sec_x, sec_y = x // self.section_size, y // self.section_size
        for i in range(sec_y * self.section_size, (sec_y + 1) * self.section_size):
            for j in range(sec_x * self.section_size, (sec_x + 1) * self.section_size):
                if grid[i][j] == num:
                    return False

        return True

    def display_field(self):
        for y in range(self.size):
            row = ""
            for x in range(self.size):
                num = self.field[y][x]
                row += f"{num if num != 0 else '.'} "
                if (x + 1) % self.section_size == 0 and x < self.size - 1:
                    row += "| "
            print(row)
            if (y + 1) % self.section_size == 0 and y < self.size - 1:
                print("- " * (self.size + self.section_size))

    def get_first_empty_cell(self):
        for idx_y in range(0, self.size):
            for idx_x in range(0, self.size):
                if self.field[idx_y][idx_x] == 0:
                    return idx_x, idx_y
        return None

    def is_field_valid(self):
        for idx_y in range(0, self.size):
            for idx_x in range(0, self.size):
                if self.field[idx_y][idx_x] == 0:
                    continue

                num = self.field[idx_y][idx_x]
                self.field[idx_y][idx_x] = 0

                if self.is_place_valid(idx_x, idx_y, num):
                    self.field[idx_y][idx_x] = num
                else:
                    self.field[idx_y][idx_x] = num
                    return False
        return True

    def field_clear(self):
        self.field = copy.deepcopy(self.field_start)
        self.place_counter = 0