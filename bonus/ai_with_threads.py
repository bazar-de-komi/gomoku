"""
The file contains the AI class that will be used to play the game.
"""

import random
from threading import Thread
from typing import List, Dict, Any, Tuple
from . import constants as CONST

class MapUpdater:
    def __init__(self):
        self.map: List[List[int]] = []
        self.writing: bool = False
    def write(self, y:int, x:int, data:int) -> None:
        """
            Function in charge of updating data in the map
        """
        while self.writing is True:
            pass
        if self.writing is False:
            self.writing = True
            self.map[y][x] = data
            self.writing = False
            

class AIThread:
    def __init__(self, current_map: MapUpdater):
        self.current_map: MapUpdater = current_map
        self.simulation_result: int = 0
        self.run_completed: bool = False
    
    def _generate_possible_moves(self, board: List[List[int]], radius: int = 2) -> List[Tuple[int, int]]:
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

    def simulate_random_game(self, board: List[List[int]], current_player: int, depth_total: int) -> int:
        """
        Simulate a random game with a limited depth
        """
        # move_stack: List[Tuple[int, int]] = []
        depth: int = 0
        local_result: int = 0

        while depth < depth_total:
            if self._is_terminal(board, CONST.CELL_PLAYER):
                local_result = 1
                break
            if self._is_terminal(board, CONST.CELL_ENEMY):
                local_result = -1
                break
            moves: List[Tuple[int, int]] = self._generate_possible_moves(board)
            if not moves:
                local_result = 0
                break
            move: Tuple[int, int] = random.choice(moves)
            board[move[0]][move[1]] = current_player
            # move_stack.append(move)
            if current_player == CONST.CELL_PLAYER:
                current_player = CONST.CELL_ENEMY
            else:
                current_player = CONST.CELL_PLAYER
            depth += 1
        # for y, x in reversed(move_stack):
        #     board[y][x] = CONST.CELL_EMPTY
        if depth < depth_total:
            self.simulation_result = local_result
            self.run_completed = True
            return local_result
        self.simulation_result = 0
        self.run_completed = True
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
        rows = len(board)
        cols = len(board[0])
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

class AI:
    def __init__(self):
        self.current_map: MapUpdater = MapUpdater()
        self.threads:List[Dict[str,Any]] = []

    def _generate_possible_moves(self, board: List[List[int]], radius: int = 2) -> List[Tuple[int, int]]:
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
    
    def _get_stone_number(self, board: List[List[int]]) -> int:
        """
        Get stone number on the board
        """
        count: int = 0;
        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] != CONST.CELL_EMPTY:
                    count += 1
        return count

    def play_ai_turn(self, board: List[List[int]]) -> str:
        """
        Play the ia turn using Monte Carlo algorithm
        """
        stone_nb = self._get_stone_number(board)
        total_depth: int = 0
        radius: int = 0
        if stone_nb >= 0 and stone_nb < 80:
            total_depth = 10
            radius = 2
        if stone_nb >= 80 and stone_nb < 160:
            total_depth = 6
            radius = 1
        if stone_nb >= 160 and stone_nb < 200:
            total_depth = 6
            radius = 2
        # radius = 2
        # total_depth = 10
        possible_ai_moves: List[Tuple[int, int]] = self._generate_possible_moves(board, radius)
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
        self.map.map = [col[:] for col in board]
        for idx, move in enumerate(possible_ai_moves):
            for _ in range(CONST.MAX_SIMULATIONS):
                self.map.write(y=move[0],x=move[1],data=CONST.CELL_PLAYER)
                node:AIThread = AIThread(self.map)
                self.threads.append({
                    CONST.CLASS_NODE_KEY: node,
                    CONST.THREAD_NODE_KEY: Thread(
                        target=node.simulate_random_game,
                        args=(CONST.CELL_ENEMY, total_depth)
                    ),
                    CONST.IDX_NODE_KEY:idx,
                    CONST.MOVE_NODE_KEY:list(move)
                })
                self.threads[-1][CONST.THREAD_NODE_KEY].start()
        while not self.threads:
            for index, item in enumerate(self.threads):
                if item[CONST.CLASS_NODE_KEY].run_completed is True:
                    result = item[CONST.CLASS_NODE_KEY].simulation_result
                    scores[item[CONST.IDX_NODE_KEY]] += result
                    simulations[item[CONST.IDX_NODE_KEY]] += 1
                    node1 = item[CONST.MOVE_NODE_KEY][0]
                    node2 = item[CONST.MOVE_NODE_KEY][1]
                    # board[node1][node2] = CONST.CELL_EMPTY
                    item[CONST.THREAD_NODE_KEY].join(timeout=2)
                    self.threads.pop(index)
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
