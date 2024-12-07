import tkinter as tk

from ui import SudokuUI


def main():

    root = tk.Tk()
    root.configure(bg='#FFE0B5')
    app = SudokuUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()
