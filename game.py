from enum import Enum
import random


class FieldType(Enum):
    f9x9 = 9, 3
    f4x4 = 4, 2


class Game:
    def __init__(self, field_type=FieldType.f9x9):
        self.field_type = field_type
        self.field = self._create_empty_field()

    def _create_empty_field(self):
        size = self.field_type.value[0]
        return [[0 for _ in range(size)] for _ in range(size)]

    # def random_fill(self):
    #     size = self.field_type.value[0]
    #     return [[(x + y) % 9 + 1 for x in range(size)] for y in range(size)]

    def reset_field(self):
        self.field = self._create_empty_field()

    def is_section_contains(self, x: int, y: int, num: int) -> bool:
        size, section_size = self.field_type.value
        section_y, section_x = y // section_size, x // section_size

        for idx_y in range(section_y * section_size, (section_y + 1) * section_size):
            for idx_x in range(section_x * section_size, (section_x + 1) * section_size):
                if self.field[idx_y][idx_x] == num:
                    return True
        return False

    def is_col_row_contains(self, x: int, y: int, num: int) -> bool:
        size = self.field_type.value[0]

        for idx in range(size):
            if self.field[idx][x] == num or self.field[y][idx] == num:
                return True

        return False

    def is_place_valid(self, x: int, y: int, num: int) -> bool:
        size = self.field_type.value[0]

        if not (0 <= x < size and 0 <= y < size and 0 <= num <= size):
            raise ValueError(f"Invalid data {x} {y} {num} for is_place_valid")

        return not (self.is_section_contains(x, y, num) and self.is_col_row_contains(x, y, num))

    def place_number(self, x: int, y: int, num: int):
        self.field[y][x] = num

    def fill_random(self):
        size = self.field_type.value[0]

        numbers = list(range(1, size + 1))

        for i in range(size):
            for j in range(size):
                if self.field[i][j] == 0:
                    random.shuffle(numbers)
                    for val in numbers:
                        if self.is_place_valid(i, j, val):
                            self.field[i][j] = val
                            if self.fill_random():
                                return True
                            self.field[i][j] = 0
                    return False
        return True
