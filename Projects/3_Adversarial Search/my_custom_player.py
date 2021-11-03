import random
from sample_players import DataPlayer
from isolation.isolation import Action, Isolation
from typing import Tuple


MAX_SEARCH_DEPTH = 2


class CustomPlayer(DataPlayer):


    def get_action(self, state: Isolation) -> None:

        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            _, action = self.search(state, 0, float('-inf'), float('inf'))
            self.queue.put(action)


    def search(self, state: Isolation, depth: int, 
               alpha: float, beta: float) -> Tuple[float, Action]:

        if state.terminal_test() or depth == MAX_SEARCH_DEPTH:
            return self.score(state), None

        best_action = None
        best_score = float('-inf')

        for action in state.actions():

            new_state = state.result(action)

            score, _ = self.search(new_state, depth + 1, 
                                   -beta, -max(alpha, best_score))
            score = -score

            if score > best_score:
                best_score = score
                best_action = action

            if best_score >= beta:
                break

        return best_score, best_action


    def score(self, state: Isolation) -> int:

        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]

        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)

        return len(own_liberties) - len(opp_liberties)