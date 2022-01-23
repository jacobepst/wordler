"""class that chooses a words and returns the guesses with coloring, functionally equivalent to the wordle website"""

from wordler.utils import get_full_dicionary, LetterResponse

from logging import getLogger
from random import choice
from typing import List


class WordleGame:
    """Game runner"""

    def __init__(self, display: bool = True, true_word=None):
        """"""
        if true_word is None:
            self.true_word = choice(get_full_dicionary()).upper()
        else:
            self.true_word = true_word

        self.display = display
        self.orange_letters = ""
        self.total_guesses = 0
        self.complete = False

    def guess(self, guess: str) -> List[LetterResponse]:
        """Given a guess return a game response"""
        self.orange_letters = ""  # reset this list each guess
        self.total_guesses += 1
        guess = guess.upper()
        response = [self.process_letter(letter, true_letter) for letter, true_letter in zip(guess, self.true_word)]
        if self.display:
            logger = getLogger(__name__)
            logger.info("\t".join([letter for letter in guess]))
            logger.info("\t".join([color.name for color in response]))

        if all(color == LetterResponse.GREEN for color in response):
            self.complete = True

        return response

    def process_letter(self, letter, true_letter):
        if letter == true_letter:
            self.orange_letters += letter
            return LetterResponse.GREEN
        if letter in self.true_word:
            # there is extra logic here to make sure the word isn't repeated
            self.orange_letters += letter
            if self.orange_letters.count(letter) <= self.true_word.count(letter):
                return LetterResponse.ORANGE

        return LetterResponse.GRAY
