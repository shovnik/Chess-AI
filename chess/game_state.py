from pygame.version import ver

import chess.bb_utils as bbu
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

# A1 to H8
BB_DIAGS = [
    0x0000_0000_0000_0001,
    0x0000_0000_0000_0102,
    0x0000_0000_0001_0204,
    0x0000_0000_0102_0408,
    0x0000_0001_0204_0810,
    0x0000_0102_0408_1020,
    0x0001_0204_0810_2040,
    0x0102_0408_1020_4080,
    0x0204_0810_2040_8000,
    0x0408_1020_4080_0000,
    0x0810_2040_8000_0000,
    0x1020_4080_0000_0000,
    0x2040_8000_0000_0000,
    0x4080_0000_0000_0000,
    0x8000_0000_0000_0000,
]

# A8 to H1
BB_ANTI_DIAGS = [
    0x0000_0000_0000_0080,
    0x0000_0000_0000_8040,
    0x0000_0000_0080_4020,
    0x0000_0000_8040_2010,
    0x0000_0080_4020_1008,
    0x0000_8040_2010_0804,
    0x0080_4020_1008_0402,
    0x8040_2010_0804_0201,
    0x4020_1008_0402_0100,
    0x2010_0804_0201_0000,
    0x1008_0402_0100_0000,
    0x0804_0201_0000_0000,
    0x0402_0100_0000_0000,
    0x0201_0000_0000_0000,
    0x0100_0000_0000_0000,
]

WHITE_PAWN_ATTACKS = {}
BLACK_PAWN_ATTACKS = {}
KNIGHT_ATTACKS = {}
BISHOP_ATTACKS = {}
ROOK_ATTACKS = {}
KING_ATTACKS = {}


def get_shift_mask(source, shifts):
    attacks = BB_EMPTY
    for shift in shifts:
        target = source + shift
        if 0 <= target < 64 and abs(source % COLS - target % COLS) <= 2:
            attacks |= BB_TILES[target]
    return attacks


for i in range(TILES):
    WHITE_PAWN_ATTACKS[BB_TILES[i]] = get_shift_mask(i, [7, 9])
    BLACK_PAWN_ATTACKS[BB_TILES[i]] = get_shift_mask(i, [-7, -9])
    KNIGHT_ATTACKS[BB_TILES[i]] = get_shift_mask(i, [-6, -10, -15, -17, 6, 10, 15, 17])
    BISHOP_ATTACKS[BB_TILES[i]] = (
        BB_DIAGS[i // 8 + i % 8] ^ BB_ANTI_DIAGS[i // 8 + 7 - i % 8]
    )
    ROOK_ATTACKS[BB_TILES[i]] = BB_RANKS[i // 8] ^ BB_FILES[i % 8]
    KING_ATTACKS[BB_TILES[i]] = get_shift_mask(i, [-9, -8, -7, -1, 1, 7, 8, 9])


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
        self.en_passant_mask = 0
        self.legal_moves = set()

        self._update_legal_moves()

    def _update_legal_moves(self):
        self.legal_moves = set()
        ally_mask = self.white if self.turn else self.black
        for from_tile in bbu.scan(ally_mask):
            from_mask = BB_TILES[from_tile]
            piece = self.get_piece(from_mask)
            if piece == PAWN:
                self._update_legal_pawn_moves(from_mask)
            elif piece == KNIGHT:
                self._update_legal_knight_moves(from_mask, ally_mask)
            elif piece == BISHOP:
                self._update_legal_bishop_moves(from_mask, from_tile, ally_mask)
            elif piece == ROOK:
                self._update_legal_rook_moves(from_mask, from_tile, ally_mask)
            elif piece == QUEEN:
                self._update_legal_bishop_moves(from_mask, from_tile, ally_mask)
                self._update_legal_rook_moves(from_mask, from_tile, ally_mask)
            else:
                self._update_legal_king_moves(from_mask, ally_mask)

    def _update_legal_pawn_moves(self, from_mask):
        if self.turn:
            single_push_mask = from_mask << 8 & ~self.occupied
            double_push_mask = (
                (from_mask << 16 & ~self.occupied & ~(self.occupied << 8))
                if from_mask & BB_RANK_2
                else 0
            )
            for to_tile in bbu.scan(
                WHITE_PAWN_ATTACKS[from_mask] & (self.black | self.en_passant_mask)
            ):
                self.legal_moves.add((from_mask, BB_TILES[to_tile]))
        else:
            single_push_mask = from_mask >> 8 & ~self.occupied
            double_push_mask = (
                (from_mask >> 16 & ~self.occupied & ~(self.occupied >> 8))
                if from_mask & BB_RANK_7
                else 0
            )
            for to_tile in bbu.scan(
                BLACK_PAWN_ATTACKS[from_mask] & (self.white | self.en_passant_mask)
            ):
                self.legal_moves.add((from_mask, BB_TILES[to_tile]))
        if single_push_mask:
            self.legal_moves.add((from_mask, single_push_mask))
        if double_push_mask:
            self.legal_moves.add((from_mask, double_push_mask))

    def _update_legal_knight_moves(self, from_mask, ally_mask):
        for to_tile in bbu.scan(KNIGHT_ATTACKS[from_mask] & ~ally_mask):
            self.legal_moves.add((from_mask, BB_TILES[to_tile]))

    def _update_legal_bishop_moves(self, from_mask, from_tile, ally_mask):
        diag_mask = BB_DIAGS[from_tile // 8 + from_tile % 8]
        diag_mask = ((self.occupied & diag_mask) - 2 * from_mask) ^ bbu.flip_diags(
            bbu.flip_diags(self.occupied & diag_mask) - 2 * bbu.flip_diags(from_mask)
        )
        anti_diag_mask = BB_ANTI_DIAGS[from_tile // 8 + 7 - from_tile % 8]
        anti_diag_mask = (
            (self.occupied & anti_diag_mask) - 2 * from_mask
        ) ^ bbu.flip_anti_diags(
            bbu.flip_anti_diags(self.occupied & anti_diag_mask)
            - 2 * bbu.flip_anti_diags(from_mask)
        )
        for to_tile in bbu.scan(
            (diag_mask | anti_diag_mask) & BISHOP_ATTACKS[from_mask] & ~ally_mask
        ):
            self.legal_moves.add((from_mask, BB_TILES[to_tile]))

    def _update_legal_rook_moves(self, from_mask, from_tile, ally_mask):
        rank_mask = (self.occupied - 2 * from_mask) ^ bbu.flip_ranks(
            bbu.flip_ranks(self.occupied) - 2 * bbu.flip_ranks(from_mask)
        )
        file_mask = BB_FILES[from_tile % 8]
        file_mask = ((self.occupied & file_mask) - 2 * from_mask) ^ bbu.flip_files(
            bbu.flip_files(self.occupied & file_mask) - 2 * bbu.flip_files(from_mask)
        )
        for to_tile in bbu.scan(
            (rank_mask | file_mask) & ROOK_ATTACKS[from_mask] & ~ally_mask
        ):
            self.legal_moves.add((from_mask, BB_TILES[to_tile]))

    def _update_legal_king_moves(self, from_mask, ally_mask):
        for to_tile in bbu.scan(KING_ATTACKS[from_mask] & ~ally_mask):
            self.legal_moves.add((from_mask, BB_TILES[to_tile]))

    def move(self, from_mask, to_mask):
        if (from_mask, to_mask) not in self.legal_moves:
            return
        piece = self.get_piece(from_mask)
        self._remove_piece(from_mask)
        if piece == PAWN and to_mask == self.en_passant_mask:
            self._remove_piece(to_mask >> 8 if self.turn else to_mask << 8)
        else:
            self._remove_piece(to_mask)
        if piece == PAWN and self.turn and to_mask == from_mask << 16:
            self.en_passant_mask = to_mask >> 8
        elif piece == PAWN and not self.turn and to_mask == from_mask >> 16:
            self.en_passant_mask = to_mask << 8
        else:
            self.en_passant_mask = 0

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
        if self.turn:
            self.white |= mask
        else:
            self.black |= mask

        if piece == PAWN:
            if mask & BB_RANK_8 or mask & BB_RANK_1:
                self.queen |= mask
            else:
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
