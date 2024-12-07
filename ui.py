import tkinter as tk
from tkinter import ttk
import config
from game import Game, FieldType
from solver import Solver, SolverMode
import time


# TODO
# https://pythonassets.com/posts/background-tasks-with-tk-tkinter/

class SudokuUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.field_size_var = tk.StringVar(value="9x9")
        self.speed_var = tk.StringVar(value="Medium")
        self.solve_method_var = tk.StringVar(value="Backtracking")
        self.game = None
        self.cells = []
        self.create_top_bar()
        self.create_game_field()

    def create_top_bar(self):
        top_frame1 = tk.Frame(self.root, bg='#FFE0B5')
        top_frame1.pack(side=tk.TOP, fill=tk.X)

        start_button = tk.Button(top_frame1, text="Start", command=self.start_game, bg='#D57149', fg='#FFF2D7')
        start_button.pack(side=tk.LEFT, padx=5, pady=5)

        stop_button = tk.Button(top_frame1, text="Stop", command=self.stop_game, bg='#D57149', fg='#FFF2D7')
        stop_button.pack(side=tk.LEFT, padx=5, pady=5)

        speed_label = tk.Label(top_frame1, text="Speed:", bg='#DE8F5F', fg='#FFF2D7')
        speed_label.pack(side=tk.LEFT, padx=5)
        speed_dropdown = ttk.Combobox(
            top_frame1,
            textvariable=self.speed_var,
            values=["Fast", "Medium", "Slow"],
            state="readonly"
        )
        speed_dropdown.pack(side=tk.LEFT, padx=5)

        solve_method_label = tk.Label(top_frame1, text="Solve Method:", bg='#DE8F5F', fg='#FFF2D7')
        solve_method_label.pack(side=tk.LEFT, padx=5)
        solve_method_dropdown = ttk.Combobox(
            top_frame1,
            textvariable=self.solve_method_var,
            values=["DFS", "Backtracking", "Forward checking"],
            state="readonly"
        )
        solve_method_dropdown.pack(side=tk.LEFT, padx=5)

        top_frame2 = tk.Frame(self.root, bg='#FFE0B5')
        top_frame2.pack(side=tk.TOP, fill=tk.X)

        field_size_label = tk.Label(top_frame2, text="Field Size:", bg='#DE8F5F', fg='#FFF2D7')
        field_size_label.pack(side=tk.LEFT, padx=5)
        field_size_dropdown = ttk.Combobox(
            top_frame2,
            textvariable=self.field_size_var,
            values=["9x9", "4x4"],
            state="readonly"
        )
        field_size_dropdown.pack(side=tk.LEFT, padx=5)

        generate_button = tk.Button(top_frame2, text="Generate Field", command=self.generate_field, bg='#D57149', fg='#FFF2D7')
        generate_button.pack(side=tk.LEFT, padx=5, pady=5)

        clear_button = tk.Button(top_frame2, text="Clear Field", command=self.clear_field, bg='#D57149', fg='#FFF2D7')
        clear_button.pack(side=tk.LEFT, padx=5, pady=5)

    def clear_field(self):
        if self.game:
            self.game.field_clear()
            self.update_grid()
        else:
            for row_cells in self.cells:
                for cell in row_cells:
                    cell.config(text="")

    def create_game_field(self):
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack()
        self.draw_grid()

    def draw_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        self.cells = []
        size = 9 if self.field_size_var.get() == "9x9" else 4
        section_size = 3 if size == 9 else 2
        for row in range(size):
            row_cells = []
            for col in range(size):
                cell = tk.Label(
                    self.grid_frame,
                    width=2,
                    font=('Arial', 24),
                    borderwidth=1,
                    relief='solid',
                    justify='center'
                )
                cell.grid(row=row, column=col, sticky='nsew')
                sector_row = row // section_size
                sector_col = col // section_size
                if (sector_row + sector_col) % 2 == 0:
                    bg_color = config.FIELD_SECTOR_COLOR
                else:
                    bg_color = config.FIELD_SECTOR_COLOR2
                cell.config(bg=bg_color)
                row_cells.append(cell)
            self.cells.append(row_cells)
        for i in range(size):
            self.grid_frame.grid_rowconfigure(i, weight=1)
            self.grid_frame.grid_columnconfigure(i, weight=1)

    def generate_field(self):
        field_type = FieldType.f9x9 if self.field_size_var.get() == "9x9" else FieldType.f4x4
        self.game = Game(self.solve_tick, field_type=field_type)
        self.draw_grid()
        self.update_grid()

    def start_game(self):
        if not self.game:
            return

        solve_mode = None

        match self.solve_method_var.get():
            case "DFS":
                solve_mode = SolverMode.DFS
            case "Backtracking":
                solve_mode = SolverMode.BACKTRACKING
            case "Forward checking":
                solve_mode = SolverMode.FORWARD_CHECKING

        solver = Solver(self.game, solve_mode)
        solver.solve()

    def solve_tick(self):
        delay = self.get_delay(self.speed_var.get())
        time.sleep(delay)
        self.update_grid()
        self.root.update_idletasks()

    def stop_game(self):
        if self.game:
            self.game.field_clear()
            self.update_grid()
        else:
            for row_cells in self.cells:
                for cell in row_cells:
                    cell.config(text="")

    def update_grid(self):
        if not self.game:
            return
        size = self.game.size
        for y in range(size):
            for x in range(size):
                value = self.game.field[y][x]
                cell = self.cells[y][x]
                if value != 0:
                    cell.config(text=str(value))
                else:
                    cell.config(text="")

    def get_delay(self, speed):
        if speed == "Fast":
            return 0
        elif speed == "Medium":
            return .100
        elif speed == "Slow":
            return .500


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuUI(root)
    root.mainloop()
