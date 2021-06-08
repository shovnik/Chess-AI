import pygame

import chess.bit_board_util as bbu
from chess.game_state import GameState
from chess.constants import *


class Board:
    def __init__(self):
        self.turn = WHITE
        self.selected_mask = None
        self.selected_piece = None
        self.state = GameState()
        self.board_surface = pygame.Surface((TILE_SIZE * ROWS, TILE_SIZE * COLS))
        for i in range(ROWS):
            for j in range(COLS):
                pygame.draw.rect(
                    self.board_surface,
                    DARK if (i + j) % 2 else LIGHT,
                    (i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                )
        self.sprite_map = {}
        for piece, sprite_path in SPRITES.items():
            self.sprite_map[piece] = pygame.transform.scale(
                pygame.image.load(sprite_path), (TILE_SIZE, TILE_SIZE)
            )

    def draw(self, display):
        display.blit(self.board_surface, OFFSET)
        for n in bbu.scan(self.state.pawn & self.state.white):
            x, y, mask = n % ROWS, 7 - n // COLS, 1 << n
            if mask != self.selected_mask:
                display.blit(
                    self.sprite_map[PAWN | WHITE],
                    (x * TILE_SIZE + OFFSET[0], y * TILE_SIZE + OFFSET[1]),
                )
        for n in bbu.scan(self.state.knight & self.state.white):
            x, y, mask = n % ROWS, 7 - n // COLS, 1 << n
            if mask != self.selected_mask:
                display.blit(
                    self.sprite_map[KNIGHT | WHITE],
                    (x * TILE_SIZE + OFFSET[0], y * TILE_SIZE + OFFSET[1]),
                )
        for n in bbu.scan(self.state.bishop & self.state.white):
            x, y, mask = n % ROWS, 7 - n // COLS, 1 << n
            if mask != self.selected_mask:
                display.blit(
                    self.sprite_map[BISHOP | WHITE],
                    (x * TILE_SIZE + OFFSET[0], y * TILE_SIZE + OFFSET[1]),
                )
        for n in bbu.scan(self.state.rook & self.state.white):
            x, y, mask = n % ROWS, 7 - n // COLS, 1 << n
            if mask != self.selected_mask:
                display.blit(
                    self.sprite_map[ROOK | WHITE],
                    (x * TILE_SIZE + OFFSET[0], y * TILE_SIZE + OFFSET[1]),
                )
        for n in bbu.scan(self.state.queen & self.state.white):
            x, y, mask = n % ROWS, 7 - n // COLS, 1 << n
            if mask != self.selected_mask:
                display.blit(
                    self.sprite_map[QUEEN | WHITE],
                    (x * TILE_SIZE + OFFSET[0], y * TILE_SIZE + OFFSET[1]),
                )
        for n in bbu.scan(self.state.king & self.state.white):
            x, y, mask = n % ROWS, 7 - n // COLS, 1 << n
            if mask != self.selected_mask:
                display.blit(
                    self.sprite_map[KING | WHITE],
                    (x * TILE_SIZE + OFFSET[0], y * TILE_SIZE + OFFSET[1]),
                )
        for n in bbu.scan(self.state.pawn & self.state.black):
            x, y, mask = n % ROWS, 7 - n // COLS, 1 << n
            if mask != self.selected_mask:
                display.blit(
                    self.sprite_map[PAWN | BLACK],
                    (x * TILE_SIZE + OFFSET[0], y * TILE_SIZE + OFFSET[1]),
                )
        for n in bbu.scan(self.state.knight & self.state.black):
            x, y, mask = n % ROWS, 7 - n // COLS, 1 << n
            if mask != self.selected_mask:
                display.blit(
                    self.sprite_map[KNIGHT | BLACK],
                    (x * TILE_SIZE + OFFSET[0], y * TILE_SIZE + OFFSET[1]),
                )
        for n in bbu.scan(self.state.bishop & self.state.black):
            x, y, mask = n % ROWS, 7 - n // COLS, 1 << n
            if mask != self.selected_mask:
                display.blit(
                    self.sprite_map[BISHOP | BLACK],
                    (x * TILE_SIZE + OFFSET[0], y * TILE_SIZE + OFFSET[1]),
                )
        for n in bbu.scan(self.state.rook & self.state.black):
            x, y, mask = n % ROWS, 7 - n // COLS, 1 << n
            if mask != self.selected_mask:
                display.blit(
                    self.sprite_map[ROOK | BLACK],
                    (x * TILE_SIZE + OFFSET[0], y * TILE_SIZE + OFFSET[1]),
                )
        for n in bbu.scan(self.state.queen & self.state.black):
            x, y, mask = n % ROWS, 7 - n // COLS, 1 << n
            if mask != self.selected_mask:
                display.blit(
                    self.sprite_map[QUEEN | BLACK],
                    (x * TILE_SIZE + OFFSET[0], y * TILE_SIZE + OFFSET[1]),
                )
        for n in bbu.scan(self.state.king & self.state.black):
            x, y, mask = n % ROWS, 7 - n // COLS, 1 << n
            if mask != self.selected_mask:
                display.blit(
                    self.sprite_map[KING | BLACK],
                    (x * TILE_SIZE + OFFSET[0], y * TILE_SIZE + OFFSET[1]),
                )

    def draw_dragged(self, display):
        if self.selected_mask is None:
            return
        sprite = self.sprite_map[self.selected_piece | self.state.turn]
        display.blit(
            sprite,
            sprite.get_rect(center=pygame.mouse.get_pos()),
        )

    def select_piece(self, x, y):
        mask = 1 << ((7 - y) * ROWS + x)
        if (self.state.white & mask and self.state.turn == WHITE) or (
            self.state.black & mask and self.state.turn == BLACK
        ):
            self.selected_mask = mask
            self.selected_piece = self.state.get_piece(mask)

    def unselect_piece(self, x, y):
        if self.selected_mask is None:
            return
        mask = 1 << ((7 - y) * ROWS + x)
        self.state.move(self.selected_mask, mask)
        self.selected_mask = None
