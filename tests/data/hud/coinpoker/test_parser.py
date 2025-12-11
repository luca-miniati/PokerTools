import os
from pokertools.data.hud.coinpoker.parser import CoinPokerParser


ROOT_DIR = os.path.join(os.path.dirname(__file__), 'data')


def test_parse_mtt() -> None:
    parser = CoinPokerParser()
    path = os.path.join(ROOT_DIR, 'mtt1.txt')
    with open(path) as f:
        hh = f.read()
        hh = next(parser(hh))

    breakpoint()