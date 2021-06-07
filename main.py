import pygame, chess
from chess.constants import (
    FPS,
    WIDTH,
    HEIGHT,
    OFFSET,
    ROWS,
    COLS,
    TILE_SIZE,
    RED,
    BLACK,
)


def get_tile():
    position = pygame.mouse.get_pos()
    return (
        int(position[0] - OFFSET[0]) // TILE_SIZE,
        int(position[1] - OFFSET[1]) // TILE_SIZE,
    )


def mouse_highlight(display, x, y):
    if x >= 0 and y >= 0 and x < COLS and y < ROWS:
        pygame.draw.rect(
            display,
            RED,
            (
                OFFSET[0] + x * TILE_SIZE,
                OFFSET[1] + y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE,
            ),
            2,
        )


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

            tile_x, tile_y = get_tile()
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.select_piece(tile_x, tile_y)
            if event.type == pygame.MOUSEBUTTONUP:
                board.unselect_piece(tile_x, tile_y)

            display.fill(BLACK)
            board.draw(display)
            mouse_highlight(display, tile_x, tile_y)
            board.draw_dragged(display)
            pygame.display.update()


main()
