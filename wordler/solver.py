"""The solver class

Strategies can be added by defining a new function and passing that function name in when instantiating.
"""

from wordler.utils import get_full_dicionary, ALPHABET, unique_letters, LetterResponse

from random import choice
from typing import List, Tuple, Optional


class Solver:
    """Given repsonses to gueses make a new guess

    :param strategy: which strategy to use
    """

    def __init__(self, strategy: Optional[str] = None):
        self.strategy = strategy
        self.current_guess: Optional[str] = None
        self.green = ["*"] * 5
        self.all_words = get_full_dicionary()
        self.reduced_alphabet = get_full_dicionary()
        self.orange: List[Tuple[str, int]] = []
        self.letters_in_word: List[str] = []
        self.max_repeats = {letter: 5 for letter in ALPHABET}
        if self.strategy is None:
            self.strategy = "valid_only"

    def guess(self) -> str:
        """Given the current contraints make a guess"""
        return getattr(self, self.strategy)()

    def valid_only(self):
        """A strategy that plays on 'hard' mode. I.e. contraints from previous guesses are always used in new guesses"""
        # remove wrong letters from the alphabet
        self.reduced_alphabet = [letter for letter in ALPHABET if self.max_repeats[letter] > 0]

        possible_words = []
        for word in self.all_words:
            if self.in_reduced_alphabet(word) and self.meets_orange(word) and self.meets_green(
                    word) and self.has_all_correct_letters(word) and self.meets_repeats(word):
                possible_words.append(word)

        # determine letter prevalnce in the reduced list
        counts = [sum([letter in word for word in possible_words]) for letter in self.reduced_alphabet]

        num_top_letters = 5
        top_words = []
        while len(top_words) == 0:
            top_letters = [letter for _, letter in sorted(zip(counts, self.reduced_alphabet), reverse=True)][
                          :num_top_letters]
            for word in possible_words:
                if all([letter in top_letters for letter in word]):
                    top_words.append(word)
            num_top_letters += 1
            if num_top_letters > len(self.reduced_alphabet):
                break

        # this shouldn't happen, but is added to make debugging easier should it ever.
        if not top_words:
            return None

        # best_words = top_words
        total_letters = 5
        best_words = []
        while len(best_words) == 0:
            for word in top_words:
                if unique_letters(word) == total_letters:
                    best_words.append(word)
            total_letters -= 1

            if total_letters == 0:
                break

        self.current_guess = choice(best_words)
        return self.current_guess

    def in_reduced_alphabet(self, word: str) -> bool:
        """given the reduced alphabet check if a word is valid"""
        return all([letter in self.reduced_alphabet for letter in word])

    def has_all_correct_letters(self, word: str) -> bool:
        """given the reduced alphabet check if a word is valid"""
        return all([letter in word for letter in self.letters_in_word])

    def meets_green(self, word: str) -> bool:
        """given the green letters check if a word is valid"""
        return all([known_letter in [letter, "*"] for letter, known_letter in zip(word, self.green)])

    def meets_orange(self, word: str) -> bool:
        """check that the orange letters don't conflict"""
        return all(word[index] != letter for letter, index in self.orange)

    def meets_repeats(self, word: str) -> bool:
        """check that a letter is not repeated too many times"""
        # no need to check the alphabet, just the letter in the word
        return all(word.count(letter) <= self.max_repeats[letter] for letter in word)

    def process_response(self, response: List[LetterResponse]):
        """Given a result update the game state"""
        possible_wrong_letters = []

        times_seen_orange_or_green = {letter: 0 for letter in ALPHABET}

        for index, (letter, color) in enumerate(zip(self.current_guess, response)):
            if color == LetterResponse.GREEN:
                self.green[index] = letter
                times_seen_orange_or_green[letter] += 1

            if color == LetterResponse.ORANGE:
                self.orange.append((letter, index))
                times_seen_orange_or_green[letter] += 1

            if color == LetterResponse.GRAY:
                possible_wrong_letters.append(letter)

        # generate list of letters that are in the word
        self.letters_in_word = [letter for letter in self.green if letter != "*"] + [letter for letter, _ in
                                                                                     self.orange]
        for letter in possible_wrong_letters:
            # if a letter is gray we don't need to do this check
            self.max_repeats[letter] = times_seen_orange_or_green[letter]
