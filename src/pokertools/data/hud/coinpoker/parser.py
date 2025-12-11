from re import compile, DOTALL, MULTILINE
from collections import defaultdict
from dataclasses import dataclass
from operator import add
from pokerkit.notation import REParser
from pokerkit.utilities import UNMATCHABLE_PATTERN, parse_time


@dataclass
class CoinPokerParser(REParser):
    "A class for CoinPoker hand history parser."

    HAND = compile(r'^CoinPoker Hand #\d+.*?(?=^\n{2,})', DOTALL | MULTILINE)
    FINAL_SEAT = compile(r' Seat #(?P<final_seat>\d+) is the button')
    VARIANT = compile(r"CoinPoker Hand #\d+: .*(?P<variant>Hold'em No Limit|Omaha Pot Limit).*\(")
    VARIANTS = { "Hold'em No Limit": 'NT', 'Omaha Pot Limit': 'PLO' }
    SEATS = compile(r'Seat (?P<seat>\d+): (?P<player>.+) \(\D?[0-9.,]+ in chips\)')
    ANTE_POSTING = compile(r'(?P<player>.+): posts the ante \D?(?P<ante>[0-9.,]+)')
    BLIND_OR_STRADDLE_POSTING = compile(r'(?P<player>.+): posts (small|big) blind \D?(?P<blind_or_straddle>[0-9.,]+)')
    STARTING_STACKS = compile(r'Seat \d+: (?P<player>.+) \(\D?(?P<starting_stack>[0-9.,]+) in chips\)')
    HOLE_DEALING = UNMATCHABLE_PATTERN
    BOARD_DEALING = compile(
        (
            r'\*\*\*'
            r'('
            r' (FLOP)'
            r' \*\*\*'
            r'|'
            r' (TURN|RIVER)'
            r' \*\*\*'
            r' \[[0-9TJQKAcdhs ]+\]'
            r')'
            r' \[(?P<cards>[0-9TJQKAcdhs ]+)\]'
        ),
    )
    FOLDING = compile(r'(?P<player>.+): folds')
    CHECKING_OR_CALLING = compile(r'(?P<player>.+): (calls|checks)')
    COMPLETION_BETTING_OR_RAISING = compile(
        (
            r'(?P<player>.+)'
            r':'
            r' (bets|raises|all-in(\(raise\))?)'
            r' \D?(?P<amount>[0-9.,]+)'
        ),
    )
    HOLE_CARDS_SHOWING = compile(
        r'(?P<player>.+): shows \[(?P<cards>[0-9TJQKAcdhs ]+)\]',
    )
    CONSTANTS = {'venue': 'CoinPoker'}
    DATETIME = compile(
        (
            r' (?P<year>\d+)\/(?P<month>\d+)\/(?P<day>\d+)'
            r' (?P<time>\d{2}:\d{2}:\d{2})'
            r' (?P<time_zone_abbreviation>\S+)'
        ),
    )
    VARIABLES = {
        'time': (DATETIME, parse_time),
        'day': (DATETIME, int),
        'month': (DATETIME, int),
        'year': (DATETIME, int),
        'hand': (compile(r'CoinPoker Hand #(?P<hand>\d+):'), int),
        'seat_count': (compile(r'(?P<seat_count>\d+)-max'), int),
        'table': (compile(r"Table: '(?P<table>.+?)' \d+-max"), str),
        'currency_symbol': (compile('₮'), str),
    }
    PLAYER_VARIABLES = {
        'winnings': (
            compile(
                (
                    r'(?P<player>.+?)'
                    r' collected'
                    r' \D?(?P<winnings>[0-9.,]+) from pot'
                ),
            ),
            None,
            int,
            add,
        ),
    }

    # def _get_completion_betting_or_raising_to_amount(
    #     self,
    #     bets: defaultdict[str, int],
    #     player: str,
    #     completion_betting_or_raising_amount: int,
    #     line: str,
    # ) -> int:
    #     return bets[player] + completion_betting_or_raising_amount