class GameStats:
    """"track stats for the game"""

    def __init__(self, si_settings):
        """"initialize stats"""
        self.si_settings = si_settings
        self.reset_stats()
        # start the game in inactive state
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        """"initialize stats that can change during the game"""
        self.ships_left = self.si_settings.ship_limit
        self.score = 0
        self.level = 1

# TODO: save highscores to file with names
