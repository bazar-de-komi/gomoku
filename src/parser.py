"""_summary_
This module contains the parser for the command line arguments.
"""

import sys
from typing import List, Dict
from threading import Thread
from . import constants as CONST
from .ai import AI


class SystemBoard:
    """
    The class in charge of creating the board for the game.
    """

    def __init__(self):
        self.board: List[List[int]] = []
        self.board_size: int = 0

    def create_board(self, size: int = 0) -> List[List[int]]:
        """
        Create the board for the game.
        """
        self.board_size = size
        self.board = [
            [CONST.CELL_EMPTY for _ in range(self.board_size)]
            for _ in range(self.board_size)
        ]


class ParserThread:
    """
        The class in charge of parsing the command line arguments while running in a thread.

    Args:
        Thread (_type_): _description_

    Returns:
        _type_: _description_
    """

    def __init__(self, game_board: SystemBoard, ai: AI):
        self.ai: AI = ai
        self.completed: bool = False
        self.global_status = CONST.SUCCESS
        self.game_board: SystemBoard = game_board
        self.board_mode: bool = False
        self.board_index: int = 0

    def update_global_status(self, status: bool) -> None:
        """
        Update the status of the global variable.
        Args:
            status (bool): _description_
        """
        if status != CONST.SUCCESS:
            self.global_status = status

    def process_command(self, cmd: List[str]) -> int:
        """
        Process the command given in the command line.
        Args:
            cmd (List[str]): _description_

        Returns:
            int: _description_
        """
        print(f"Received commands: cmd={cmd}")
        command = cmd[0].upper()
        cmd_args = cmd[1:]
        if command == CONST.CMD_START:
            status = self.process_start_command(cmd_args)
            self.update_global_status(status)
            self.completed = True
            return status
        if command == CONST.CMD_BEGIN:
            status = self.process_begin_command(cmd_args)
            self.update_global_status(status)
            self.completed = True
            return status
        if command == CONST.CMD_TURN:
            status = self.process_turn_command(cmd_args)
            self.update_global_status(status)
            self.completed = True
            return status
        if command == CONST.CMD_BOARD:
            self.board_mode = True
            self.board_index = 0
            self.update_global_status(CONST.SUCCESS)
            return CONST.SUCCESS
        if command == CONST.CMD_RESTART:
            status = self.process_restart_command(cmd_args)
            self.update_global_status(status)
            self.completed = True
            return status
        self.update_global_status(CONST.ERROR)
        self.completed = True
        return status

    def print_success(self) -> None:
        """
        Print the success message.
        """
        print("OK")

    def process_start_command(self, cmd: List[str]) -> int:
        """
        Process the start command.

        Args:
            cmd (List[str]): _description_

        Returns:
            int: _description_
        """
        if len(cmd) != 2:
            print(f"ERROR Unsupported number of arguments: {len(cmd)}")
            return CONST.ERROR
        if not cmd[1].isdigit():
            print(f"ERROR Invalid board size: {cmd[1]}")
            return CONST.ERROR
        size = int(cmd[1])
        if size < 5:
            print(f"ERROR Invalid board size: {cmd[1]}")
            return CONST.ERROR
        self.game_board.create_board(size)
        self.print_success()
        return CONST.SUCCESS

    def process_begin_command(self, cmd: List[str]) -> int:
        """
        Process the begin command.

        Args:
            cmd (List[str]): _description_

        Returns:
            int: _description_
        """
        if len(cmd) != 1:
            print(f"ERROR Unsupported number of arguments: {len(cmd)}")
            return CONST.ERROR
        print(self.ai.play_ai_turn(self.game_board.board))
        return CONST.SUCCESS

    def process_turn_command(self, cmd: List[str]) -> int:
        """
        Process the turn command.

        Args:
            cmd (List[str]): _description_

        Returns:
            int: _description_
        """
        cmd_length = len(cmd)
        if cmd_length not in (2, 3):
            print(f"ERROR Unsupported number of arguments: {len(cmd)}")
            return CONST.ERROR
        if cmd_length == 2:
            turn_params = cmd[1].split(",")
            if len(turn_params) != 2:
                print(f"ERROR Invalid turn parameters: {cmd[1]}")
                return CONST.ERROR
        else:
            turn_params = [cmd[1], cmd[2]]
        if not turn_params[0].isdigit() or not turn_params[1].isdigit():
            print(f"ERROR Invalid turn parameters: {cmd[1]}")
            return CONST.ERROR
        row = int(turn_params[0])
        col = int(turn_params[1])
        if row < 0 or row >= self.game_board.board_size:
            print(f"ERROR Invalid turn parameters: {row}")
            return CONST.ERROR
        if col < 0 or col >= self.game_board.board_size:
            print(f"ERROR Invalid turn parameters: {col}")
            return CONST.ERROR
        print(self.ai.play_ai_turn(self.game_board.board, row, col))
        return CONST.SUCCESS

    def process_board_command(self, cmd: List[str]) -> int:
        """
        Process the board command.

        Args:
            cmd (List[str]): _description_

        Returns:
            int: _description_
        """
        if cmd[0] == "":
            return CONST.SUCCESS
        if cmd[0].upper() == "DONE":
            self.board_mode = False
            print(f"{self.game_board.board_size},{self.game_board.board_size}")
            self.update_global_status(CONST.SUCCESS)
            return CONST.SUCCESS
        board_line = cmd[0].split(",")
        if len(board_line) != 3:
            print(f"ERROR Invalid board line: {cmd[0]}")
            return CONST.ERROR
        if not board_line[0].isdigit() or not board_line[1].isdigit():
            print(f"ERROR Invalid board line: {cmd[0]}")
            return CONST.ERROR
        row = int(board_line[0])
        col = int(board_line[1])
        value = CONST.BOARD_EQUIVALENCE.get(board_line[2])
        if value is None:
            print(f"ERROR Invalid board value: {board_line[2]}")
            return CONST.ERROR
        if row < 0 or row >= self.game_board.board_size:
            print(f"ERROR Invalid board row: {row}")
            return CONST.ERROR
        if col < 0 or col >= self.game_board.board_size:
            print(f"ERROR Invalid board col: {col}")
            return CONST.ERROR
        self.game_board.board[row][col] = value
        return CONST.SUCCESS

    def process_restart_command(self, cmd: List[str]) -> int:
        """
        Process the restart command.

        Args:
            cmd (List[str]): _description_

        Returns:
            int: _description_
        """
        if cmd[0] == "":
            pass
        return CONST.SUCCESS


class Parser:
    """
    This class is the parser for the command line arguments.
    """

    def __init__(self):
        self.thread_timeout: int = 2
        self.global_status = CONST.SUCCESS
        self.continue_running: bool = True
        self.board: List[List[int]]
        self.threads: List[Dict[Thread]] = []
        self.game_board = SystemBoard()
        self.ai: AI = AI()

    def perror(self, string: str) -> None:
        """
        Print an error message to the standard error output.
        """
        print(string, file=sys.stderr)

    def __call__(self) -> int:
        """_summary_
            The function in charge of processing the incoming commands.

        Returns:
            int: _description_
        """
        while self.continue_running:
            data = input()
            cmd_line = data.split(" ")
            cmd_bin = cmd_line[0].upper()
            if cmd_bin == CONST.CMD_END:
                self.continue_running = False
                for index, item in enumerate(self.threads):
                    item[CONST.THREAD_NODE_KEY].join(
                        timeout=self.thread_timeout
                    )
                    self.threads.pop(index)
                continue
            if cmd_bin in CONST.COMMANDS:
                if self.threads[-1][CONST.CLASS_NODE_KEY].board_mode is True:
                    status = self.threads[-1][CONST.CLASS_NODE_KEY].process_board_command(
                        cmd_line
                    )
                    self.threads[-1][CONST.CLASS_NODE_KEY].update_global_status(
                        status
                    )
                    self.update_global_status(status)
                self.threads.append(
                    {
                        CONST.CLASS_NODE_KEY: ParserThread(self.game_board, self.ai),
                        CONST.THREAD_NODE_KEY: Thread(
                            target=ParserThread.process_command,
                            args=(cmd_line,)
                        )
                    }
                )
                self.threads[-1][CONST.THREAD_NODE_KEY].start()
            else:
                self.perror(f"Unknown command: {cmd_bin}")
                self.update_global_status(CONST.ERROR)
            self.clean_threads()
        return self.global_status

    def clean_threads(self) -> None:
        """
        Clean the threads that have finished.
        """
        for index, item in enumerate(self.threads):
            if item[CONST.CLASS_NODE_KEY].completed is True:
                item[CONST.THREAD_NODE_KEY].join(timeout=self.thread_timeout)
                self.update_global_status(
                    item[CONST.CLASS_NODE_KEY].global_status
                )
                self.threads.pop(index)

    def update_global_status(self, status: bool) -> None:
        """
        Update the status of the global variable.
        Args:
            status (bool): _description_
        """
        if status != CONST.SUCCESS:
            self.global_status = status
