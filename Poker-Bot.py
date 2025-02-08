#!/usr/bin/env python3
import asyncio
import argparse
from tg.bot import Bot
import time
from enum import Enum, IntEnum

parser = argparse.ArgumentParser(
    prog='Template bot',
    description='A Turing Games poker bot that always checks or calls, no matter what the target bet is (it never folds and it never raises)')

parser.add_argument('--port', type=int, default=1999,
                    help='The port to connect to the server on')
parser.add_argument('--host', type=str, default='localhost',
                    help='The host to connect to the server on')
parser.add_argument('--room', type=str, default='my-new-room',
                    help='The room to connect to')
parser.add_argument('--username', type=str, default='bot',
                    help='The username for this bot (make sure it\'s unique)')

args = parser.parse_args()


class Rank(IntEnum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

class Suit(Enum):
    HEARTS = 'hearts'
    DIAMONDS = 'diamonds'
    CLUBS = 'clubs'
    SPADES = 'spades'

def preflop(hand):
    if len(hand) != 2:
        raise ValueError("Hand must contain exactly 2 cards.")

    card1, card2 = hand



    # Map the enum values to their common string representations.
    rank_to_str = {
        Rank.ACE: "A",
        Rank.KING: "K",
        Rank.QUEEN: "Q",
        Rank.JACK: "J",
        Rank.TEN: "T",
        Rank.NINE: "9",
        Rank.EIGHT: "8",
        Rank.SEVEN: "7",
        Rank.SIX: "6",
        Rank.FIVE: "5",
        Rank.FOUR: "4",
        Rank.THREE: "3",
        Rank.TWO: "2",
    }

    # If the two cards form a pair, just return the letter twice.
    if card1.rank == card2.rank:
        return poker_ranking[rank_to_str[card1.rank] * 2]
    

    # For non-pairs, we want to order the cards with the highest rank first.
    # In typical poker, Ace is considered highest, so we define a custom order.
    poker_rank_order = {
        Rank.ACE: 14,
        Rank.KING: 13,
        Rank.QUEEN: 12,
        Rank.JACK: 11,
        Rank.TEN: 10,
        Rank.NINE: 9,
        Rank.EIGHT: 8,
        Rank.SEVEN: 7,
        Rank.SIX: 6,
        Rank.FIVE: 5,
        Rank.FOUR: 4,
        Rank.THREE: 3,
        Rank.TWO: 2,
    }

    # Sort cards in descending order by their poker ranking value.
    sorted_cards = sorted(hand, key=lambda c: poker_rank_order[c.rank], reverse=True)
    first_card, second_card = sorted_cards

    # Build the string using the rank abbreviations.
    combo = rank_to_str[first_card.rank] + rank_to_str[second_card.rank]

    # Append suited/offsuit marker.
    if first_card.suit == second_card.suit:
        combo += "s"
    else:
        combo += "o"

    return poker_ranking[combo]


poker_ranking = {
    'AA': 0, 'AKs': 2, 'AQs': 2, 'AJs': 3, 'ATs': 5, 'A9s': 8, 'A8s': 10, 'A7s': 13, 'A6s': 14, 'A5s': 12, 'A4s': 14, 'A3s': 14, 'A2s': 17,
    'AKo': 5, 'KK': 1, 'KQs': 3, 'KJs': 3, 'KTs': 6, 'K9s': 10, 'K8s': 16, 'K7s': 19, 'K6s': 24, 'K5s': 25, 'K4s': 25, 'K3s': 26, 'K2s': 26,
    'AQo': 8, 'KQo': 9, 'QQ': 1, 'QJs': 5, 'QTs': 6, 'Q9s': 10, 'Q8s': 19, 'Q7s': 26, 'Q6s': 28, 'Q5s': 29, 'Q4s': 29, 'Q3s': 30, 'Q2s': 31,
    'AJo': 12, 'KJo': 14, 'QJo': 15, 'JJ': 2, 'JTs': 6, 'J9s': 11, 'J8s': 17, 'J7s': 27, 'J6s': 33, 'J5s': 35, 'J4s': 37, 'J3s': 37, 'J2s': 38,
    'ATo': 18, 'KTo': 20, 'QTo': 22, 'JTo': 21, 'TT': 4, 'T9s': 10, 'T8s': 16, 'T7s': 25, 'T6s': 31, 'T5s': 40, 'T4s': 40, 'T3s': 41, 'T2s': 41,
    'A9o': 32, 'K9o': 35, 'Q9o': 36, 'J9o': 34, 'T9o': 31, '99': 7, '98s': 17, '97s': 24, '96s': 29, '95s': 38, '94s': 47, '93s': 47, '92s': 49,
    'A8o': 39, 'K8o': 50, 'Q8o': 53, 'J8o': 48, 'T8o': 43, '98o': 42, '88': 9, '87s': 21, '86s': 27, '85s': 33, '84s': 40, '83s': 53, '82s': 54,
    'A7o': 45, 'K7o': 57, 'Q7o': 66, 'J7o': 59, 'T7o': 59, '97o': 55, '87o' : 52, '77': 12, '76s': 25, '75s': 28, '74s': 37, '73s': 45, '72s': 56,
    'A6o': 51, 'K6o': 60, 'Q6o': 71, 'J6o': 80, 'T6o': 74, '96o': 68, '86':61, '76':57, '66': 16, '65s': 27, '64s': 29, '63s': 38, '62s': 49,
    'A5o': 44, 'K5o': 63, 'Q5o': 75, 'J5o': 82, 'T5o': 89, '95o': 83, '85o': 73, '75o': 65, '65o': 58, '55': 20,'54s': 28, '53s': 32, '52s': 39,  
    'A4o': 46, 'K4o': 67, 'Q4o': 76, 'J4o': 85, 'T4o': 90, '94o': 95, '84o': 88, '74o': 78, '64o': 70, '54o': 62,'44': 23, '43s': 36, '42s': 41, 
    'A3o': 49, 'K3o': 67, 'Q3o': 77, 'J3o': 86, 'T3o': 92, '93o': 96, '83o': 98, '73o': 93, '63o': 81, '53o': 72, '43': 76, '33': 23, '32s': 46,  
    'A2o': 54, 'K2o': 69, 'Q2o': 79, 'J2o': 87, 'T2o': 94, '92o': 97, '82o': 99, '72o': 100, '62o': 95, '52o': 84, '42o':86, '32o': 91, '22': 24
    }


class TemplateBot(Bot):
    def act(self, state, hand):
        print('asked to act')
        print('acting', state, hand, self.my_id)

        if (state.round == 'pre-flop'):
            print('preflop', preflop(hand))
            if (preflop(hand) > 24):
                return {'type': 'raise', 'amount': 1000}
        else:
            return {'type': 'call'}

        """
        if (preflop(hand) > 24):
            return {'type': 'flop'}
        elif (state.round == 'pre-flop'): 
            return {'type': 'raise', 'amount': self.stack}
        else:
            return {'type': 'call'}
        """

    def opponent_action(self, action, player):
        print('opponent action?', action, player)

    def game_over(self, payouts):
        print('game over', payouts)

    def start_game(self, my_id):
        self.my_id = my_id
        print('start game', my_id)

if __name__ == "__main__":
    bot = TemplateBot(args.host, args.port, args.room, args.username)
    asyncio.run(bot.start())
