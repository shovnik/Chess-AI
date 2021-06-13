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
] = [1 << i for i in range(64)]

BB_FILES = [
    BB_FILE_A, BB_FILE_B, BB_FILE_C, BB_FILE_D, BB_FILE_E, BB_FILE_F, BB_FILE_G, BB_FILE_H,
] = [0x0101_0101_0101_0101 << i for i in range(8)]

BB_RANKS = [
    BB_RANK_1,
    BB_RANK_2,
    BB_RANK_3,
    BB_RANK_4,
    BB_RANK_5,
    BB_RANK_6,
    BB_RANK_7,
    BB_RANK_8,
] = [0xff << (8 * i) for i in range(8)]
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


def print_bb(bb):
    board = "{:064b}".format(bb)
    for i in range(8):
        print(
            board[8 * i + 7]
            + " "
            + board[8 * i + 6]
            + " "
            + board[8 * i + 5]
            + " "
            + board[8 * i + 4]
            + " "
            + board[8 * i + 3]
            + " "
            + board[8 * i + 2]
            + " "
            + board[8 * i + 1]
            + " "
            + board[8 * i + 0]
        )
    print()


def reverse_horizontal(bb):
    # Source: https://www.chessprogramming.org/Flipping_Mirroring_and_Rotating#MirrorHorizontally
    bb = ((bb >> 1) & 0x5555_5555_5555_5555) | ((bb & 0x5555_5555_5555_5555) << 1)
    bb = ((bb >> 2) & 0x3333_3333_3333_3333) | ((bb & 0x3333_3333_3333_3333) << 2)
    bb = ((bb >> 4) & 0x0F0F_0F0F_0F0F_0F0F) | ((bb & 0x0F0F_0F0F_0F0F_0F0F) << 4)
    return bb


for diag in BB_ANTI_DIAGS:
    print_bb(diag)

# Pawn shift 1
# A & ~B
# Pawn shift 2
# A & ~B & ~(B << 8)