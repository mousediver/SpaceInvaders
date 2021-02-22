import pygame
from pygame.sprite import Sprite


class AlienBullet(Sprite):
    """"A class that handles everything about bullets."""

    def __init__(self, si_settings, screen, alien):
        """"create a bullet at the ships position"""
        super(AlienBullet, self).__init__()
        self.screen = screen

        # Create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, si_settings.alien_bullet_width, si_settings.alien_bullet_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom

        # store the bullet's position as a decimal
        self.y = float(self.rect.y)

        # set color and speed
        self.color = si_settings.alien_bullet_color
        self.speed_factor = si_settings.alien_bullet_speed_factor

    def update(self):
        """"Move bullet on the screen"""
        self.y -= self.speed_factor
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """"draw bullet to screen"""
        pygame.draw.rect(self.screen, self. color, self.rect)
