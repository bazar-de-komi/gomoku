"""_summary_
This module contains the parser for the command line arguments.
"""

import sys
from typing import List, Dict
from threading import Thread
from . import constants as CONST


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
            [0 for _ in range(self.board_size)]
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

    def __init__(self, game_board: List[List[int]] = SystemBoard):
        self.global_status = CONST.SUCCESS
        self.completed: bool = False
        self.game_board = game_board

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
            status = self.process_board_command(cmd_args)
            self.update_global_status(status)
            self.completed = True
            return status
        if command == CONST.CMD_RESTART:
            status = self.process_restart_command(cmd_args)
            self.update_global_status(status)
            self.completed = True
            return status
        self.update_global_status(CONST.ERROR)
        self.completed = True
        return status

    def process_start_command(self, cmd: List[str]) -> int:
        """
        Process the start command.

        Args:
            cmd (List[str]): _description_

        Returns:
            int: _description_
        """
        return CONST.SUCCESS

    def process_begin_command(self, cmd: List[str]) -> int:
        """
        Process the begin command.

        Args:
            cmd (List[str]): _description_

        Returns:
            int: _description_
        """
        return CONST.SUCCESS

    def process_turn_command(self, cmd: List[str]) -> int:
        """
        Process the turn command.

        Args:
            cmd (List[str]): _description_

        Returns:
            int: _description_
        """
        return CONST.SUCCESS

    def process_board_command(self, cmd: List[str]) -> int:
        """
        Process the board command.

        Args:
            cmd (List[str]): _description_

        Returns:
            int: _description_
        """
        return CONST.SUCCESS

    def process_restart_command(self, cmd: List[str]) -> int:
        """
        Process the restart command.

        Args:
            cmd (List[str]): _description_

        Returns:
            int: _description_
        """
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

    def perror(self, string: str) -> None:
        """
        Print an error message to the standard error output.
        """
        print(string, file=sys.stderr)

    def __call__(self) -> int:
        while self.continue_running:
            data = input()
            cmd_line = data.split(" ")
            cmd_bin = cmd_line[0].upper()
            if cmd_bin == CONST.CMD_END:
                self.continue_running = False
                for index, item in enumerate(self.threads):
                    item["thread"].join(timeout=self.thread_timeout)
                    self.threads.pop(index)
                continue
            if cmd_bin in CONST.COMMANDS:
                self.threads.append({
                    "node": ParserThread(self.game_board),
                    "thread": Thread(target=ParserThread.process_command, args=(cmd_line,))
                })
                self.threads[-1]["thread"].start()
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
            if item["node"].completed is True:
                item["thread"].join(timeout=self.thread_timeout)
                self.update_global_status(item["node"].global_status)
                self.threads.pop(index)

    def update_global_status(self, status: bool) -> None:
        """
        Update the status of the global variable.
        Args:
            status (bool): _description_
        """
        if status != CONST.SUCCESS:
            self.global_status = status
