from os import stat
import random

from sample_players import DataPlayer
from custom_minimax_player import CustomMinimaxPlayer
from custom_negamax_player import CustomNegamaxPlayer
from custom_abnegamax_player import CustomABNegamaxPlayer


class CustomPlayer(DataPlayer):

    def __new__(cls, player_id):
        return CustomABNegamaxPlayer(player_id)
