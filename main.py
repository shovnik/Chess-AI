import pygame, chess
from chess.constants import SQUARE_SIZE, WIDTH, HEIGHT, FPS

black_king = pygame.image.load("chess/sprites/black_king.png")


def main():
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()
    board = chess.Board()

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
            board.draw(display)
            # display.blit(
            #     pygame.transform.scale(PIECE_IMG, (SQUARE_SIZE, SQUARE_SIZE)),
            #     (3 * SQUARE_SIZE, 2 * SQUARE_SIZE),
            # )
            pygame.display.update()


main()
