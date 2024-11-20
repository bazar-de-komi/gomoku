"""
The file contains the AI class that will be used to play the game
"""

import random
import time
from typing import List, Tuple
from . import constants as CONST

class AI:
    """
    The class that contains the ai for the gomoku game
    """
    def __init__(self):
        pass

    def _generate_possible_moves(self, board: List[List[int]], radius: int = 2) -> List[Tuple[int, int]]:
        """
        Generate possible moves in a limited area around the stones
        """
        moves = set()
        cols = len(board)
        rows = len(board[0])

        for y in range(cols):
            for x in range(rows):
                if board[y][x] != CONST.CELL_EMPTY:
                    for dy in range(-radius, radius + 1):
                        for dx in range(-radius, radius + 1):
                            ny = y + dy
                            nx = x + dx
                            if 0 <= ny < cols and 0 <= nx < rows and board[ny][nx] == CONST.CELL_EMPTY:
                                moves.add((ny, nx))
        return list(moves)

    def _check_all_alignments(self, board: List[List[int]], player: int) -> bool:
        """
        Check all alignments
        """
        rows: int = len(board[0])
        cols: int = len(board)
        vertical: List[Tuple[int, int]] = []
        horizontal: List[Tuple[int, int]] = []
        diag_down: List[Tuple[int, int]] = []
        diag_up: List[Tuple[int, int]] = []

        for y in range(cols):
            for x in range(rows):
                if len(horizontal) == 0 or (y == horizontal[-1][0] and x == horizontal[-1][1] + 1 and board[y][x] == player):
                    horizontal.append((y, x))
                    if len(horizontal) == 5:
                        return True
                elif len(horizontal) != 0 and y == horizontal[-1][0] and x == horizontal[-1][1] + 1 and board[y][x] != player:
                    horizontal.clear()
                if len(vertical) == 0 or (y == vertical[-1][0] + 1 and x == vertical[-1][1] and board[y][x] == player):
                    vertical.append((y, x))
                    if len(vertical) == 5:
                        return True
                elif len(vertical) != 0 and y == vertical[-1][0] + 1 and x == vertical[-1][1] and board[y][x] != player:
                    vertical.clear()
                if len(diag_down) == 0 or (y == diag_down[-1][0] + 1 and x == diag_down[-1][1] + 1 and board[y][x] == player):
                    diag_down.append((y, x))
                    if len(diag_down) == 5:
                        return True
                elif len(diag_down) != 0 and y == diag_down[-1][0] + 1 and x == diag_down[-1][1] + 1 and board[y][x] != player:
                    diag_down.clear()
                if len(diag_up) == 0 or (y == diag_up[-1][0] - 1 and x == diag_up[-1][1] + 1 and board[y][x] == player):
                    diag_up.append((y, x))
                    if len(diag_up) == 5:
                        return True
                elif len(diag_up) != 0 and y == diag_up[-1][0] - 1 and x == diag_up[-1][1] + 1 and board[y][x] != player:
                    diag_up.clear()
        return False

    def _simulate_random_game(self, board: List[List[int]], current_player: int, depth_total: int) -> int:
        """
        Simulate a random game with a limited depth
        """
        move_stack: List[Tuple[int, int]] = []
        moves: List[Tuple[int, int]] = self._generate_possible_moves(board, 2)
        depth: int = 0
        result: int = 0

        while depth < depth_total:
            if move_stack and self._check_all_alignments(board, current_player):
                if current_player == CONST.CELL_PLAYER :
                    result = 1
                else:
                    result = -1
                break
            if not moves:
                result = 0
                break
            move: Tuple[int, int] = random.choice(moves)
            board[move[0]][move[1]] = current_player
            move_stack.append(move)
            moves.remove(move)
            current_player = 3 - current_player
            depth += 1
        for y, x in reversed(move_stack):
            board[y][x] = CONST.CELL_EMPTY
        if depth < depth_total:
            return result
        return 0

    def play_ai_turn(self, board: List[List[int]]) -> str:
        """
        Play the ia turn using Monte Carlo algorithm
        """
        start_time = time.time()
        total_depth: int = 7
        radius: int = 2
        possible_ai_moves: List[Tuple[int, int]] = self._generate_possible_moves(board, radius)
        scores: List[int] = [0] * len(possible_ai_moves)
        simulations: List[int] = [0] * len(possible_ai_moves)
        result: int = 0
        ratio: float = -1.0
        best_index: int = 0
        best_ratio: float = -float('inf')

        if not possible_ai_moves:
            x: int = random.randint(0, len(board[0]))
            y: int = random.randint(0, len(board))
            return f"{x},{y}"
        for idx, move in enumerate(possible_ai_moves):
            if (time.time() - start_time) >= 4.8:
                break
            for _ in range(CONST.MAX_SIMULATIONS):
                if (time.time() - start_time) >= 4.8:
                    break
                board[move[0]][move[1]] = CONST.CELL_PLAYER
                result = self._simulate_random_game(board, CONST.CELL_ENEMY, total_depth)
                scores[idx] += result
                simulations[idx] += 1
                board[move[0]][move[1]] = CONST.CELL_EMPTY
            if simulations[idx] > 0:
                ratio = scores[idx] / simulations[idx]
            else:
                ratio = 0
            if ratio > best_ratio:
                best_ratio = ratio
                best_index = idx
        best_move = possible_ai_moves[best_index]
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Temps d'exécution: {execution_time} secondes")
        return f"{best_move[1]},{best_move[0]}"
