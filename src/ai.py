"""
The file contains the AI class that will be used to play the game.
"""

import random
from typing import List
from . import CONST

class AI:
    def __init__(self):
        pass

    def _generate_possible_moves(self, board: List[List[int]]) -> List[tuple[int, int]]:
        possible_moves: List[tuple[int, int]] = []
        for y, col in enumerate(board):
            for x, cell in enumerate(col):
                if cell == CONST.CELL_EMPTY:
                    possible_moves.append((y, x))
        return possible_moves

    def _simulate_random_game(self, board: List[List[int]], current_player: int) -> int:
        while True:
            if self._is_terminal(board, CONST.CELL_PLAYER):
                return 1
            if self._is_terminal(board, CONST.CELL_ENEMY):
                return -1
            moves: List[tuple[int, int]] = self._generate_possible_moves(board)
            if not moves:
                return 0
            move: tuple[int, int] = random.choice(moves)
            board[move[0]][move[1]] = current_player
            if current_player == CONST.CELL_PLAYER:
                current_player = CONST.CELL_ENEMY
            else:
                current_player = CONST.CELL_PLAYER

    def _check_horizontal(self, board: List[List[int]], player: int) -> bool:
        for row in board:
            count: int = 0
            for cell in row:
                if cell == player:
                    count += 1
                    if count == 5:
                        return True
                else:
                    count = 0
        return False

    def _check_vertical(self, board: List[List[int]], player: int) -> bool:
        rows: int = len(board)
        cols: int = len(board[0])
        for col in range(cols):
            count: int = 0
            for row in range(rows):
                if board[row][col] == player:
                    count += 1
                    if count == 5:
                        return True
                else:
                    count = 0
        return False

    def _check_diagonal_to_down(self, board: List[List[int]], player: int) -> bool:
        rows: int = len(board)
        cols: int = len(board[0])
        for row in range(rows - 4):
            for col in range(cols - 4):
                if all(board[row + i][col + i] == player for i in range(5)):
                    return True
        return False

    def _check_diagonal_to_up(self, board: List[List[int]], player: int) -> bool:
        rows: int = len(board)
        cols: int = len(board[0])
        for row in range(4, rows):
            for col in range(cols - 4):
                if all(board[row - i][col + i] == player for i in range(5)):
                    return True
        return False

    def _is_board_full(self, board: List[List[int]]) -> bool:
        return all(cell != CONST.CELL_EMPTY for row in board for cell in row)

    def _is_terminal(self, board: List[List[int]], player: int) -> bool:
        if self._check_horizontal(board, player):
            return True
        if self._check_vertical(board, player):
            return True
        if self._check_diagonal_to_down(board, player):
            return True
        if self._check_diagonal_to_up(board, player):
            return True
        if self._is_board_full(board):
            return True
        return False

    def play_ai_turn(self, board: List[List[int]]) -> str:
        possible_ai_moves: List[tuple[int, int]] = self._generate_possible_moves(board)
        scores: List[int] = [0] * len(possible_ai_moves)
        simulations: List[int] = [0] * len(possible_ai_moves)

        for j, move in enumerate(possible_ai_moves):
            for _ in range(CONST.MAX_SIMULATIONS):
                board_copy: List[List[int]] = [row[:] for row in board]
                board_copy[move[0]][move[1]] = CONST.CELL_PLAYER
                result: int = self._simulate_random_game(board_copy, CONST.CELL_ENEMY)
                scores[j] += result
                simulations[j] += 1
        best_index: int = 0
        best_ratio: float = -float('inf')
        for i, (score, simulation) in enumerate(zip(scores, simulations)):
            if simulation > 0:
                ratio: float = score / simulation
            else:
                ratio = 0
            if ratio > best_ratio:
                best_ratio = ratio
                best_index = i
        best_move: tuple[int, int] = possible_ai_moves[best_index]
        return f"{best_move[1]},{best_move[0]}"
