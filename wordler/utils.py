"""Constants and helper functions used in this module"""

from wordler.__about__ import __title__

from enum import Enum
import logging
from typing import List, Union
from pkg_resources import resource_filename

ALPHABET = "abcdefghijklmnopqrstuvwxyz".upper()


def get_full_dicionary(word_length: int = 5) -> List[str]:
    """Retrive all the words of a certain lenth from the database"""
    filename = resource_filename(__title__, "assets/words.txt")
    with open(filename) as file:
        words = file.readlines()
    words = [word.rstrip().upper() for word in words]
    words = [word for word in words if len(word) == word_length and word.isalpha()]
    return words


def unique_letters(word: str) -> int:
    """Return the numver of unique letters in a given word."""
    return sum([letter.upper() in word.upper() for letter in ALPHABET])


class LetterResponse(Enum):
    """What can the letters of the guess be?"""

    GREEN = "green"
    ORANGE = "orange"
    GRAY = "gray"

    def __repr__(self):
        return self.name


def set_up_logging(log_level: Union[str, int] = logging.DEBUG) -> None:
    """Set up the handlers for logging rcf tests to stderr and journal
    :param log_level: Level at which to log to stderr
    """
    # the root logger is at debug b/c we want to catch everything
    root_logger = logging.getLogger()
    root_logger.setLevel("DEBUG")

    # the stderr handler can be configured
    log_format = "%(levelname)s - %(message)s"
    stderr_handler = logging.StreamHandler()
    stderr_formatter = logging.Formatter(fmt=log_format)
    stderr_handler.setFormatter(stderr_formatter)
    stderr_handler.setLevel(log_level)
    root_logger.addHandler(stderr_handler)
