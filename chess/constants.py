# Settings
FPS = 60

# Dimensions
WIDTH, HEIGHT = 1000, 1000
OFFSET = (100, 100)
ROWS, COLS = 8, 8
TILES = 64
TILE_SIZE = 100

# Palette
DARK = (168, 124, 96)
LIGHT = (247, 215, 195)
BLACK = (0, 0, 0)
RED = (255, 0, 0, 50)


# Pieces (numbers chosen to allow unique (piece | colour))
WHITE = True
BLACK = False
PAWN = 2
KNIGHT = 4
BISHOP = 6
ROOK = 8
QUEEN = 10
KING = 12

# Sprite paths
SPRITES = {
    PAWN | WHITE: "chess/sprites/white_pawn.png",
    KNIGHT | WHITE: "chess/sprites/white_knight.png",
    BISHOP | WHITE: "chess/sprites/white_bishop.png",
    ROOK | WHITE: "chess/sprites/white_rook.png",
    QUEEN | WHITE: "chess/sprites/white_queen.png",
    KING | WHITE: "chess/sprites/white_king.png",
    PAWN | BLACK: "chess/sprites/black_pawn.png",
    KNIGHT | BLACK: "chess/sprites/black_knight.png",
    BISHOP | BLACK: "chess/sprites/black_bishop.png",
    ROOK | BLACK: "chess/sprites/black_rook.png",
    QUEEN | BLACK: "chess/sprites/black_queen.png",
    KING | BLACK: "chess/sprites/black_king.png",
}