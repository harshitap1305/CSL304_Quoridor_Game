# -*- coding: utf-8 -*-

import os
from pygame import Color

from .entities.coord import Coord

__doc__ = """ Centralizes all global configuration flags """

# Debug FLAG
__DEBUG__ = False

# Frame rate
FRAMERATE = 25

# Config Options
GAME_TITLE = 'Quoridor'
DEFAULT_NUM_PLAYERS = 2

# Cell size
CELL_WIDTH = 50
CELL_HEIGHT = 50
CELL_PAD = 7
CELL_BORDER_SIZE = 2

# Default Number of rows and cols
DEF_ROWS = 9
DEF_COLS = 9

# Number of Walls per player
NUM_WALLS = 10

### COLORS ###
### REALISTIC QUORIDOR BOARD THEME ###

# Font
FONT_COLOR = Color(20, 20, 20)
FONT_BG_COLOR = Color(245, 245, 245)
FONT_SIZE = 16

# Board Background & Border
BOARD_BG_COLOR = Color(205, 170, 125)    # Light wood texture color
BOARD_BRD_COLOR = Color(130, 100, 70)    # Darker wood edges
BOARD_BRD_SIZE = 2

# Cells (Grid)
CELL_BORDER_COLOR = Color(110, 80, 55)   # Dark wood lines
CELL_COLOR = Color(225, 195, 150)        # Smooth wooden cell color
CELL_VALID_COLOR = Color(180, 150, 100)  # Slightly darker wood for valid tiles

# Walls (Very similar to real Quoridor walls)
WALL_COLOR = Color(110, 75, 45)          # Dark brown wooden block color

# Pawns (Just like real Quoridor sets)
PAWN_A_COL = Color(180, 30, 30)          # Classic red pawn
PAWN_B_COL = Color(40, 60, 160)          # Classic blue pawn
PAWN_BORDER_COL = Color(240, 220, 100)   # Slight gold/beige edge

# Gauges (small wood-tone bars)
GAUGE_WIDTH = CELL_WIDTH
GAUGE_HEIGHT = 6
GAUGE_COLOR = Color(160, 110, 60)        # Medium brown
GAUGE_BORDER_COLOR = Color(60, 40, 20)

# Padding
PAWN_PADDING = 25
                       # Balanced spacing



# Other constants
CELL_GLOW_COLOR = Color(0, 255, 255)
PAWN_SELECTED_COLOR = Color(255, 0, 255)  # Magenta glow
WALL_HIGHLIGHT_COLOR = Color(0, 255, 180)



class DIR:
    """ Directions
    """
    N = 0
    S = 1
    E = 2
    W = 3


DIRS = {DIR.N, DIR.S, DIR.E, DIR.W}  # Available directions
OPPOSITE_DIRS = [DIR.S, DIR.N, DIR.W, DIR.E]  # Reverse direction

# Delta to add to position to move into that direction
DIRS_DELTA = [Coord(-1, 0), Coord(+1, 0), Coord(0, -1), Coord(0, +1)]

# Network port
NETWORK_ENABLED = False  # Set to true to enable network playing
PORT = 8001  # This client port
BASE_PORT = 8000
SERVER_ADDR = 'localhost'
SERVER_URL = 'http://{}:{}'.format(SERVER_ADDR, PORT)

# Default AI playing level
LEVEL = 0

# Infinite
INF = 99

# Cache
CACHE_ENABLED = False
CACHE_DIR = './__cache'
CACHE_AI_FNAME = os.path.join(CACHE_DIR, 'ai.memo')
CACHE_DIST_FNAME = os.path.join(CACHE_DIR, 'dist.memo')
