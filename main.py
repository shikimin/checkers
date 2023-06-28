import pygame
from checkerboard import CheckerBoard
from game_mechanics import Game

pygame.display.set_caption('Checkers!')

# Initialise game
pygame.init()
clock = pygame.time.Clock()

def main():
    is_running = True

    BOARD = CheckerBoard()
    GAME = Game(BOARD)
    start_location = None

    # Event loop
    while is_running:
        for event in pygame.event.get():
            #60 FPS
            clock.tick(60)
            
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # first click
                if start_location is None:
                    start_location = GAME.first_click(pygame.mouse.get_pos())

                # second click
                else:
                    start_location = GAME.second_click(start_location, pygame.mouse.get_pos())

        # draw board every loop
        BOARD.draw_board()
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__': main()