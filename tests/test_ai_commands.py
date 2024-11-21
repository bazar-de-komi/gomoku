"""
    File in charge of testing the function responses to given commands.
"""

import os
import sys
import unittest.mock
from typing import List
from io import StringIO
from pytest import CaptureFixture

sys.path.append(os.getcwd())
sys.path.append(os.path.join("..", os.getcwd()))
try:
    from src.parser import Parser, my_print, ParserThread
    from src import constants as CONST
except ImportError as e:
    raise ImportError("The module is not found") from e

SINGLE_TURN = True

PI: Parser = Parser()
PI.ai = None
PI.continue_running = False

PIT: ParserThread = ParserThread(PI.game_board, PI.ai)

CMD = CONST.COMMANDS


def override_outputs():
    """
    Override the output of the function.
    """
    captured_output = StringIO()
    captured_error = StringIO()
    sys.stdout = captured_output
    sys.stderr = captured_error
    return [captured_output, captured_error]


def get_outputs(captured_output: StringIO, captured_error: StringIO) -> List[str]:
    """
    Get the outputs of the function.
    """
    return [captured_output.getvalue(), captured_error.getvalue()]


def reset_redirects():
    """
    Reset the output of the function.
    """
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


def test_my_print():
    """
    Test the process_command function with a BEGIN command.
    """
    test_string = "test"
    output, output_err = override_outputs()
    my_print(test_string)
    stream, stream_err = get_outputs(output, output_err)
    reset_redirects()
    assert stream == f"{test_string}\n"
    assert stream_err == ""


@unittest.mock.patch('builtins.input', side_effect=[f"{CONST.CMD_START} 20"])
def test_process_command_start(mock_input):
    """
    Test the process_command function with a START command.
    """
    output, output_err = override_outputs()
    status = PI(single_turn=SINGLE_TURN)
    stream, stream_err = get_outputs(output, output_err)
    reset_redirects()
    assert status == CONST.SUCCESS
    assert stream == "OK\n"
    assert stream_err == ""


@unittest.mock.patch('builtins.input', side_effect=[f"{CONST.CMD_TURN} 0 0"])
def test_process_command_turn(mock_input):
    """
    Test the process_command function with a TURN command.
    """
    output, output_err = override_outputs()
    PI.game_board.create_board(20)
    status = PI(single_turn=SINGLE_TURN)
    stream, stream_err = get_outputs(output, output_err)
    reset_redirects()
    assert status == CONST.SUCCESS
    assert stream == ""
    assert stream_err == ""


@unittest.mock.patch('builtins.input', side_effect=[CONST.CMD_BEGIN])
def test_process_command_begin(mock_input):
    """
    Test the process_command function with a BEGIN command.
    """
    output, output_err = override_outputs()
    status = PI(single_turn=SINGLE_TURN)
    stream, stream_err = get_outputs(output, output_err)
    reset_redirects()
    assert status == CONST.SUCCESS
    assert stream == ""
    assert stream_err == ""


def test_process_command_board(capsys: CaptureFixture):
    """
    Test the process_command function with a BOARD command.
    """
    status = PIT.process_command([CONST.CMD_BOARD])
    board_mode_status = PIT.board_mode
    PIT.board_mode = False
    stream = capsys.readouterr()
    assert status == CONST.SUCCESS
    assert board_mode_status is True
    assert stream.out == ""
    assert stream.err == ""


@unittest.mock.patch('builtins.input', side_effect=[CONST.CMD_INFO])
def test_process_command_info(mock_input):
    """
    Test the process_command function with a INFO command.
    """
    output, output_err = override_outputs()
    status = PI(single_turn=SINGLE_TURN)
    stream, stream_err = get_outputs(output, output_err)
    reset_redirects()
    assert status == CONST.SUCCESS
    assert stream == ""
    assert stream_err == ""


@unittest.mock.patch('builtins.input', side_effect=[CONST.CMD_END])
def test_process_command_end(mock_input):
    """
    Test the process_command function with a END command.
    """
    PI.global_status = CONST.SUCCESS
    output, output_err = override_outputs()
    status = PI()
    stream, stream_err = get_outputs(output, output_err)
    reset_redirects()
    assert status == CONST.SUCCESS
    assert stream == ""
    assert stream_err == ""
