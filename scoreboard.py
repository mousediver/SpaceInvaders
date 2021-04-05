import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """"a class to represent the scoreboard"""

    def __init__(self, si_settings, screen, stats):
        """"initialize score keeping"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.si_settings = si_settings
        self.stats = stats

        # rect for scoreboard background
        self.scoreboard_height = si_settings.scoreboard_height
        self.scoreboard_rect = pygame.Rect(0, 0, si_settings.screen_width, self.scoreboard_height)
        self.scoreboard_bg = si_settings.scoreboard_bg

        # font settings for scoring information
        self.text_color = (0, 0, 200)
        self.font = pygame.font.SysFont(None, 40)

        # prepare initial score image
        self.prep_score()
        self.prep_high_score(stats)
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """"turn score into image"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.scoreboard_bg)

        # Display score at top of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 10

    def prep_high_score(self, stats):
        """"turn score into image"""
        rounded_score = int(round(self.stats.highest_score, -1))
        if stats.new_high_score:
            score_str = 'new high score!'
        elif stats.best_player == '#####':
            score_str = ""
        else:
            score_str = "{:,}".format(rounded_score) + ' by ' + stats.best_player
        self.high_score_image = self.font.render(score_str, True, self.text_color, self.scoreboard_bg)

        # Display score at top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 10

    def prep_level(self):
        """"show current level"""
        lvlstr = "level " + str(self.stats.level)
        self.level_image = self.font.render(lvlstr, True, self.text_color, self.scoreboard_bg)

        # position below score

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom

    def prep_ships(self):
        """"show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.si_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """"show score at screen"""
        self.screen.fill(self.scoreboard_bg, self.scoreboard_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

