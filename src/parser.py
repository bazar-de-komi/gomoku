"""_summary_
This module contains the parser for the command line arguments.
"""

import sys
from typing import List, Union, TextIO
from . import constants as CONST
from .ai import AI


def my_print(string: str, file: Union[TextIO, None] = None) -> None:
    """
        Print the string to the specified file.

    Args:
        string (str): The string to be displayed.
        file (Union[TextIO, None], optional): The stream to which to output the content. Defaults to None.
    """
    if file is None:
        print(string, flush=True, file=sys.stdout)
    else:
        print(string, flush=True, file=file)


def pdebug(string: str) -> None:
    """
    Print the debug message.
    """
    if CONST.DEBUG:
        my_print(string, sys.stderr)


class SystemBoard:
    """
    The class in charge of creating the board for the game.
    """

    def __init__(self):
        self.board: List[List[int]] = []
        self.board_size: int = 0

    def create_board(self, size: int = 0) -> None:
        """
        Create the board for the game.
        """
        self.board_size = size
        self.board = [
            [CONST.CELL_EMPTY for _ in range(self.board_size)]
            for _ in range(self.board_size)
        ]

    def clear_board(self) -> None:
        """
        Clear the board.
        """
        for coli, col in enumerate(self.board):
            for index in range(len(col)):
                self.board[coli][index] = CONST.CELL_EMPTY

    def recreate_board(self, size: Union[int, None] = None) -> None:
        """
            Recreate the board.
        """
        if size is not None:
            self.create_board(size)
        self.clear_board()


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
        command = cmd[0].upper()
        # cmd_args = cmd[1:]
        cmd_args = cmd
        pdebug(f"Command: {command}, board_mode = {self.board_mode}")
        if command == CONST.CMD_START:
            pdebug("Processing start command")
            status = self.process_start_command(cmd_args)
            self.update_global_status(status)
            self.completed = True
            return status
        if command == CONST.CMD_BEGIN:
            pdebug("Processing begin command")
            status = self.process_begin_command(cmd_args)
            self.update_global_status(status)
            self.completed = True
            return status
        if command == CONST.CMD_TURN:
            pdebug("Processing turn command")
            status = self.process_turn_command(cmd_args)
            self.update_global_status(status)
            self.completed = True
            return status
        if command == CONST.CMD_BOARD:
            pdebug("Processing board command")
            self.board_mode = True
            self.board_index = 0
            status = CONST.SUCCESS
            self.update_global_status(status)
            return status
        if command == CONST.CMD_RESTART:
            pdebug("Processing restart command")
            status = self.process_restart_command(cmd_args)
            self.update_global_status(status)
            self.completed = True
            return status
        self.completed = True
        return CONST.SUCCESS

    def process_ai_call(self) -> int:
        """
        Process the result returned by the ai.

        Returns:
            int: _description_
        """
        if self.ai is None:
            return CONST.SUCCESS
        response = self.ai.play_ai_turn(self.game_board.board)
        x, y = response.split(",")
        if not x.isdigit() and not y.isdigit():
            my_print(f"ERROR Invalid AI response: {response}")
            self.update_global_status(CONST.ERROR)
            return CONST.ERROR
        x = int(x)
        y = int(y)
        if x < 0 or x >= self.game_board.board_size:
            my_print(f"ERROR Invalid AI response: {x}")
            self.update_global_status(CONST.ERROR)
            return CONST.ERROR
        if y < 0 or y >= self.game_board.board_size:
            my_print(f"ERROR Invalid AI response: {y}")
            self.update_global_status(CONST.ERROR)
            return CONST.ERROR
        if self.game_board.board[x][y] != CONST.CELL_EMPTY:
            my_print(f"ERROR Invalid AI response: {response}")
            self.update_global_status(CONST.ERROR)
            return CONST.ERROR
        self.game_board.board[x][y] = CONST.CELL_PLAYER
        my_print(response)
        self.update_global_status(CONST.SUCCESS)
        return CONST.SUCCESS

    def print_success(self) -> None:
        """
        Print the success message.
        """
        my_print("OK")

    def process_start_command(self, cmd: List[str]) -> int:
        """
        Process the start command.

        Args:
            cmd (List[str]): _description_

        Returns:
            int: _description_
        """
        if len(cmd) != 2:
            my_print(f"ERROR Unsupported number of arguments: {len(cmd)}")
            return CONST.ERROR
        if not cmd[1].isdigit():
            my_print(f"ERROR Invalid board size: {cmd[1]}")
            return CONST.ERROR
        size = int(cmd[1])
        if size < 5:
            my_print(f"ERROR Invalid board size: {cmd[1]}")
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
            my_print(f"ERROR Unsupported number of arguments: {len(cmd)}")
            return CONST.ERROR
        return self.process_ai_call()

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
            my_print(f"ERROR Unsupported number of arguments: {len(cmd)}")
            return CONST.ERROR
        if cmd_length == 2:
            turn_params = cmd[1].split(",")
            if len(turn_params) != 2:
                my_print(f"ERROR Invalid turn parameters: {cmd[1]}")
                return CONST.ERROR
        else:
            turn_params = [cmd[1], cmd[2]]
        if not turn_params[0].isdigit() or not turn_params[1].isdigit():
            my_print(f"ERROR Invalid turn parameters: {cmd[1]}")
            return CONST.ERROR
        row = int(turn_params[0])
        col = int(turn_params[1])
        if row < 0 or row >= self.game_board.board_size:
            my_print(f"ERROR Invalid turn parameters: {row}")
            return CONST.ERROR
        if col < 0 or col >= self.game_board.board_size:
            my_print(f"ERROR Invalid turn parameters: {col}")
            return CONST.ERROR
        if self.game_board.board[row][col] != CONST.CELL_EMPTY:
            my_print(f"ERROR Invalid board cell: {row},{col}")
            return CONST.ERROR
        self.game_board.board[row][col] = CONST.CELL_ENEMY
        return self.process_ai_call()

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
        if self.game_board.board == [] or self.game_board.board is None:
            my_print("ERROR Board not created")
            return CONST.ERROR
        if cmd[0].upper() == "DONE":
            self.board_mode = False
            return self.process_ai_call()
        board_line = cmd[0].split(",")
        if len(board_line) != 3:
            my_print(f"ERROR Invalid board line: {cmd[0]}")
            return CONST.ERROR
        if not board_line[0].isdigit() or not board_line[1].isdigit():
            my_print(f"ERROR Invalid board line: {cmd[0]}")
            return CONST.ERROR
        row = int(board_line[0])
        col = int(board_line[1])
        value = CONST.BOARD_EQUIVALENCE.get(board_line[2])
        pdebug(
            f"Board line: {board_line}, value: {value}," +
            f" row: {row}, col: {col}"
        )
        if value is None:
            my_print(f"ERROR Invalid board value: {board_line[2]}")
            return CONST.ERROR
        if row < 0 or row >= self.game_board.board_size:
            my_print(f"ERROR Invalid board row: {row}")
            return CONST.ERROR
        if col < 0 or col >= self.game_board.board_size:
            my_print(f"ERROR Invalid board col: {col}")
            return CONST.ERROR
        if self.game_board.board[row] == []:
            my_print(f"ERROR Board row not created: {row}")
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
        if len(cmd) != 1:
            my_print(f"ERROR Invalid restart command: {cmd}")
            return CONST.ERROR
        self.game_board.recreate_board()
        self.print_success()
        return CONST.SUCCESS


class Parser:
    """
    This class is the parser for the command line arguments.
    """

    def __init__(self):
        self.thread_timeout: int = 2
        self.global_status = CONST.SUCCESS
        self.continue_running: bool = True
        self.board_mode: bool = False
        self.board: List[List[int]]
        self.game_board = SystemBoard()
        self.ai: AI = AI()

    def update_global_status(self, status: bool) -> None:
        """
        Update the status of the global variable.
        Args:
            status (bool): _description_
        """
        if status != CONST.SUCCESS:
            self.global_status = status

    def __call__(self, single_turn: bool = False) -> int:
        """_summary_
            The function in charge of processing the incoming commands.

        Returns:
            int: _description_
        """
        node = ParserThread(self.game_board, self.ai)
        while self.continue_running or single_turn:
            data = input()
            cmd_line = data.split(" ")
            cmd_bin = cmd_line[0].upper()
            if cmd_bin == CONST.CMD_END:
                self.continue_running = False
                self.update_global_status(CONST.SUCCESS)
                continue
            if self.board_mode is True:
                node.board_mode = True
                status = node.process_board_command(cmd_line)
                node.update_global_status(status)
                self.update_global_status(status)
                continue
            if cmd_bin in CONST.COMMANDS:
                node = ParserThread(self.game_board, self.ai)
                node.process_command(cmd_line)
                if node.board_mode is True:
                    self.board_mode = True
            else:
                my_print("UNKNOWN")
                self.update_global_status(CONST.ERROR)
            single_turn = False
        return self.global_status
