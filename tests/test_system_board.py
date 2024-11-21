"""
    File in charge of testing the class that manages the game board.
"""

import os
import sys
from random import randint

sys.path.append(os.getcwd())
sys.path.append(os.path.join("..", os.getcwd()))
try:
    from src.parser import SystemBoard
    from src import constants as CONST
except ImportError as e:
    raise ImportError("The module is not found") from e

SBI: SystemBoard = SystemBoard()


def test_create_board_size_3():
    """
    Test the create_board function.
    """
    size = 3
    SBI.board = []
    SBI.board_size = 0
    SBI.create_board(size)
    assert SBI.board_size == size
    assert SBI.board == [
        [CONST.CELL_EMPTY for _ in range(size)] for _ in range(size)
    ]


def test_create_board_size_20():
    """
    Test the create_board function.
    """
    size = 20
    SBI.board = []
    SBI.board_size = 0
    SBI.create_board(size)
    assert SBI.board_size == size
    assert SBI.board == [
        [CONST.CELL_EMPTY for _ in range(size)] for _ in range(size)
    ]


def test_create_board_size_40():
    """
    Test the create_board function.
    """
    size = 40
    SBI.board = []
    SBI.board_size = 0
    SBI.create_board(size)
    assert SBI.board_size == size
    assert SBI.board == [
        [CONST.CELL_EMPTY for _ in range(size)] for _ in range(size)
    ]


def test_create_board_size_60():
    """
    Test the create_board function.
    """
    size = 60
    SBI.board = []
    SBI.board_size = 0
    SBI.create_board(size)
    assert SBI.board_size == size
    assert SBI.board == [
        [CONST.CELL_EMPTY for _ in range(size)] for _ in range(size)
    ]


def test_clear_board():
    """
    Test the clear_board function.
    """
    size = 40
    characters = [CONST.CELL_ENEMY, CONST.CELL_EMPTY, CONST.CELL_PLAYER]
    character_length = len(characters) - 1
    SBI.board_size = size
    SBI.board = [
        [
            characters[randint(0, character_length)] for _ in range(size)
        ] for _ in range(size)
    ]
    SBI.clear_board()
    for coli, col in enumerate(SBI.board):
        for index in range(len(col)):
            assert SBI.board[coli][index] == CONST.CELL_EMPTY


def test_recreate_board_size_3_not_none():
    """
    Test the create_board function.
    """
    size = 3
    SBI.board = []
    SBI.board_size = 0
    SBI.recreate_board(size)
    assert SBI.board_size == size
    assert SBI.board == [
        [CONST.CELL_EMPTY for _ in range(size)] for _ in range(size)
    ]


def test_recreate_board_size_20_not_none():
    """
    Test the create_board function.
    """
    size = 20
    SBI.board = []
    SBI.board_size = 0
    SBI.recreate_board(size)
    assert SBI.board_size == size
    assert SBI.board == [
        [CONST.CELL_EMPTY for _ in range(size)] for _ in range(size)
    ]


def test_recreate_board_size_40_not_none():
    """
    Test the create_board function.
    """
    size = 40
    SBI.board = []
    SBI.board_size = 0
    SBI.recreate_board(size)
    assert SBI.board_size == size
    assert SBI.board == [
        [CONST.CELL_EMPTY for _ in range(size)] for _ in range(size)
    ]


def test_recreate_board_size_60_not_none():
    """
    Test the create_board function.
    """
    size = 60
    SBI.board = []
    SBI.board_size = 0
    SBI.recreate_board(size)
    assert SBI.board_size == size
    assert SBI.board == [
        [CONST.CELL_EMPTY for _ in range(size)] for _ in range(size)
    ]


def test_recreate_board_size_3_none():
    """
    Test the create_board function.
    """
    size = 3
    SBI.board = [
        [CONST.CELL_PLAYER for _ in range(size)] for _ in range(size)
    ]
    SBI.board_size = size
    SBI.recreate_board()
    assert SBI.board_size == size
    assert SBI.board == [
        [CONST.CELL_EMPTY for _ in range(size)] for _ in range(size)
    ]


def test_recreate_board_size_20_none():
    """
    Test the create_board function.
    """
    size = 20
    SBI.board = [
        [CONST.CELL_PLAYER for _ in range(size)] for _ in range(size)
    ]
    SBI.board_size = size
    SBI.recreate_board()
    assert SBI.board_size == size
    assert SBI.board == [
        [CONST.CELL_EMPTY for _ in range(size)] for _ in range(size)
    ]


def test_recreate_board_size_40_none():
    """
    Test the create_board function.
    """
    size = 40
    SBI.board = [
        [CONST.CELL_PLAYER for _ in range(size)] for _ in range(size)
    ]
    SBI.board_size = size
    SBI.recreate_board()
    assert SBI.board_size == size
    assert SBI.board == [
        [CONST.CELL_EMPTY for _ in range(size)] for _ in range(size)
    ]


def test_recreate_board_size_60_none():
    """
    Test the create_board function.
    """
    size = 60
    SBI.board = [
        [CONST.CELL_PLAYER for _ in range(size)] for _ in range(size)
    ]
    SBI.board_size = size
    SBI.recreate_board()
    assert SBI.board_size == size
    assert SBI.board == [
        [CONST.CELL_EMPTY for _ in range(size)] for _ in range(size)
    ]
