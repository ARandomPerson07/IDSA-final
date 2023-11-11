import pygame
from components.colors import *


def get_hover_gridsquare(mouse_pos, rows, width):
    gap = width//rows
    y, x = mouse_pos

    row = y//gap
    col = x//gap

    return (row, col)


pygame.font.init()
font = pygame.font.SysFont(None, 28)


class ToggleButton:
    def __init__(self, x, y, width, height, text="I AM A BUTTON!", alt_text="I am pressed",  initial_state=False):
        self.color = GREY
        self.rect = pygame.Rect(x, y, width, height)
        self.state = initial_state
        self.text = text
        self.alt_text = alt_text
        self.display_text = self.text
        self.text_surf = font.render(self.display_text, True, BLACK)

    def draw(self, win):
        self.color = GREEN if self.state else RED
        pygame.draw.rect(win, self.color, self.rect)
        text_size = self.text_surf.get_size()

        # Calculate position to center the text
        text_x = self.rect.x + (self.rect.width - text_size[0]) // 2
        text_y = self.rect.y + (self.rect.height - text_size[1]) // 2

        # Blit the text surface onto the screen
        win.blit(self.text_surf, (text_x, text_y))

    def change_state(self):
        self.state = not self.state

        if self.state:
            self.display_text = self.alt_text
        else:
            self.display_text = self.text

        self.text_surf = font.render(self.display_text, True, BLACK)

    def get_rect(self):
        return self.rect

    def get_state(self):
        return self.state


class TextBox:
    def __init__(self, x, y, width, height, text="This is placeholder"):
        self.bg_color = GREY
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont(None, 24)
        self.text_surfs = self.wrap_text()

    def wrap_text(self):
        lines = [line.split(' ')
                 for line in self.text.splitlines()]
        space = self.font.size(' ')[0]  # The width of a space.
        max_width, max_height = self.rect.size
        max_width -= 20  # buffer
        max_height -= 10  # buffer
        surfaces = []
        x, y = 0, 0
        for line in lines:
            for word in line:
                word_surface = self.font.render(word, True, BLACK)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    y += word_height  # start new line
                    x = 0  # reset x
                surfaces.append((word_surface, (x, y)))
                x += word_width + space
            y += word_height  # start new line
            x = 0
        return surfaces

    def draw(self, win):
        pygame.draw.rect(win, self.bg_color, self.rect)
        for surf, pos in self.text_surfs:
            # Adjust the y-coordinate for the surface based on the rect y position and the line height
            win.blit(
                surf, (self.rect.x + pos[0] + 10, self.rect.y + pos[1] + 5))

    def set_text(self, newtext: str):
        self.text = newtext
        self.text_surfs = self.wrap_text()
