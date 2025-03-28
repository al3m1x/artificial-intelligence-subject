import random
from copy import deepcopy

from exceptions import GameplayException

class MinMaxAgent:
    def __init__(self, my_token='o', heuristic='b'):
        self.my_token = my_token
        self.enemy_token = 0
        self.heuristic = heuristic
        self.counter = 0

    def minmax(self, connect4, x,depth):
        self.counter += 1
        if depth == 0 or connect4.game_over: # przekroczona głębokość
            if self.heuristic == 'b':
                return self.basic_static_eval(connect4)
            else:
                return self.advanced_static_eval(connect4)
        return self.find_move(x, connect4, depth)

    def find_move(self, x, connect4, depth):
        if x: # wybieranie ruchu najlepszego dla nas
            max_eval = float('-inf')
            for column in connect4.possible_drops():
                new_connect4 = deepcopy(connect4)
                new_connect4.drop_token(column)
                eval = self.minmax(new_connect4, False, depth - 1) # zagłębiamy się coraz głębiej i zwracamy wyliczoną wartość eval
                max_eval = max(max_eval, eval) # wybieramy maximum z obliczonych eval
            return max_eval
        else: # wybieranie ruchu najbardziej dla nas niekorzystnego, czyli najoptymalniejszego dla naszego przeciwnika
            min_eval = float('inf')
            for column in connect4.possible_drops():
                new_connect4 = deepcopy(connect4)
                new_connect4.drop_token(column)
                eval = self.minmax(new_connect4, True, depth - 1)
                min_eval = min(min_eval, eval)
            return min_eval

    def advanced_static_eval(self, connect4):
        score = 0
        if connect4.wins == self.my_token:
            return 999999
        elif connect4.wins == self.enemy_token:
            return -999999
        else:
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
        if connect4.wins == self.my_token:
            return 999999
        elif connect4.wins == self.enemy_token:
            return -999999
        else:
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
        for column in connect4.possible_drops():
            new_connect4 = deepcopy(connect4)
            new_connect4.drop_token(column)
            score = self.minmax(new_connect4, False, 4)
            if score > best_score:
                best_score = score
                best_move = column
        return best_move


