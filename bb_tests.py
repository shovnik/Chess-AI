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

BB_BACKRANKS = BB_RANK_1 | BB_RANK_8
BB_CORNERS = BB_A1 | BB_H1 | BB_A8 | BB_H8
BB_CENTER = BB_D4 | BB_E4 | BB_D5 | BB_E5

BB_LIGHT_TILES = 0x55AA_55AA_55AA_55AA
BB_DARK_TILES = 0xAA55_AA55_AA55_AA55

knights = BB_H6
print(BB_H6)
print(BB_H8)

def knightAttacks(n):
   attacks = BB_EMPTY
   for shift in [-6, -10, -15, -17, 6, 10, 15, 17]:
       index = n + shift
       if 0 <= index < 64 and abs(n%8 - index%8) <= 2:
           attacks |= BB_TILES[index]
   return attacks

def kingAttacks(n):
   attacks = BB_EMPTY
   for shift in [-9, -8, -7, -1, 1, 7, 8, 9]:
       index = n + shift
       if 0 <= index < 64 and abs(n%8 - index%8) <= 2:
           attacks |= BB_TILES[index]
   return attacks

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

for i in range(64):
    print_bb(kingAttacks(i))
    print()
