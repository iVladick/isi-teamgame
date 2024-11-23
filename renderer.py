import pygame
from config import WIDTH, HEIGHT, FIELD_RENDER_SIZE, WHITE, BLUE, BLACK, RED, FONT1_SIZE, FONT2_SIZE


class Renderer:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font1 = pygame.font.SysFont("comicsans", FONT1_SIZE)
        self.font2 = pygame.font.SysFont("comicsans", FONT2_SIZE)

    def render_grid(self, original_grid):
        size = self.game.field_type.value[0]

        for row in range(size):
            for col in range(size):
                value = self.game.field[row][col]
                if value != 0:
                    self._draw_cell(row, col, value, original_grid[row][col] != 0)
        self._draw_lines()

    def highlight_cell(self, x, y):
        for i in range(2):
            self._draw_highlight(x, y, i)

    def render_value(self, x, y, value):
        self._draw_text(self.font1, str(value), x, y, BLACK)

    def show_error(self, error_type: int):
        messages = {
            1: "Cannot solve this puzzle!",
            2: "Invalid move!",
        }
        self._draw_message(self.font1, messages.get(error_type, ""), RED, 20)

    def render_instructions(self):
        self._draw_message(self.font2, "PRESS D TO RESET / R TO EMPTY / N FOR NEW PUZZLE", BLACK, 520)
        self._draw_message(self.font2, "ENTER VALUES AND PRESS ENTER TO SOLVE", BLACK, 540)

    def render_result(self):
        self._draw_message(self.font1, "SOLVED! PRESS N FOR NEW PUZZLE", BLACK, 570)

    def _cell_dif(self):
        return FIELD_RENDER_SIZE // self.game.field_type.value[0]

    def _draw_cell(self, row, col, value, is_original):

        dif = self._cell_dif()

        start_off = (WIDTH - FIELD_RENDER_SIZE) // 2

        color = BLUE if is_original else (128, 128, 128)
        if is_original:
            pygame.draw.rect(self.screen, color, (start_off+col * dif, row * dif, dif + 1, dif + 1))
        self._draw_text(self.font1, str(value), col, row, BLACK if is_original else color)

    def _draw_lines(self):

        size = self.game.field_type.value[0]
        gap = self.game.field_type.value[1]
        dif = self._cell_dif()

        start_off = (WIDTH - FIELD_RENDER_SIZE) // 2

        for i in range(size + 1):
            thickness = 7 if i % gap == 0 else 1
            pygame.draw.line(self.screen, BLACK, (start_off, i * dif), (start_off + FIELD_RENDER_SIZE, i * dif),
                             thickness)
            pygame.draw.line(self.screen, BLACK, (start_off + i * dif, 0), (start_off + i * dif, FIELD_RENDER_SIZE),
                             thickness)

    def _draw_highlight(self, x, y, i):

        dif = self._cell_dif()

        pygame.draw.line(self.screen, RED, (x * dif - 3, (y + i) * dif),
                         (x * dif + dif + 3, (y + i) * dif), 7)
        pygame.draw.line(self.screen, RED, ((x + i) * dif, y * dif),
                         ((x + i) * dif, y * dif + dif), 7)

    def _draw_text(self, font, text, col, row, color):

        dif = self._cell_dif()

        start_off = (WIDTH - FIELD_RENDER_SIZE) // 2

        rendered_text = font.render(text, True, color)
        self.screen.blit(rendered_text, (start_off + col * dif + 15, row * dif + 15))

    def _draw_message(self, font, message, color, y_offset):
        text = font.render(message, True, color)
        self.screen.blit(text, (20, y_offset))
