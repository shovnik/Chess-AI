import chess.bit_board_util as bbu
from chess.constants import (
    BISHOP,
    COLS,
    KING,
    KNIGHT,
    PAWN,
    QUEEN,
    ROOK,
    ROWS,
    TILES,
    WHITE,
)

Bitboard = int
BB_EMPTY = 0
BB_ALL = 0xFFFF_FFFF_FFFF_FFFF
# fmt: off
BB_TILES = [
    BB_A1, BB_B1, BB_C1, BB_D1, BB_E1, BB_F1, BB_G1, BB_H1,
    BB_A2, BB_B2, BB_C2, BB_D2, BB_E2, BB_F2, BB_G2, BB_H2,
    BB_A3, BB_B3, BB_C3, BB_D3, BB_E3, BB_F3, BB_G3, BB_H3,
    BB_A4, BB_B4, BB_C4, BB_D4, BB_E4, BB_F4, BB_G4, BB_H4,
    BB_A5, BB_B5, BB_C5, BB_D5, BB_E5, BB_F5, BB_G5, BB_H5,
    BB_A6, BB_B6, BB_C6, BB_D6, BB_E6, BB_F6, BB_G6, BB_H6,
    BB_A7, BB_B7, BB_C7, BB_D7, BB_E7, BB_F7, BB_G7, BB_H7,
    BB_A8, BB_B8, BB_C8, BB_D8, BB_E8, BB_F8, BB_G8, BB_H8,
] = [1 << i for i in range(TILES)]

BB_FILES = [
    BB_FILE_A, BB_FILE_B, BB_FILE_C, BB_FILE_D, BB_FILE_E, BB_FILE_F, BB_FILE_G, BB_FILE_H,
] = [0x0101_0101_0101_0101 << i for i in range(COLS)]

BB_RANKS = [
    BB_RANK_1,
    BB_RANK_2,
    BB_RANK_3,
    BB_RANK_4,
    BB_RANK_5,
    BB_RANK_6,
    BB_RANK_7,
    BB_RANK_8,
] = [0xff << (COLS * i) for i in range(ROWS)]
# fmt: on

BB_BACKRANKS = BB_RANK_1 | BB_RANK_8
BB_CORNERS = BB_A1 | BB_H1 | BB_A8 | BB_H8
BB_CENTER = BB_D4 | BB_E4 | BB_D5 | BB_E5

BB_LIGHT_TILES = 0x55AA_55AA_55AA_55AA
BB_DARK_TILES = 0xAA55_AA55_AA55_AA55


class GameState:
    def __init__(self):
        self.turn = WHITE
        self.occupied = BB_RANK_1 | BB_RANK_2 | BB_RANK_7 | BB_RANK_8
        self.white = BB_RANK_1 | BB_RANK_2
        self.black = BB_RANK_7 | BB_RANK_8
        self.pawn = BB_RANK_2 | BB_RANK_7
        self.knight = BB_B1 | BB_G1 | BB_B8 | BB_G8
        self.bishop = BB_C1 | BB_F1 | BB_C8 | BB_F8
        self.rook = BB_A1 | BB_H1 | BB_A8 | BB_H8
        self.queen = BB_D1 | BB_D8
        self.king = BB_E1 | BB_E8
        self.knight_attacks = {}
        self.king_attacks = {}
        self.legal_moves = set()

        self._pregenerate_attacks()
        self._update_legal_moves()

    def _pregenerate_attacks(self):
        def get_shift_mask(source, shifts):
            attacks = BB_EMPTY
            for shift in shifts:
                target = source + shift
                if 0 <= target < 64 and abs(source % COLS - target % COLS) <= 2:
                    attacks |= BB_TILES[target]
            return attacks

        for i in range(TILES):
            self.knight_attacks[BB_TILES[i]] = get_shift_mask(
                i, [-6, -10, -15, -17, 6, 10, 15, 17]
            )
            self.king_attacks[BB_TILES[i]] = get_shift_mask(
                i, [-9, -8, -7, -1, 1, 7, 8, 9]
            )

    def _update_legal_moves(self):
        self.legal_moves = set()
        ally_mask = self.white if self.turn == WHITE else self.black
        for from_tile in bbu.scan(ally_mask):
            from_mask = BB_TILES[from_tile]
            piece = self.get_piece(from_mask)
            if piece == KNIGHT:
                for to_tile in bbu.scan(self.knight_attacks[from_mask] & ~ally_mask):
                    self.legal_moves.add((from_mask, BB_TILES[to_tile]))
            if piece == KING:
                for to_tile in bbu.scan(self.king_attacks[from_mask] & ~ally_mask):
                    self.legal_moves.add((from_mask, BB_TILES[to_tile]))

    def move(self, from_mask, to_mask):
        if from_mask == to_mask:
            return
        if (
            (self.get_piece(from_mask) == KNIGHT
            or self.get_piece(from_mask) == KING)
            and (from_mask, to_mask) not in self.legal_moves
        ):
            return
        piece = self.get_piece(from_mask)
        self._remove_piece(from_mask)
        self._remove_piece(to_mask)
        self._set_piece(to_mask, piece)
        self.turn = not self.turn
        self._update_legal_moves()

    def get_piece(self, mask):
        if not self.occupied & mask:
            return None
        if self.pawn & mask:
            return PAWN
        if self.knight & mask:
            return KNIGHT
        if self.bishop & mask:
            return BISHOP
        if self.rook & mask:
            return ROOK
        if self.queen & mask:
            return QUEEN
        return KING

    def _remove_piece(self, mask):
        self.occupied &= ~mask
        self.white &= ~mask
        self.black &= ~mask
        self.pawn &= ~mask
        self.knight &= ~mask
        self.bishop &= ~mask
        self.rook &= ~mask
        self.queen &= ~mask
        self.king &= ~mask

    def _set_piece(self, mask, piece):
        self.occupied |= mask
        if self.turn == WHITE:
            self.white |= mask
        else:
            self.black |= mask

        if piece == PAWN:
            self.pawn |= mask
        if piece == KNIGHT:
            self.knight |= mask
        if piece == BISHOP:
            self.bishop |= mask
        if piece == ROOK:
            self.rook |= mask
        if piece == QUEEN:
            self.queen |= mask
        if piece == KING:
            self.king |= mask
