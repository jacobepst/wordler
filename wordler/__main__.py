"""sim entry point"""
from wordler.simulator import Simulator
from wordler.utils import set_up_logging

import argparse
import logging


def main() -> None:
    """"""
    parser = argparse.ArgumentParser("wordler")
    parser.add_argument(
        "--display",
        help="print guesses",
        action="store_true",
    )
    parser.add_argument(
        "--num-tests",
        help="How many sims?",
        type=int,
        default=10,
    )
    parsed = parser.parse_args()

    set_up_logging()

    simulator = Simulator(display=parsed.display)
    simulator.run(games=parsed.num_tests)

    logger = logging.getLogger(__name__)
    logger.info(f"Average solve {sum(simulator.total_guesses)/len(simulator.total_guesses)}")
    for n in range(1, 11):
        logger.info(f"{n}: {sum([num_guesses == n for num_guesses in simulator.total_guesses])}")


if __name__ == "__main__":
    main()
