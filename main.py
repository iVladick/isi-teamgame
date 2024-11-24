
from game import Game, FieldType
from renderer import Renderer
from config import WIDTH, HEIGHT, WHITE
from solver import Solver, SolverMode


def main():

    game = Game(FieldType.f9x9)
    game.display_field()

    solver = Solver(game, SolverMode.BACKTRACKING)

    solver.solve()

    game.display_field()


if __name__ == "__main__":
    main()
