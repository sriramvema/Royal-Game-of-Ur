"""
File:    royal_game_of_ur.py
Author:  Sriram Vema
Date:    11/13/2020
Section: 43
E-mail:  sriramv1@umbc.edu
Description:
  This program runs the Royal Game of Ur
"""
from sys import argv
from random import choice
from board_square import BoardSquare, UrPiece


class RoyalGameOfUr:
    STARTING_PIECES = 7

    def __init__(self, board_file_name):
        self.board = None
        self.load_board(board_file_name)

    def load_board(self, board_file_name):
        """
        This function takes a file name and loads the map, creating BoardSquare objects in a grid.

        :param board_file_name: the board file name
        :return: sets the self.board object within the class
        """

        import json
        try:
            with open(board_file_name) as board_file:
                board_json = json.loads(board_file.read())
                self.num_pieces = self.STARTING_PIECES
                self.board = []
                for x, row in enumerate(board_json):
                    self.board.append([])
                    for y, square in enumerate(row):
                        self.board[x].append(BoardSquare(x, y, entrance=square['entrance'], _exit=square['exit'], rosette=square['rosette'], forbidden=square['forbidden']))

                for i in range(len(self.board)):
                    for j in range(len(self.board[i])):
                        if board_json[i][j]['next_white']:
                            x, y = board_json[i][j]['next_white']
                            self.board[i][j].next_white = self.board[x][y]
                        if board_json[i][j]['next_black']:
                            x, y = board_json[i][j]['next_black']
                            self.board[i][j].next_black = self.board[x][y]
        except OSError:
            print('The file was unable to be opened. ')

    def draw_block(self, output, i, j, square):
        """
        Helper function for the display_board method
        :param output: the 2d output list of strings
        :param i: grid position row = i
        :param j: grid position col = j
        :param square: square information, should be a BoardSquare object
        """
        MAX_X = 8
        MAX_Y = 5
        for y in range(MAX_Y):
            for x in range(MAX_X):
                if x == 0 or y == 0 or x == MAX_X - 1 or y == MAX_Y - 1:
                    output[MAX_Y * i + y][MAX_X * j + x] = '+'
                if square.rosette and (y, x) in [(1, 1), (1, MAX_X - 2), (MAX_Y - 2, 1), (MAX_Y - 2, MAX_X - 2)]:
                    output[MAX_Y * i + y][MAX_X * j + x] = '*'
                if square.piece:
                    output[MAX_Y * i + 2][MAX_X * j + 3: MAX_X * j + 5] = square.piece.symbol

    def find_white_entrance(self):
        for i in range(len(self.board)):          # This functions finds the entrance
            for square in self.board[i]:          # board square for the white side.
                if square.entrance == 'White':
                    white_start = square
                    return white_start

    def find_white_exit(self):                 # This function finds the exit
        for i in range(len(self.board)):       # for the white side.
            for square in self.board[i]:
                if square.exit == 'White':
                    white_end = square
                    return white_end

    def find_black_entrance(self):                # This function finds the entrance
        for i in range(len(self.board)):          # board square for the black side.
            for square in self.board[i]:
                if square.entrance == 'Black':
                    black_start = square
                    return black_start

    def find_black_exit(self):               # This function finds the exit
        for i in range(len(self.board)):     # for the black side.
            for square in self.board[i]:
                if square.exit == 'Black':
                    black_end = square
                    return black_end

    def display_board(self):
        """
        Draws the board contained in the self.board object

        """
        if self.board:
            output = [[' ' for _ in range(8 * len(self.board[i//5]))] for i in range(5 * len(self.board))]
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if not self.board[i][j].forbidden:
                        self.draw_block(output, i, j, self.board[i][j])

            print('\n'.join(''.join(output[i]) for i in range(5 * len(self.board))))

    def roll_d4_dice(self, n=4):
        """
        Keep this function as is.  It ensures that we'll have the same runs with different random seeds for rolls.
        :param n: the number of tetrahedral d4 to roll, each with one dot on
        :return: the result of the four rolls.
        """
        dots = 0
        for _ in range(n):
            dots += choice([0, 1])
        return dots

    def black_pieces(self):                # This function creates each
        black_piece_list = []              # black piece and assigns it to
        for i in range(7):                 # a UrPiece class
            b = str(i+1)                   # then it adds all the black pieces
            b = 'B' + b                    # to one list.
            i = UrPiece('Black', b, self.find_black_entrance())
            black_piece_list.append(i)
        return black_piece_list

    def white_pieces(self):         # This function does the
        white_piece_list = []       # exact same thing as black_pieces
        for i in range(7):          # but for the white pieces.
            b = str(i+1)
            b = 'W' + b
            i = UrPiece('White', b, self.find_white_entrance())

            white_piece_list.append(i)
        return white_piece_list

    def player_info(self, player, color, piece_list):       # This function creates a
        player['Name'] = input('What is your name? ')       # dictionary for each player
        player['Color'] = color                             # and adds their name, what color
        print(player['Name'] + ', you will be', color)      # they are playing as, and the list
        player['Pieces'] = piece_list                       # that holds all of their pieces.
        return player

    def player_roll(self, player1):                           # This function rolls the dice and asks
        dice_roll = self.roll_d4_dice(n=4)                    # the player which piece they want to move,
        print(player1['Name'], 'you rolled a', dice_roll)     # then it runs the can_move function to see
        if dice_roll == -1:                                   # if the piece can make that move or not.
            print('You can\'t move')
        else:
            for i in range(len(player1['Pieces'])):                                      # This prints the position
                if player1['Pieces'][i].position == None:                                # for each piece.
                    print(i + 1, player1['Pieces'][i].symbol, 'currently off the board')
                else:
                    print(i + 1, player1['Pieces'][i].symbol, player1['Pieces'][i].position.position)
            move_option = int(input('What move do you wish to make? '))
            move_chance = player1['Pieces'][move_option - 1].can_move(dice_roll)
            if move_chance == False:                                              # If can_move returns False,
                print('No moves are possible with the current dice roll')         # the piece isn't allowed to move.
            elif move_chance == True:
                if player1['Pieces'][move_option - 1].position == None:
                    player1['Pieces'][move_option - 1].position = player1['Pieces'][move_option - 1].start
                    dice_roll = dice_roll - 1
                player1['Pieces'][move_option - 1].position.piece = None
                piece_move = player1['Pieces'][move_option - 1].position         # Before the piece is moved, piece_move
                for i in range(dice_roll):                                       # goes to the new board_square to check
                    if player1['Pieces'][move_option - 1].color == 'White':      # if it is occupied by another piece.
                        if piece_move.exit == 'White' and i > 0:
                            player1['Pieces'][move_option - 1].position = None
                            player1['Pieces'][move_option - 1].complete = True
                        else:
                            piece_move = piece_move.next_white
                    else:
                        if piece_move.exit == 'Black' and i > 0:                       # If piece_move checks the new
                            player1['Pieces'][move_option - 1].position = None         # board square and finds that
                            player1['Pieces'][move_option - 1].complete = True         # opponent's piece is on it,
                        else:                                                          # this if statement kicks the
                            piece_move = piece_move.next_black                         # opponent's piece off the board.
                if piece_move.piece != None:
                    if piece_move.rosette == True:
                        print('No moves are possible with the current dice roll')
                    else:
                        if piece_move.piece.color != player1['Pieces'][move_option - 1].color:
                            piece_move.piece.position = None
                            piece_move.piece = None
                            player1['Pieces'][move_option - 1].position = piece_move
                            piece_move.piece = player1['Pieces'][move_option - 1]
                            player1['Pieces'][move_option - 1].position.piece = player1['Pieces'][move_option - 1]
                else:
                    player1['Pieces'][move_option - 1].position = piece_move
                    piece_move.piece = player1['Pieces'][move_option - 1]
                    player1['Pieces'][move_option - 1].position.piece = player1['Pieces'][move_option - 1]

            return move_option - 1

    def player_turn(self, player):                                                   # This function runs player_roll
        piece = self.player_roll(player)                                             # and then displays the board with
        self.display_board()                                                         # the new piece positions
        if player['Pieces'][piece].position.rosette == True:                         # Then it sees if the new pieces
            print(player['Name'], 'you landed on a rosette, you get another turn.')  # have landed on a rosette.
            self.player_roll(player)                                                 # If someone landed on a rosette,
            self.display_board()                                                     # they get another turn.
        complete_pieces = 0
        for i in range(len(player['Pieces'])):            # This for loop runs a counter
            if player['Pieces'][i].complete == True:      # to count how many pieces have
                complete_pieces += 1                      # completed the path
        return complete_pieces                            # and returns that number.


    def play_game(self):
        """
            Your job is to recode this function to play the game.
        """
        a = self.white_pieces()
        player1 = {}
        player2 = {}
        player1 = self.player_info(player1, 'White', a)   # This sets up the game by running functions to set up
        b = self.black_pieces()                           # the player dictionaries
        player2 = self.player_info(player2, 'Black', b)
        self.display_board()
        player1_complete_pieces = 0
        player2_complete_pieces = 0
        while player1_complete_pieces != 7 and player2_complete_pieces != 7:  # This while loop runs the game until
            player1_complete_pieces = self.player_turn(player1)               # one of the players gets all 7 of their
            player2_complete_pieces = self.player_turn(player2)               # pieces across the board and out the exit










if __name__ == '__main__':
    file_name = input('What is the file name of the board json? ') if len(argv) < 2 else argv[1]
    rgu = RoyalGameOfUr(file_name)
    rgu.play_game()
