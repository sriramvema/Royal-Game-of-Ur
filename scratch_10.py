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
                    # print(square.piece.symbol)
                    output[MAX_Y * i + 2][MAX_X * j + 3: MAX_X * j + 5] = square.piece.symbol
    def find_white_entrance(self):
        for i in range(len(self.board)):
            for square in self.board[i]:
                if square.entrance == 'White':
                    white_start = square
                    return white_start

    def find_white_exit(self):
        for i in range(len(self.board)):
            for square in self.board[i]:
                if square.exit == 'White':
                    white_end = square
                    return white_end

    def find_black_entrance(self):
        for i in range(len(self.board)):
            for square in self.board[i]:
                if square.entrance == 'Black':
                    black_start = square
                    return black_start

    def find_black_exit(self):
        for i in range(len(self.board)):
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

    def black_pieces(self):
        black_piece_list = []
        for i in range(7):
            b = str(i+1)
            b = 'B' + b
            i = UrPiece('Black', b, self.find_black_entrance())
            black_piece_list.append(i)
        return black_piece_list

    def white_pieces(self):
        white_piece_list = []
        for i in range(7):
            b = str(i+1)
            b = 'W' + b
            self.find_white_entrance()
            i = UrPiece('White', b, self.find_white_entrance())

            white_piece_list.append(i)
        return white_piece_list

    def player_info(self, player, color, piece_list):
        player['Name'] = input('What is your name? ')
        player['Color'] = color
        print(player['Name'] + ', you will be', color)
        player['Pieces'] = piece_list
        return player

    def player_roll(self, player1):
        dice_roll = self.roll_d4_dice(n=4)
        print(player1['Name'], 'you rolled a', dice_roll)
        if dice_roll == 0:
            print('You can\'t move')
        else:
            for i in range(len(player1['Pieces'])):
                if player1['Pieces'][i].position == None:
                    print(i + 1, player1['Pieces'][i].symbol, 'currently off the board')
                else:
                    print(i + 1, player1['Pieces'][i].symbol, player1['Pieces'][i].position.position)
            move_option = int(input('What move do you wish to make? '))
            move_chance = player1['Pieces'][move_option - 1].can_move(dice_roll)
            print(player1['Pieces'][move_option - 1].start.next_white.next_white.next_white.rosette)


    def player_turn(self, player):
        piece = self.player_roll(player)
        self.display_board()

        complete_pieces = 0
        for i in range(len(player['Pieces'])):
            if player['Pieces'][i].complete == True:
                complete_pieces += 1
        return complete_pieces


    def play_game(self):
        """
            Your job is to recode this function to play the game.
        """
        a = self.white_pieces()
        player1 = {}
        player2 = {}
        player1 = self.player_info(player1, 'White', a)
        b = self.black_pieces()
        player2 = self.player_info(player2, 'Black', b)
        self.display_board()
        player1_complete_pieces = 0
        player2_complete_pieces = 0
        while player1_complete_pieces != 7 and player2_complete_pieces != 7:
            player1_complete_pieces = self.player_turn(player1)
            player2_complete_pieces = self.player_turn(player2)










if __name__ == '__main__':
    file_name = input('What is the file name of the board json? ') if len(argv) < 2 else argv[1]
    rgu = RoyalGameOfUr(file_name)
    rgu.play_game()