import numpy as np
import random

# helper functions

# tested and detects horizontal, vertical, diagonal and if 0
def term_test(board, depth):
    # checks if game over or if depth == 0
    # returns true if terminal
    player1_win_str= '{0}{0}{0}{0}'.format(1)
    player2_win_str= '{0}{0}{0}{0}'.format(2)
    to_str = lambda a: ''.join(a.astype(str))
    if depth == 0:
        print 'depth == 0 reached'
        return True

    def check_horizontal(b):
        for row in b:
            if player1_win_str in to_str(row):
                return True
            elif player2_win_str in to_str(row):
                return True
        return False

    def check_verticle(b):
        return check_horizontal(b.T)

    def check_diagonal(b):
        for op in [None, np.fliplr]:
            op_board = op(b) if op else b

            root_diag = np.diagonal(op_board, offset=0).astype(np.int)
            if player1_win_str in to_str(root_diag):
                return True
            if player2_win_str in to_str(root_diag):
                return True

            for i in range(1, b.shape[1]-3):
                for offset in [i, -i]:
                    diag = np.diagonal(op_board, offset=offset)
                    diag = to_str(diag.astype(np.int))
                    if player1_win_str in diag:
                        return True
                    if player2_win_str in diag:
                        return True

        return False

    return (check_horizontal(board) or
            check_verticle(board) or
            check_diagonal(board))

# same as Result in pseudocode
# tested and places above preexisting piece in correct column
def Result(board, action, player_num):
    if 0 in board[:,action]:
        for row in range(0, 6):
            index = 5 - row
            print('Result: checking row', index)
            if board[index, action] == 0:
                print('Result: inserting at row', index)
                board[index, action] = player_num
                return board
    else:
        err = 'Invalid move by player {}. Column {}'.format(player_num, action)
        raise Exception(err)

# get the other player's number
# tested and works as expected
def other_player(player_num):
    if player_num == 1:
        return 2
    elif player_num == 2:
        return 1
    else:
        print 'Error: player_num != 1 or 2'
        return -1

# get all available actions
# tested and works as expected
def Actions(board):
    valid_cols = []
    for col in range(board.shape[1]):
        if 0 in board[:,col]:
            valid_cols.append(col)

    return valid_cols


def count_connected(board, player_num):
    # counts 'count' number of connected pieces 
    print('player_num =', player_num)
    two_count = '{0}{0}'.format(player_num)
    three_count = '{0}{0}{0}'.format(player_num)
    to_str = lambda a: ''.join(a.astype(str))
    for row in board:
        if two_count in to_str(row):
            print(row, ":")
            print("Found 2 in a row!")
        if three_count in to_str(row):
            print(row, ":")
            print("Found 3 in a row!")
	

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        print('get_alpha_beta_move: printing the board')
        print(board)
        count_connected(board, self.player_number)
        valid_cols = Actions(board)
        print('Actions(board) =', Actions(board))
        test = random.randint(0, 6)

        # testing term_test
        print('Testing random chose', test)
        print('Term_test(board, 0) =', term_test(board, 0))
        print('Term_test(board, 1) =', term_test(board, 1))
        testboard = np.zeros([6,7]).astype(np.uint8)
        testboard[5] = [1, 1, 1, 1, 0, 0, 0]
        print('Test board = ', testboard)
        print('Term_test(testboard, 0) =', term_test(testboard, 1))
        testboard = np.zeros([6,7]).astype(np.uint8)
        testboard[5][0] = 1
        testboard[4][0] = 1
        testboard[3][0] = 1
        testboard[2][0] = 1
        print('Test board = ', testboard)
        print('Term_test(testboard, 0) =', term_test(testboard, 1))
        testboard = np.zeros([6,7]).astype(np.uint8)
        testboard[5][0] = 1
        testboard[4][1] = 1
        testboard[3][2] = 1
        testboard[2][3] = 1
        print('Test board = ', testboard)
        print('Term_test(testboard, 0) =', term_test(testboard, 1))

        # testing Result
        testboard = np.zeros([6,7]).astype(np.uint8)
        testboard[5] = [1, 1, 1, 1, 0, 0, 0]
        print('Test board = ', testboard)
        testboard = Result(testboard, 1, self.player_number)
        print('Test board after Result(testboard, 1, self.player_number) = ', testboard)
        

        return test
        

    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        # raise NotImplementedError('Whoops I don\'t know what to do')
	#for i, j in range(0:6, 1:6)




    def evaluation_function(self, board):
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
       
       
        return 0


class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

