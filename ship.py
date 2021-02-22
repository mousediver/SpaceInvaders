import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """"A class defining the player's ship."""

    def __init__(self, si_settings, screen):
        """"Initialize the ship and it's starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.si_settings = si_settings

        # Load the ship img and it's rect
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.center = float(self.screen_rect.centerx)
        self.rect.bottom = self.screen_rect.bottom - self.si_settings.ship_height_from_bottom

        # movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """"Updates the position based on the movement flags"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.si_settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.si_settings.ship_speed_factor

        # Update rect object from self.center.
        self.rect.centerx = self.center

    def blitme(self):
        """"Draw the ship at it's current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """"center the ship on screen"""
        self.center = self.screen_rect.centerx
