from src.color import Color


class Piece:

    HOME_POSITION = 57
    position = 0

    def __init__(self, color: Color):
        self.position = 0
        self.color = color

    def move(self, places):
        if self.can_move(places):
            self.position += places
        else :
            self.position += places
            overshot = self.position - self.HOME_POSITION
            self.position = self.HOME_POSITION - overshot

    def can_move(self, places):
        if (self.position + places) <= self.HOME_POSITION:
            return True

        return False

    def moves_left(self):
        return self.HOME_POSITION - self.position

    def is_in(self):
        if self.position == 0:
            return True

        return False

    def is_out(self):
        if self.position > 0 and not self.is_home():
            return True

        return False

    def is_home(self):
        if self.position == self.HOME_POSITION:
            return True

        return False

    def return_to_start(self):
        if not self.is_home():
            self.position = 0