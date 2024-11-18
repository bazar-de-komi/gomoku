"""
This is the main package of the project.
"""

from .ai import AI
from .parser import Parser
from . import constants as CONST

__all__ = ["AI", "Parser", "CONST"]
