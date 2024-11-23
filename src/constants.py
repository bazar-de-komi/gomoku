"""
This file contains the constants used in the project.
"""

SUCCESS = 0
ERROR = 84

# Commands
# Mandatory
CMD_START = "START"
CMD_TURN = "TURN"
CMD_BEGIN = "BEGIN"
CMD_END = "END"
CMD_ABOUT = "ABOUT"
CMD_BOARD = "BOARD"

# Optional
CMD_INFO = "INFO"
CMD_PLAY = "PLAY"
CMD_RESTART = "RESTART"
CMD_TAKEBACK = "TAKEBACK"
CMD_RECTSTART = "RECTSTART"
CMD_SWAP2BOARD = "SWAP2BOARD"

# Special case
CMD_INFO = "INFO"

COMMANDS = [
    CMD_START,
    CMD_TURN,
    CMD_BEGIN,
    CMD_END,
    CMD_INFO,
    CMD_PLAY,
    CMD_ABOUT,
    CMD_BOARD,
    CMD_RESTART,
    CMD_TAKEBACK,
    CMD_RECTSTART,
    CMD_SWAP2BOARD
]

CELL_EMPTY = 0
CELL_PLAYER = 1
CELL_ENEMY = 2

BOARD_EQUIVALENCE = {
    "1": CELL_PLAYER,
    "2": CELL_ENEMY,
    "": CELL_EMPTY
}

MAX_SIMULATIONS = 50

THREAD_NODE_KEY = "thread"
CLASS_NODE_KEY = "node"

DEBUG = False
