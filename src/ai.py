"""
The file contains the AI class that will be used to play the game.
"""

import random
from typing import List, Tuple
from . import constants as CONST

class AI:
    def __init__(self):
        random.seed()

    def _generate_possible_moves(self, board: List[List[int]], radius: int = 1) -> List[Tuple[int, int]]:
        """
        Generate possible moves in a limited area around the stones
        """
        moves = set()
        for y, col in enumerate(board):
            for x, cell in enumerate(col):
                if cell != CONST.CELL_EMPTY:
                    for dy in range(-radius, radius + 1):
                        for dx in range(-radius, radius + 1):
                            ny = y + dy
                            nx = x + dx
                            if 0 <= ny < len(board) and 0 <= nx < len(col) and board[ny][nx] == CONST.CELL_EMPTY:
                                moves.add((ny, nx))
        return list(moves)

    def _simulate_random_game(self, board: List[List[int]], current_player: int, depth_total: int = 4) -> int:
        """
        Simulate a random game with a limited depth
        """
        move_stack: List[Tuple[int, int]] = []
        depth: int = 0
        result: int = 0

        while depth < depth_total:
            if self._is_terminal(board, CONST.CELL_PLAYER):
                result = 1
                break
            if self._is_terminal(board, CONST.CELL_ENEMY):
                result = -1
                break
            moves: List[Tuple[int, int]] = self._generate_possible_moves(board)
            if not moves:
                result = 0
                break
            move: Tuple[int, int] = random.choice(moves)
            board[move[0]][move[1]] = current_player
            move_stack.append(move)
            if current_player == CONST.CELL_PLAYER:
                current_player = CONST.CELL_ENEMY
            else:
                current_player = CONST.CELL_PLAYER
            depth += 1
        for y, x in reversed(move_stack):
            board[y][x] = CONST.CELL_EMPTY
        if depth < depth_total:
            return result
        return 0

    def _check_line(self, sequence: List[int], player: int) -> bool:
        """
        Check a line with winning sequence
        """
        count: int = 0
        for cell in sequence:
            if cell == player:
                count += 1
                if count == 5:
                    return True
            else:
                count = 0
        return False

    def _check_horizontal(self, board: List[List[int]], player: int) -> bool:
        """
        Check the rows
        """
        for row in board:
            if self._check_line(row, player):
                return True
        return False

    def _check_vertical(self, board: List[List[int]], player: int) -> bool:
        """
        Check the columns
        """
        for col in range(len(board[0])):
            column = [board[row][col] for row in range(len(board))]
            if self._check_line(column, player):
                return True
        return False

    def _check_diagonal_to_down(self, board: List[List[int]], player: int) -> bool:
        """
        Check the diagonal to down
        """
        rows, cols = len(board), len(board[0])
        for start_row in range(rows - 4):
            for start_col in range(cols - 4):
                if all(board[start_row + i][start_col + i] == player for i in range(5)):
                    return True
        return False

    def _check_diagonal_to_up(self, board: List[List[int]], player: int) -> bool:
        """
        Check the diagonal to up
        """
        rows: int = len(board)
        cols: int = len(board[0])
        for start_row in range(4, rows):
            for start_col in range(cols - 4):
                if all(board[start_row - i][start_col + i] == player for i in range(5)):
                    return True
        return False

    def _is_terminal(self, board: List[List[int]], player: int) -> bool:
        """
        Define if a game can be finished by one of the two players
        """
        return (
            self._check_horizontal(board, player) or
            self._check_vertical(board, player) or
            self._check_diagonal_to_down(board, player) or
            self._check_diagonal_to_up(board, player)
        )

    def play_ai_turn(self, board: List[List[int]]) -> str:
        """
        Play the ia turn using Monte Carlo algorithm
        """
        possible_ai_moves: List[Tuple[int, int]] = self._generate_possible_moves(board)
        scores: List[int] = [0] * len(possible_ai_moves)
        simulations: List[int] = [0] * len(possible_ai_moves)
        result: int = 0
        ratio: float = -1.0
        best_index: int = 0
        best_ratio: float = -float('inf')

        if not possible_ai_moves:
            x = random.randint(0, len(board))
            y = random.randint(0, len(board[0]))
            return f"{x},{y}"
        for idx, move in enumerate(possible_ai_moves):
            for _ in range(CONST.MAX_SIMULATIONS):
                board[move[0]][move[1]] = CONST.CELL_PLAYER
                result = self._simulate_random_game(board, CONST.CELL_ENEMY)
                scores[idx] += result
                simulations[idx] += 1
                board[move[0]][move[1]] = CONST.CELL_EMPTY
        best_index = 0
        best_ratio = -float('inf')
        for idx, (score, sim_count) in enumerate(zip(scores, simulations)):
            if sim_count > 0:
                ratio = score / sim_count
            else:
                ratio = 0
            if ratio > best_ratio:
                best_ratio = ratio
                best_index = idx
        best_move = possible_ai_moves[best_index]
        return f"{best_move[1]},{best_move[0]}"
