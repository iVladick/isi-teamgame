import pygame
from game import Game, FieldType
from renderer import Renderer
from config import WIDTH, HEIGHT, WHITE


def main():
    pygame.init()
    # screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # pygame.display.set_caption("Sudoku")
    # screen.fill(WHITE)

    game = Game(FieldType.f9x9)
    # renderer = Renderer(screen, game)

    # game.fill_random()
    game.display_field()
    # running = True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #
    #     renderer.render_grid()
    #     pygame.display.update()
    #
    # pygame.quit()


if __name__ == "__main__":
    main()
