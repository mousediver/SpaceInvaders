import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """"A class handling aliens"""
    def __init__(self, si_settings, screen):
        """"Initialize the alien in starting position"""
        super(Alien, self).__init__()
        self.screen = screen
        self.si_settings = si_settings

        # Load alien image and set rect
        self.image = pygame.image.load('images/alien1_1.png')
        self.rect = self.image.get_rect()

        # Start each alien near top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store alien's position
        self.x = float(self.rect.x)

    def update(self, si_settings):
        """"move the alien"""
        self.rect.x += (self.si_settings.alien_speedfactor_x * si_settings.fleet_direction)
        self.x = self.rect.x

    def blitme(self):
        """"Draw alien to location"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """"check if fleet is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= screen_rect.left:
            return True

# TODO: change alien sprite during movement and when new level
