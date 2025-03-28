from exceptions import GameplayException
from connect4 import Connect4
from randomagent import RandomAgent
from alphabetaagent import AlphaBetaAgent
from minmaxagent import MinMaxAgent

# 1. random vs minmax (mozna kilka razy dla x i o)
# 2. random vs alphabeta
# 3. advanced_static_eval - x, alphabeta, basic vs o, alphabeta, advanced i odwrotnie

connect4 = Connect4(width=7, height=6)
agent1 = AlphaBetaAgent('o', 'b')
agent2 = RandomAgent('x')
AlphaBetaWins = 0
RandomWins = 0

for i in range(5):
    while not connect4.game_over:
        connect4.draw()
        try:
            if connect4.who_moves == agent1.my_token:
                n_column = agent1.decide(connect4)
            else:
                n_column = agent2.decide(connect4)
            connect4.drop_token(n_column)
        except (ValueError, GameplayException):
            print('invalid move')
    if connect4.wins == 'o':
        AlphaBetaWins += 1
    else:
        RandomWins += 1
    connect4 = Connect4(width=7, height=6)

agent1 = AlphaBetaAgent('x', 'b')
agent2 = RandomAgent('o')

for i in range(5):
    while not connect4.game_over:
        connect4.draw()
        try:
            if connect4.who_moves == agent1.my_token:
                n_column = agent1.decide(connect4)
            else:
                n_column = agent2.decide(connect4)
            connect4.drop_token(n_column)
        except (ValueError, GameplayException):
            print('invalid move')
    if connect4.wins == 'x':
        AlphaBetaWins += 1
    else:
        RandomWins += 1
    connect4 = Connect4(width=7, height=6)

connect4.draw()
# print('MinMax counter: ', agent1.counter)
print('AlphaBeta wins: ', AlphaBetaWins)
print('RandomWins: ', RandomWins)
# print('AlphaBeta counter: ', agent2.counter)