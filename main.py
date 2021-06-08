import pygame

import chess
from chess.constants import BLACK, FPS, HEIGHT, WIDTH


def main():
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()
    board = chess.Board()

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                board.select_piece()
            if event.type == pygame.MOUSEBUTTONUP:
                board.unselect_piece()

            display.fill(BLACK)
            board.draw(display)
            pygame.display.update()


main()
