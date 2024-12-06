import tkinter as tk
from tkinter import ttk

from game import Game, FieldType
from renderer import Renderer
from config import WIDTH, HEIGHT, WHITE
from solver import Solver, SolverMode
from ui import SudokuUI


def main():

    root = tk.Tk()
    root.configure(bg='#FFE0B5')
    app = SudokuUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()
