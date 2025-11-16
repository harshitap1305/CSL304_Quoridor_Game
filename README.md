# Quoridor AI Game

A Python implementation of the classic board game **Quoridor** with an intelligent AI opponent. This project features a graphical interface built with Pygame and implements minimax with alpha-beta pruning for optimal gameplay.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Game Rules](#game-rules)
- [AI Implementation](#ai-implementation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Command-Line Options](#command-line-options)
- [Technical Details](#technical-details)

## Overview

Quoridor is a strategy board game where two players compete to be the first to reach the opposite side of the board. Players can either move their pawn or place walls to block their opponent's path. This implementation provides:

- **Interactive GUI**: Beautiful graphical interface using Pygame
- **AI Opponent**: Intelligent computer player with adjustable difficulty levels
- **Optimization**: Advanced caching and memoization for performance
- **Real-time Visualization**: Visual feedback for valid moves, wall placement, and game state

## Features

- **Two-player gameplay**: Human vs AI
- **Adjustable AI difficulty**: Multiple difficulty levels (0 = Easy, higher = Harder)
- **Visual feedback**: Highlighted valid moves, wall preview on hover
- **Performance metrics**: Displays memoization statistics and cache hits
- **Persistent caching**: Optional disk-based caching for faster AI calculations
- **Debug mode**: Visualize AI distance calculations and thinking process
- **Sound effects**: Audio feedback for AI moves

## Requirements

- Python 3.6 or higher
- Pygame 1.9.6

## Installation

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd AI_Project
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install Pygame directly:
   ```bash
   pip install pygame==1.9.6
   ```

## Usage

### Basic Usage

Run the game with default settings: **Make sure to run this command from the root directory.**
```bash
python -m src.quoridor
```

### Command-Line Options

```bash
python -m src.quoridor [OPTIONS]
```

**Available Options:**

- `-l, --level LEVEL`: Set AI difficulty level (default: 0)
  - Level 0: Easy (greedy heuristic)
  - Level 1+: Harder (minimax with increasing depth)
  - Example: `python -m src.quoridor -l 2`

- `-d, --debug`: Enable debug mode
  - Shows distance calculations on the board
  - Displays detailed AI thinking process
  - Example: `python -m src.quoridor -d`

- `-C, --cache`: Enable persistent memoization cache
  - Speeds up AI calculations by caching game states
  - Creates a `__cache` directory for storage
  - Example: `python -m src.quoridor -C`

**Examples:**

```bash
# Play against easy AI
python -m src.quoridor

# Play against hard AI with caching enabled
python -m src.quoridor -l 3 -C

# Debug mode to see AI calculations
python -m src.quoridor -d -l 2
```

### Gameplay Controls

- **Move Pawn**: Click on a highlighted cell to move your pawn
- **Place Wall**: Hover over wall positions (between cells) and click to place
- **Exit**: Press `ESC` or close the window to quit

## Game Rules

### Objective
Be the first player to reach the opposite side of the board (your goal row).

### Setup
- **Board**: 9×9 grid of cells
- **Starting Positions**: 
  - Player 1 (Red): Bottom center
  - Player 2 (Blue): Top center
- **Walls**: Each player starts with 10 walls

### Moves
On your turn, you must choose **one** of the following:

1. **Move your pawn** to an adjacent cell (up, down, left, right)
   - Cannot move through walls
   - Can jump over opponent's pawn if adjacent
   - Can move diagonally if jumping over opponent

2. **Place a wall** to block paths
   - Walls are placed between cells (horizontally or vertically)
   - Cannot place a wall that completely blocks either player from reaching their goal
   - Each wall blocks two adjacent cells

### Winning
The first player to reach any cell in their goal row wins the game.

## AI Implementation

### Algorithm

The AI uses a **minimax algorithm with alpha-beta pruning** to determine optimal moves:

1. **Heuristic Function**: 
   - Calculates shortest path distance to goal for both players
   - Evaluates: `h = my_distance - opponent_distance`
   - Lower (more negative) values favor the AI

2. **Search Strategy**:
   - Explores game tree up to specified depth (level)
   - Uses alpha-beta pruning to eliminate suboptimal branches
   - Memoizes game states for faster lookups

3. **Distance Calculation**:
   - Uses BFS (Breadth-First Search) to compute shortest paths
   - Memoizes distance arrays for each game state
   - Updates dynamically as walls are placed

### Difficulty Levels

- **Level 0**: Greedy heuristic only (fast, easy)
- **Level 1+**: Minimax with increasing depth
  - Higher levels = deeper search = stronger play
  - Trade-off: More computation time

### Optimization Features

- **Memoization**: Caches AI decision nodes and distance calculations
- **Persistent Cache**: Optional disk-based caching across game sessions
- **State Compression**: Efficient game state representation for lookups
- **Incremental Updates**: Only recalculates distances when necessary

## Project Structure

```
Directory structure:
└── AI_Project/
    ├── README.md
    ├── requirements.txt       # Python dependencies
    ├── sound/
    │   └── chime.ogg
    └── src/
        ├── __init__.py
        ├── cache.py            # Persistent dictionary implementation
        ├── config.py           # Configuration constants and settings
        ├── core.py             # Core game logic and distance calculations
        ├── helpers.py          # Logging utilities
        ├── quoridor.py         # Main entry point
        ├── ai/                 # AI implementation
        │   ├── __init__.py
        │   ├── action.py       # Action classes (MovePawn, PlaceWall)
        │   └── ai.py           # Main AI class with minimax algorithm
        └── entities/           # Game entities
            ├── __init__.py
            ├── board.py        # Game board and state management
            ├── cell.py         # Individual cell representation
            ├── coord.py        # Coordinate system
            ├── drawable.py     # Base class for drawable objects
            ├── pawn.py         # Player pawn logic and movement
            └── wall.py         # Wall placement and collision
```

### Key Components

- **`src/quoridor.py`**: Main game loop, event handling, Pygame initialization
- **`src/core.py`**: Distance calculations, memoization, game state management
- **`src/ai/ai.py`**: Minimax algorithm, action evaluation, move selection
- **`src/entities/board.py`**: Board state, wall validation, player switching
- **`src/entities/pawn.py`**: Pawn movement, valid moves, goal checking

## Configuration

Configuration options are defined in `src/config.py`. Key settings include:

### Game Settings
- `DEF_ROWS`, `DEF_COLS`: Board dimensions (default: 9×9)
- `NUM_WALLS`: Starting walls per player (default: 10)
- `FRAMERATE`: Game frame rate (default: 25 FPS)

### Visual Settings
- `CELL_WIDTH`, `CELL_HEIGHT`: Cell size in pixels
- `CELL_PAD`: Padding between cells
- Color constants for board, pawns, walls, etc.

### AI Settings
- `LEVEL`: Default AI difficulty (default: 0)
- `INF`: Infinity value for distance calculations (default: 99)

### Cache Settings
- `CACHE_ENABLED`: Enable/disable caching (default: False)
- `CACHE_DIR`: Cache directory path (default: `./__cache`)

## Technical Details

### Game State Representation

The game state is encoded as a string:
- Current player index
- Pawn positions and remaining walls
- Wall positions on the board

This compact representation enables efficient memoization.

### Distance Calculation

Uses a **BFS-based shortest path algorithm**:
1. Initialize goal cells with distance 0
2. Propagate distances outward using valid moves
3. Memoize results for each game state
4. Update incrementally when walls change

### Performance Optimizations

1. **Memoization**: 
   - Caches AI decision nodes (`MEMOIZED_NODES`)
   - Caches distance arrays (`MEMOIZE_DISTANCES`)
   - Caches valid wall placements (`MEMOIZED_WALLS`)

2. **Alpha-Beta Pruning**:
   - Eliminates branches that won't affect final decision
   - Reduces search space exponentially

3. **State Cleanup**:
   - Removes unreachable memoized states
   - Prevents memory bloat during long games

4. **Persistent Cache**:
   - Saves cache to disk for reuse across sessions
   - Significantly speeds up repeated game states

### Statistics

At game end, the program displays:
- Total memoized nodes
- Cache hit count
- Memoized distances per player
- Distance cache hits per player

---

**Enjoy playing Quoridor!**
