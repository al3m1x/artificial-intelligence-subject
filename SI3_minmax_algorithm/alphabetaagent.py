import random
from copy import deepcopy
from exceptions import GameplayException

class AlphaBetaAgent:
    def __init__(self, my_token='o', heuristic='b'):
        self.my_token = my_token
        self.enemy_token = 0
        self.heuristic = heuristic
        self.counter = 0

    def alphabeta(self, connect4, depth, alpha, beta, x):
        self.counter += 1
        if depth == 0:  # przekroczona głębokość
            if self.heuristic == 'b':
                return self.basic_static_eval(connect4)
            else:
                return self.advanced_static_eval(connect4)
        if connect4.game_over:
            if connect4.wins == self.enemy_token:  # przegrana
                return 999999
            elif connect4.wins == self.my_token:  # wygrana
                return 999999
            else:  # remis
                return 0
        if x:
            max_eval = float('-inf')
            for column in connect4.possible_drops():
                new_connect4 = deepcopy(connect4)
                new_connect4.drop_token(column)
                eval = self.alphabeta(new_connect4, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for column in connect4.possible_drops():
                new_connect4 = deepcopy(connect4)
                new_connect4.drop_token(column)
                eval = self.alphabeta(new_connect4, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def advanced_static_eval(self, connect4):
        score = 0
        for four in connect4.iter_fours():
            if four.count(self.my_token) == 3 and four.count('_') == 1:
                score += 5
            elif four.count(self.my_token) == 2 and four.count('_') == 2:
                score += 2
            elif four.count(self.my_token) == 1 and four.count('_') == 3:
                score += 1
            elif four.count(self.enemy_token) == 3 and four.count('_') == 1:
                score -= 5
            elif four.count(self.enemy_token) == 2 and four.count('_') == 2:
                score -= 2
            elif four.count(self.enemy_token) == 1 and four.count('_') == 3:
                score -= 1
        return score

    def basic_static_eval(self, connect4):
        score = 0
        for four in connect4.iter_fours():
            if four.count(self.my_token) == 3:
                score += 1
            elif four.count(self.enemy_token) == 3:
                score -= 1
        return score

    def decide(self, connect4):
        if self.my_token == 'o':
            self.enemy_token = 'x'
        else:
            self.enemy_token = 'o'

        if connect4.who_moves != self.my_token:
            raise GameplayException('not my round')

        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        for column in connect4.possible_drops():
            new_connect4 = deepcopy(connect4)
            new_connect4.drop_token(column)
            score = self.alphabeta(new_connect4, 6, alpha, beta, False)
            if score > best_score:
                best_score = score
                best_move = column
            alpha = max(alpha, score)
        return best_move
