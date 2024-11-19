"""
This file contains the constants used in the project.
"""

SUCCESS = 0
ERROR = 84

# Commands
CMD_END = "END"
CMD_START = "START"
CMD_BEGIN = "BEGIN"
CMD_TURN = "TURN"
CMD_BOARD = "BOARD"
CMD_RESTART = "RESTART"

COMMANDS = [
    CMD_END,
    CMD_START,
    CMD_BEGIN,
    CMD_TURN,
    CMD_BOARD,
    CMD_RESTART
]

CELL_EMPTY = 0
CELL_PLAYER = 1
CELL_ENEMY = 2

BOARD_EQUIVALENCE = {
    "1": CELL_PLAYER,
    "2": CELL_ENEMY,
    "": CELL_EMPTY
}

MAX_SIMULATIONS = 1000
