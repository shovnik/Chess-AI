import pygame
from pygame.display import set_palette
from chess.constants import *


class Board:
    def __init__(self):
        self.turn = WHITE
        self.selected_x = None
        self.selected_y = None
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.board_surface = pygame.Surface((TILE_SIZE * ROWS, TILE_SIZE * COLS))
        for i in range(ROWS):
            for j in range(COLS):
                pygame.draw.rect(
                    self.board_surface,
                    DARK if (i + j) % 2 else LIGHT,
                    (i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                )
        self.sprite_map = {
            WHITE | PAWN: pygame.image.load("chess/sprites/white_pawn.png"),
            WHITE | KNIGHT: pygame.image.load("chess/sprites/white_knight.png"),
            WHITE | BISHOP: pygame.image.load("chess/sprites/white_bishop.png"),
            WHITE | ROOK: pygame.image.load("chess/sprites/white_rook.png"),
            WHITE | QUEEN: pygame.image.load("chess/sprites/white_queen.png"),
            WHITE | KING: pygame.image.load("chess/sprites/white_king.png"),
            BLACK | PAWN: pygame.image.load("chess/sprites/black_pawn.png"),
            BLACK | KNIGHT: pygame.image.load("chess/sprites/black_knight.png"),
            BLACK | BISHOP: pygame.image.load("chess/sprites/black_bishop.png"),
            BLACK | ROOK: pygame.image.load("chess/sprites/black_rook.png"),
            BLACK | QUEEN: pygame.image.load("chess/sprites/black_queen.png"),
            BLACK | KING: pygame.image.load("chess/sprites/black_king.png"),
        }
        for piece, sprite in self.sprite_map.items():
            self.sprite_map[piece] = pygame.transform.scale(
                sprite, (TILE_SIZE, TILE_SIZE)
            )
        self.setup_board()

    def setup_board(self, FEN=None):
        if FEN is None:
            FEN = INITIAL_POSITION
        fen_rows = FEN.split("/")
        fen_map = {
            "P": WHITE | PAWN,
            "N": WHITE | KNIGHT,
            "B": WHITE | BISHOP,
            "R": WHITE | ROOK,
            "Q": WHITE | QUEEN,
            "K": WHITE | KING,
            "p": BLACK | PAWN,
            "n": BLACK | KNIGHT,
            "b": BLACK | BISHOP,
            "r": BLACK | ROOK,
            "q": BLACK | QUEEN,
            "k": BLACK | KING,
        }

        for i in range(ROWS):
            j = 0
            for char in fen_rows[i]:
                if char.isdigit():
                    for _ in range(int(char)):
                        self.board[i][j] = 0
                        j += 1
                else:
                    self.board[i][j] = fen_map[char]
                    j += 1

    def draw(self, display):
        display.blit(self.board_surface, OFFSET)
        for i in range(ROWS):
            for j in range(COLS):
                if self.board[i][j] != 0:
                    sprite = self.sprite_map[self.board[i][j]]
                    if self.selected_y != i or self.selected_x != j:
                        display.blit(
                            sprite,
                            (j * TILE_SIZE + OFFSET[0], i * TILE_SIZE + OFFSET[1]),
                        )
    
    def draw_dragged(self, display):
        if self.selected_x is None:
            return
        sprite = self.sprite_map[self.board[self.selected_y][self.selected_x]]
        display.blit(
            sprite,
            sprite.get_rect(center=pygame.mouse.get_pos()),
        )

    def select_piece(self, x, y):
        if self.board[y][x] != 0 and self.board[y][x] & self.turn:
            self.selected_x = x
            self.selected_y = y

    def unselect_piece(self, x, y):
        if self.selected_x is None:
            return
        if x != self.selected_x or y != self.selected_y:
            self.board[y][x] = self.board[self.selected_y][self.selected_x]
            self.board[self.selected_y][self.selected_x] = 0
            self.turn = WHITE if self.turn == BLACK else BLACK
        self.selected_x = None
        self.selected_y = None