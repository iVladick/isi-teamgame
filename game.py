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
    def __init__(self, field_type=FieldType.f9x9):
        self.field_type = field_type.value
        self.size = self.field_type['size']
        self.section_size = self.field_type['section_size']
        self.filled_range = self.field_type['filled_range']
        self.field = self._create_empty_field()
        self.fill_grid_backtracking()  # Fill the grid completely
        self.shuffle_grid()  # Shuffle for randomness
        self.remove_numbers_from_grid()  # Remove numbers to create the puzzle
        self.field_start = copy.deepcopy(self.field)

    def _create_empty_field(self):
        return [[0 for _ in range(self.size)] for _ in range(self.size)]

    def reset_field(self):
        self.field = copy.deepcopy(self.field_start)

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

    # Backtracking to fill the grid completely
    def fill_grid_backtracking(self) -> bool:
        empty = self.find_empty_location()
        if not empty:
            return True  # Grid fully filled
        y, x = empty

        numbers = list(range(1, self.size + 1))
        random.shuffle(numbers)  # Ensure randomness

        for num in numbers:
            if self.is_place_valid(x, y, num):
                self.field[y][x] = num
                if self.fill_grid_backtracking():
                    return True
                self.field[y][x] = 0  # Backtrack

        return False  # Trigger backtracking

    def find_empty_location(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.field[y][x] == 0:
                    return (y, x)
        return None

    # Removing numbers to create the puzzle
    def remove_numbers_from_grid(self):
        num_removed = 0
        num_to_remove = self.get_num_to_remove()

        attempts = num_to_remove * 2  # To prevent infinite loops

        while num_removed < num_to_remove and attempts > 0:
            y = random.randint(0, self.size - 1)
            x = random.randint(0, self.size - 1)

            if self.field[y][x] != 0:
                backup = self.field[y][x]
                self.field[y][x] = 0

                # Make a copy of the grid to pass to the solver
                grid_copy = copy.deepcopy(self.field)
                solutions = []
                self.count_solutions(grid_copy, solutions)

                if len(solutions) != 1:
                    self.field[y][x] = backup  # Restore if not unique
                else:
                    num_removed += 1
            attempts -= 1

        if num_removed < num_to_remove:
            print(f"Removed {num_removed} numbers out of requested {num_to_remove}")

    def get_num_to_remove(self):
        num_filled = random.choice(self.filled_range)
        return self.size * self.size - num_filled

    # Solver to count the number of solutions
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
                    return (y, x)
        return None

    def is_place_valid_grid(self, grid, x, y, num):
        # Check row and column
        for i in range(self.size):
            if grid[y][i] == num or grid[i][x] == num:
                return False

        # Check section
        sec_x, sec_y = x // self.section_size, y // self.section_size
        for i in range(sec_y * self.section_size, (sec_y + 1) * self.section_size):
            for j in range(sec_x * self.section_size, (sec_x + 1) * self.section_size):
                if grid[i][j] == num:
                    return False

        return True

    # Shuffling methods to ensure grid randomness
    def shuffle_grid(self):
        self.shuffle_rows_within_sections()
        self.shuffle_columns_within_sections()
        self.shuffle_sections()
        self.shuffle_columns()
        self.shuffle_rows()

    def shuffle_rows_within_sections(self):
        for sec in range(self.section_size):
            rows = list(range(sec * self.section_size, (sec + 1) * self.section_size))
            random.shuffle(rows)
            shuffled = [self.field[r] for r in rows]
            self.field[sec * self.section_size:(sec + 1) * self.section_size] = shuffled

    def shuffle_columns_within_sections(self):
        for sec in range(self.section_size):
            cols = list(range(sec * self.section_size, (sec + 1) * self.section_size))
            random.shuffle(cols)
            for row in self.field:
                shuffled_row = [row[c] for c in cols]
                row[:] = shuffled_row

    def shuffle_sections(self):
        sections = list(range(self.section_size))
        random.shuffle(sections)
        self.field = [self.field[y * self.section_size:(y + 1) * self.section_size] for y in sections]
        self.field = [item for sublist in self.field for item in sublist]

    def shuffle_columns(self):
        for _ in range(self.size):
            y = random.randint(0, self.size - 1)
            x1, x2 = random.sample(range(self.size), 2)
            self.field[y][x1], self.field[y][x2] = self.field[y][x2], self.field[y][x1]

    def shuffle_rows(self):
        for _ in range(self.size):
            y1, y2 = random.sample(range(self.size), 2)
            self.field[y1], self.field[y2] = self.field[y2], self.field[y1]

    # Displaying the grid
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
