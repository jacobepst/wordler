"""class that simulates a game of wordle (with a game and a solver)"""

from wordler.solver import Solver
from wordler.wordle_game import WordleGame

from logging import getLogger


class Simulator:
    """A Wordle simulator"""

    def __init__(self, display: bool = False, strategy: str = None):
        self.words = []
        self.total_guesses = []
        self.display = display
        self.strategy = strategy

    def run(self, games: int = 100):
        """Loop through the desired number of games and simulate"""
        for game in range(games):
            self.run_game()

    def run_game(self):
        """Simulate a single game."""
        logger = getLogger(__name__)
        s = Solver(strategy=self.strategy)
        w = WordleGame(display=self.display)
        if self.display:
            logger.info("-" * 45)
        while not w.complete:
            guess = s.guess()
            if guess is None:
                logger.warning("FAIL")
                logger.warning(f"{w.true_word}, {s.green}, {s.orange}, {s.max_repeats}")
                w.total_guesses = 10
                breakpoint()
                break
            response = w.guess(guess)
            s.process_response(response)
        self.words.append(w.true_word)
        self.total_guesses.append(w.total_guesses)
