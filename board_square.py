"""
File:    board_square.py
Author:  Sriram Vema
Date:    11/13/2020
Section: 43
E-mail:  sriramv1@umbc.edu
Description:
  This program runs the Royal Game of Ur
"""
class UrPiece:
    def __init__(self, color, symbol, start):
        self.color = color
        self.position = None
        self.complete = False
        self.symbol = symbol
        self.start = start

    def can_move(self, num_moves):            # For each condition, if
        if self.position == None:             # the move doesn't meet it,
            piece_move = self.start           # the function returns False
            num_moves = num_moves - 1         # otherwise it returns True
        else:
            piece_move = self.position
        if self.color == 'White':
            for i in range(num_moves):
                if piece_move == 'exit' and i != num_moves - 1 and i != 0:
                    return False
                else:
                    piece_move = piece_move.next_white
            if piece_move.piece != None:                     # This condition checks if
                if piece_move.piece.color != self.color:     # there is already a piece on
                    if piece_move.rosette == True:           # the board square
                        return False                         # If there is a piece on the square
                    else:                                    # and it is an opponent, can_move returns
                        return True                          # true so that the player can knock that piece off
                elif piece_move.piece.color == self.color:   # if the piece is the player's, then the function returns
                    return False                             # False
            else:
                return True
        else:
            for i in range(num_moves):                                      # This is the same exact code, except for
                if piece_move == 'exit' and i != num_moves - 1 and i != 0:  # black pieces, because black pieces require
                    return False                                            # .next_black to move to the next square
                else:
                    piece_move = piece_move.next_black
            if piece_move.piece != None:
                if piece_move.piece.color != self.color:
                    if piece_move.rosette == True:            # This if statement makes it so
                        return False                          # if a piece lands on a rosette,
                    else:                                     # then it can't be kicked off
                        return True
                elif piece_move.piece.color == self.color:
                    return False
            else:
                return True


class BoardSquare:
    def __init__(self, x, y, entrance=False, _exit=False, rosette=False, forbidden=False):
        self.piece = None
        self.position = (x, y)
        self.next_white = None
        self.next_black = None
        self.exit = _exit
        self.entrance = entrance
        self.rosette = rosette
        self.forbidden = forbidden


    def load_from_json(self, json_string):
        import json
        loaded_position = json.loads(json_string)
        self.piece = None
        self.position = loaded_position['position']
        self.next_white = loaded_position['next_white']
        self.next_black = loaded_position['next_black']
        self.exit = loaded_position['exit']
        self.entrance = loaded_position['entrance']
        self.rosette = loaded_position['rosette']
        self.forbidden = loaded_position['forbidden']

    def jsonify(self):
        next_white = self.next_white.position if self.next_white else None
        next_black = self.next_black.position if self.next_black else None
        return {'position': self.position, 'next_white': next_white, 'next_black': next_black, 'exit': self.exit, 'entrance': self.entrance, 'rosette': self.rosette, 'forbidden': self.forbidden}
