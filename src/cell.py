import pygame


class Cell:

    def __init__(self, x, y, color_id, track_id = None, cell_size = 50, border_size = 3):
        self.x = x
        self.y = y
        self.color_id = int(color_id)
        self.track_id = track_id
        self.cell_size = cell_size
        self.border_size = border_size

    def __str__(self):
        return str(self.x) + " / " + str(self.y) + " / " + str(self.color()) + " / " + str(self.track_id)

    def color(self):
        if self.color_id == 0:
            return pygame.Color("white")
        elif self.color_id == 1:
            return pygame.Color("red")
        elif self.color_id == 2:
            return pygame.Color("green")
        elif self.color_id == 3:
            return pygame.Color("skyblue")
        elif self.color_id == 4:
            return pygame.Color("gold")
        elif self.color_id == 6:
            return pygame.Color("forestgreen")
        elif self.color_id == 7:
            return pygame.Color("goldenrod3")
        else:
            return pygame.Color("black")

    def position(self, offset = 0):
        x = (self.x * (self.cell_size + self.border_size)) + offset
        y = (self.y * (self.cell_size + self.border_size)) + offset

        return (x, y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color(), pygame.Rect(self.position(), (self.cell_size, self.cell_size)))

    def draw_piece(self, screen, color):
        if color == "RED":
            color = pygame.Color("red")
        elif color == "GREEN":
            color = pygame.Color("green")
        elif color == "YELLOW":
            color = pygame.Color("gold")
        elif color == "BLUE":
            color = pygame.Color("skyblue")

        pygame.draw.circle(screen, color, self.position(self.cell_size / 2), 20)
        pygame.draw.circle(screen, pygame.Color("black"), self.position(self.cell_size / 2), 20, 2)