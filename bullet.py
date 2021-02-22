import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """"A class that handles everything about bullets."""

    def __init__(self, si_settings, screen, ship):
        """"create a bullet at the ships position"""
        super(Bullet, self).__init__()
        self.screen = screen

        # Create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, si_settings.bullet_width, si_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # store the bullet's position as a decimal
        self.y = float(self.rect.y)

        # set color and speed
        self.color = si_settings.bullet_color
        self.speed_factor = si_settings.bullet_speed_factor

    def update(self):
        """"Move bullet on the screen"""
        self.y -= self.speed_factor
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """"draw bullet to screen"""
        pygame.draw.rect(self.screen, self. color, self.rect)
