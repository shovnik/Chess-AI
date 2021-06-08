def scan(bb):
    while bb:
        remainder = bb & -bb
        yield remainder.bit_length() - 1
        bb ^= remainder

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
