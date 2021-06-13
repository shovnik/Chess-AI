def scan(bb):
    while bb:
        remainder = bb & -bb
        yield remainder.bit_length() - 1
        bb ^= remainder

def flip_ranks(bb):
    # Source: https://www.chessprogramming.org/Flipping_Mirroring_and_Rotating#MirrorHorizontally
    bb = ((bb >> 1) & 0x5555_5555_5555_5555) | ((bb & 0x5555_5555_5555_5555) << 1)
    bb = ((bb >> 2) & 0x3333_3333_3333_3333) | ((bb & 0x3333_3333_3333_3333) << 2)
    bb = ((bb >> 4) & 0x0f0f_0f0f_0f0f_0f0f) | ((bb & 0x0f0f_0f0f_0f0f_0f0f) << 4)
    return bb

def flip_files(bb):
    # Source: https://www.chessprogramming.org/Flipping_Mirroring_and_Rotating#FlipVertically
    bb = ((bb >> 8) & 0x00ff_00ff_00ff_00ff) | ((bb & 0x00ff_00ff_00ff_00ff) << 8)
    bb = ((bb >> 16) & 0x0000_ffff_0000_ffff) | ((bb & 0x0000_ffff_0000_ffff) << 16)
    bb = (bb >> 32) | ((bb & 0x0000_0000_ffff_ffff) << 32)
    return bb

def flip_diags(bb):
    # Source: https://www.chessprogramming.org/Flipping_Mirroring_and_Rotating#FlipabouttheDiagonal
    temp = (bb ^ (bb << 28)) & 0x0f0f_0f0f_0000_0000
    bb = bb ^ (temp ^ (temp >> 28))
    temp = (bb ^ (bb << 14)) & 0x3333_0000_3333_0000
    bb = bb ^ (temp ^ (temp >> 14))
    temp = (bb ^ (bb << 7)) & 0x5500_5500_5500_5500
    bb = bb ^ (temp ^ (temp >> 7))
    return bb

def flip_anti_diags(bb):
    # Source: https://www.chessprogramming.org/Flipping_Mirroring_and_Rotating#FlipabouttheAntidiagonal
    bb = bb ^ (((bb ^ (bb << 36)) ^ (bb >> 36)) & 0xf0f0_f0f0_0f0f_0f0f)
    temp = (bb ^ (bb << 18)) & 0xcccc_0000_cccc_0000
    bb = bb ^ (temp ^ (temp >> 18))
    temp = (bb ^ (bb << 9)) & 0xaa00_aa00_aa00_aa00
    bb = bb ^ (temp ^ (temp >> 9))
    return bb

# For debugging
def visualize(bb):
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
