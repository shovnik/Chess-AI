import pygame
from chess.constants import ROWS, COLS, BLACK, WHITE, SQUARE_SIZE


class Board:
    def __init__(self):
        self.board = []

    def draw(self, display):
        display.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(
                    display,
                    WHITE,
                    (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                )
