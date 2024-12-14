import tkinter as tk
from tkinter import ttk
import config
from game import Game, FieldType
from solver import Solver, SolverMode
import threading
import time


class SudokuUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.field_size_var = tk.StringVar(value="9x9")
        self.speed_var = tk.StringVar(value="Medium")
        self.solve_method_var = tk.StringVar(value="Backtracking")
        self.place_counter_var = tk.StringVar(value="0")
        self.game = None
        self.cells = []
        self.solver_thread = None
        self.stop_event = threading.Event()
        self.create_top_bar()
        self.create_game_field()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_top_bar(self):
        # First Row: Solve Method and Steps Count
        first_row = tk.Frame(self.root, bg='#FFE0B5')
        first_row.pack(side=tk.TOP, fill=tk.X, pady=5)

        solve_method_label = tk.Label(first_row, text="Solve Method:", bg='#DE8F5F', fg='#FFF2D7')
        solve_method_label.pack(side=tk.LEFT, padx=5)
        solve_method_dropdown = ttk.Combobox(
            first_row,
            textvariable=self.solve_method_var,
            values=["DFS", "Backtracking", "Forward checking"],
            state="readonly"
        )
        solve_method_dropdown.pack(side=tk.LEFT, padx=5)

        place_counter_label = tk.Label(first_row, text="Steps:", bg='#DE8F5F', fg='#FFF2D7')
        place_counter_label.pack(side=tk.LEFT, padx=5)
        place_counter_display = tk.Label(first_row, textvariable=self.place_counter_var, bg='#DE8F5F', fg='#FFF2D7')
        place_counter_display.pack(side=tk.LEFT, padx=5)

        # Second Row: Field Size, Generate Field, Clear Field
        second_row = tk.Frame(self.root, bg='#FFE0B5')
        second_row.pack(side=tk.TOP, fill=tk.X, pady=5)

        field_size_label = tk.Label(second_row, text="Field Size:", bg='#DE8F5F', fg='#FFF2D7')
        field_size_label.pack(side=tk.LEFT, padx=5)
        field_size_dropdown = ttk.Combobox(
            second_row,
            textvariable=self.field_size_var,
            values=["9x9", "4x4"],
            state="readonly"
        )
        field_size_dropdown.pack(side=tk.LEFT, padx=5)

        generate_button = tk.Button(second_row, text="Generate Field", command=self.generate_field, bg='#D57149',
                                    fg='#FFF2D7')
        generate_button.pack(side=tk.LEFT, padx=5, pady=5)

        clear_button = tk.Button(second_row, text="Clear Field", command=self.clear_field, bg='#D57149', fg='#FFF2D7')
        clear_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Third Row: Start, Stop, Speed
        third_row = tk.Frame(self.root, bg='#FFE0B5')
        third_row.pack(side=tk.TOP, fill=tk.X, pady=5)

        start_button = tk.Button(third_row, text="Start", command=self.start_game, bg='#D57149', fg='#FFF2D7')
        start_button.pack(side=tk.LEFT, padx=5, pady=5)

        stop_button = tk.Button(third_row, text="Stop", command=self.stop_game, bg='#D57149', fg='#FFF2D7')
        stop_button.pack(side=tk.LEFT, padx=5, pady=5)

        speed_label = tk.Label(third_row, text="Speed:", bg='#DE8F5F', fg='#FFF2D7')
        speed_label.pack(side=tk.LEFT, padx=5)
        speed_dropdown = ttk.Combobox(
            third_row,
            textvariable=self.speed_var,
            values=["Fast", "Medium", "Slow"],
            state="readonly"
        )
        speed_dropdown.pack(side=tk.LEFT, padx=5)

    def clear_field(self):
        if self.game:
            self.game.field_clear()
            self.update_steps()
            self.update_grid()
        else:
            for row_cells in self.cells:
                for cell in row_cells:
                    cell.config(text="")
            self.place_counter_var.set(0)

    def create_game_field(self):
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(padx=10, pady=10)
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
                    justify='center',
                    bg=config.FIELD_SECTOR_COLOR if (
                                (row // section_size + col // section_size) % 2 == 0) else config.FIELD_SECTOR_COLOR2
                )
                cell.grid(row=row, column=col, sticky='nsew')
                row_cells.append(cell)
            self.cells.append(row_cells)
        for i in range(size):
            self.grid_frame.grid_rowconfigure(i, weight=1)
            self.grid_frame.grid_columnconfigure(i, weight=1)

    def generate_field(self):
        field_type = FieldType.f9x9 if self.field_size_var.get() == "9x9" else FieldType.f4x4
        self.game = Game(self.on_place, field_type=field_type)
        self.update_steps()
        self.draw_grid()
        self.update_grid()

    def start_game(self):
        if not self.game or (self.solver_thread and self.solver_thread.is_alive()):
            return

        self.stop_event.clear()

        solve_mode = None
        match self.solve_method_var.get():
            case "DFS":
                solve_mode = SolverMode.DFS
            case "Backtracking":
                solve_mode = SolverMode.BACKTRACKING
            case "Forward checking":
                solve_mode = SolverMode.FORWARD_CHECKING

        self.solver_thread = threading.Thread(target=self.run_solver, args=(solve_mode,), daemon=True)
        self.solver_thread.start()
        self.health_check()

    def run_solver(self, solve_mode):
        solver = Solver(self.game, self.stop_event, self.get_delay, mode=solve_mode)
        solver.solve()

        self.root.after(0, self.update_grid)
        self.root.after(0, lambda: self.update_steps())

    def on_place(self):
        # Schedule UI update in the main thread
        self.root.after(0, self.update_grid)
        self.root.after(0, lambda: self.update_steps())

    def update_steps(self):
        self.place_counter_var.set(f'{self.game.place_counter:,}')

    def stop_game(self):
        if self.solver_thread and self.solver_thread.is_alive():
            self.stop_event.set()
            self.solver_thread.join(timeout=.2)  # Wait for the thread to finish

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

    def get_delay(self):
        speed = self.speed_var.get()
        if speed == "Fast":
            return 0.01  # 20 ms
        elif speed == "Medium":
            return 0.2  # 200 ms
        elif speed == "Slow":
            return 1.0  # 1000 ms
        return 0.2  # Default to Medium

    def health_check(self):
        if self.solver_thread and self.solver_thread.is_alive():
            self.root.after(3000, self.health_check)
        else:
            pass

    def on_closing(self):
        self.stop_game()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuUI(root)
    root.mainloop()
