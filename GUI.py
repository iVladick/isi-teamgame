import tkinter as tk
from tkinter import messagebox
from config import WIDTH, HEIGHT, FIELD_RENDER_SIZE, WHITE, BLUE, FONT1_SIZE
from game import Game, FieldType

class SudokuGUI:
    def __init__(self, root, game):
        self.root = root
        self.root.title("Sudoku")
        self.game = game

        # Встановлення розмірів вікна
        self.root.geometry(f"{WIDTH}x{HEIGHT}")

        self.canvas = tk.Canvas(self.root, width=FIELD_RENDER_SIZE, height=FIELD_RENDER_SIZE, bg='WHITE')
        self.canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.create_grid()


    def create_grid(self):
        grid_size = self.game.size
        cell_size = FIELD_RENDER_SIZE / grid_size

        for i in range(grid_size + 1):
            # Горизонтальні лінії
            self.canvas.create_line(50,150+ i * cell_size, FIELD_RENDER_SIZE+50, 150+i * cell_size, fill="black", tags="grid")
            # Вертикальні лінії
            self.canvas.create_line(50+i * cell_size, 150, 50+i * cell_size, 150+FIELD_RENDER_SIZE, fill="black", tags="grid")

        section_size = int(grid_size ** 0.5)  # Розмір секції (3 для 9×9, 2 для 4×4)
        for i in range(section_size, grid_size, section_size):
            # Товсті горизонтальні лінії
            self.canvas.create_line(50, 150+i * cell_size, 50+FIELD_RENDER_SIZE, 150+i * cell_size, fill="black", width=2, tags="grid")
            # Товсті вертикальні лінії
            self.canvas.create_line(50+i * cell_size, 150,50+ i * cell_size, 150+FIELD_RENDER_SIZE, fill="black", width=2, tags="grid")
        self.fill_grid()

    def fill_grid(self):
        """Заповнення поля числами"""
        grid_size = self.game.size
        cell_size = FIELD_RENDER_SIZE / grid_size

        for row in range(grid_size):
            for col in range(grid_size):
                value = self.game.field[row][col]
                if value != 0:  # Якщо клітинка не порожня
                    x = col * cell_size + cell_size / 2 + 50
                    y = row * cell_size + cell_size / 2 + 150
                    self.canvas.create_text(x, y, text=str(value), font=("Arial", FONT1_SIZE), fill="blue", tags="grid")

    def update_grid(self):
        self.canvas.delete("grid")
        self.create_grid()

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(FieldType.f9x9)
    app = SudokuGUI(root, game)

    def change_game_field():
        game.field[0][0] = 5  # Зміна першої клітинки
        app.update_grid()  # Оновлення відображення

    root.after(3000, change_game_field)

    root.mainloop()
