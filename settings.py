class Settings:
    """"A class to store all settings for Space Invaders."""

    def __init__(self):
        """"Initialize the game settings."""
        # STATIC SETTINGS

        # classic rules
        self.classic_rules = False

        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        self.mouse_visible = True
        self.max_frames_sec = 120

        # star settings
        self.star_color = (255, 255, 255)
        self.star_width = 1
        self.star_spacing = 30
        self.star_rand_min = -20
        self.star_rand_max = 20

        # ship settings
        self.ship_height_from_bottom = 50
        self.ship_limit = 3

        # bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 5

        # Alien settings
        self.alien_in_row = 11
        self.alien_total_rows = 5
        self.fleet_max_width = int(self.screen_width * (2 / 3))
        self.fleet_max_height = int(self.screen_height / 2)
        self.alien_speedfactor_y = 10

        # alien bullet settings
        self.alien_bullet_speed_factor = -3
        self.alien_bullet_width = 1200
        self.alien_bullet_height = 15
        self.alien_bullet_color = (0, 255, 0)
        self.alien_bullets_allowed = 5
        self.alien_firing_rate = 600
        self.alien_firing_spread = 300

        # DYNAMIC SETTINGS
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """"initialize dynamic settings"""
        self.ship_speed_factor = 5
        self.bullet_speed_factor = 7
        self.alien_speedfactor_x = 3
        self.fleet_direction = 1
        self.alien_points = 10

    def increase_difficulty(self):
        """"increase the speed if won"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speedfactor_x *= self.speedup_scale
        self.alien_points *= 2

# TODO: make changing settings available
