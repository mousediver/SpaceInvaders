import json
from operator import itemgetter


class GameStats:
    """"track stats for the game"""

    def __init__(self, si_settings):
        """"initialize stats"""
        self.si_settings = si_settings
        self.reset_stats()
        # start the game in inactive state
        self.highest_score = 0
        self.lowest_high_score = 0
        self.high_scores = []

        # states
        self.game_active = False
        self.main_menu_active = True
        self.high_score_screen = False
        self.settings_menu = False
        self.credits_screen = False

    def reset_stats(self):
        """"initialize stats that can change during the game"""
        self.ships_left = self.si_settings.ship_limit
        self.score = 0
        self.level = 1

    def load_highscore(self):
        """"load the highscores into the game"""
        try:
            with open('highscores.txt', 'r') as f:
                highscores = json.load(f)

        except FileNotFoundError:
            # set default values if file is not found
            highscores = [
                ('#####', 0),
                ('#####', 0),
                ('#####', 0),
                ('#####', 0),
                ('#####', 0)
                ]

        self.highest_score = highscores[0][1]
        self.lowest_high_score = highscores[4][1]
        self.high_scores = highscores

    def update_highscores(self):
        """"update the highscore file"""
        player_name = input("What is your name? ")
        player_score = self.score
        high_scores = self.high_scores

        high_scores.append((player_name, player_score))
        high_scores = sorted(high_scores, key=itemgetter(1), reverse=True)[:5]

        with open('highscores.txt', 'w') as f:
            json.dump(high_scores, f)



# TODO: make highscore input in GUI
