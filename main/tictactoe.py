import random

class Tic(object):
    winningCombos = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6])

    winners = ('X-win', 'Draw', 'O-win')

    def __init__(self, squares=[]):
        if len(squares) == 0:
            self.squares = [None for i in range(9)]
        else:
            self.squares = squares

    def show(self):
        # Draws the opponent's and computer's move on the command line
        for element in [self.squares[i:i + 3] for i in range(0, len(self.squares), 3)]:
            print element

        print "\r\n"

    def availableMoves(self):
        # returns all the available moves from 0 - 8
        """what spots are left empty?"""
        return [k for k, v in enumerate(self.squares) if v is None]

    def available_combos(self, player):
        """what combos are available?"""
        return self.availableMoves() + self.getSquares(player)

    def complete(self):
        # Check if the game is over yet
        """is the game over?"""
        if None not in [v for v in self.squares]:
            return True
        if self.winner() != None:
            return True
        return False

    def xWon(self):
        return self.winner() == 'X'

    def oWon(self):
        return self.winner() == 'O'

    def tied(self):
        return self.complete() == True and self.winner() is None

    def winner(self):
        for player in ('X', 'O'):
            positions = self.getSquares(player)
            for combo in self.winningCombos:
                win = True
                for pos in combo:
                    if pos not in positions:
                        win = False
                if win:
                    return player
        return None

    def getSquares(self, player):
        """squares that belong to a player"""
        return [k for k, v in enumerate(self.squares) if v == player]

    def makeMove(self, position, player):
        """place on square on the board"""
        self.squares[position] = player

    def alphabeta(self, node, player, alpha, beta):
        if node.complete():
            if node.xWon():
                return -1
            elif node.tied():
                return 0
            elif node.oWon():
                return 1
        for move in node.availableMoves():
            node.makeMove(move, player)
            val = self.alphabeta(node, getEnemy(player), alpha, beta)
            node.makeMove(move, None)
            if player == 'O':
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    return beta
            else:
                if val < beta:
                    beta = val
                if beta <= alpha:
                    return alpha
        if player == 'O':
            return alpha
        else:
            return beta

def determine(board, player):
    a = -2
    choices = []
    if len(board.availableMoves()) == 0:
        return 4
    for move in board.availableMoves():
        board.makeMove(move, player)
        val = board.alphabeta(board, getEnemy(player), -2, 2)
        board.makeMove(move, None)
        board.winners[val + 1]
        if val > a:
            a = val
            choices = [move]
        elif val == a:
            choices.append(move)
    return random.choice(choices)

def getEnemy(player):
    if player == 'X':
        return 'O'
    return 'X'
