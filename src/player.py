from src.piece import Piece


class Player:

    color = None
    
    def __init__(self, color):
        self.color = color
        self.pieces = [Piece(self.color) for x in range(0, 4)]

    def __str__(self):
        string = str(self.color)
        return string

    def move(self, number, piece):
        self.active_piece(piece).move(number)
            
    def takeout(self):
        self.next_piece_out().move(1)

    def has_won(self):
        if self.moves_left() == 0:
            return True

        return False

    def pieces_home(self):
        home = 0
        for piece in self.pieces:
            if piece.is_home():
                home += 1

        return home

    def pieces_not_home(self):
        return len(self.pieces) - self.pieces_home()

    def pieces_out(self):
        out = 0
        for piece in self.pieces:
            if piece.is_out():
                out += 1

        return out

    def pieces_in(self):
        x = 0
        for piece in self.pieces:
            if piece.is_in():
                x += 1

        return x

    def active_piece(self, pieceNum):
        num = -1
        for piece in self.pieces:
            if piece.is_out():
                num += 1
                if num==pieceNum:
                    return piece

    def next_piece_out(self):
        for piece in self.pieces:
            if piece.is_in():
                return piece

    def moves_left(self):
        left = 0
        for piece in self.pieces:
            left += piece.moves_left()

        return left