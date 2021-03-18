import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from pygame.time import Clock
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    """Initialize game and create a screen object."""
    pygame.init()
    si_settings = Settings()
    screen = pygame.display.set_mode((si_settings.screen_width, si_settings.screen_height))
    pygame.display.set_caption("Space invaders")
    frame_number = 0
    time_to_next_bullet = 100
    stats = GameStats(si_settings)
    clock = Clock()
    scoreboard = Scoreboard(si_settings, screen, stats)

    # make the play button
    play_button = Button(si_settings, screen, "Play")

    # Make a ship, bullets and aliens
    ship = Ship(si_settings, screen)
    bullets = Group()
    aliens = Group()
    alien_bullets = Group()

    # calculate star positions
    stars = []
    gf.star_field(si_settings, stars)
    gf.create_fleet(si_settings, screen, ship, aliens)

    #load high scores
    stats.load_highscore()

    # Start mainloop for the game.
    while True:
        gf.check_events(si_settings, screen, ship, bullets, stats, play_button, scoreboard)

        if stats.game_active:
            frame_number = gf.frame_counter(frame_number)
            ship.update()
            gf.update_bullets(si_settings, screen, ship, aliens, bullets, stats, scoreboard)
            gf.update_aliens(aliens, si_settings, ship, stats, screen, bullets, alien_bullets, scoreboard)
            if frame_number == time_to_next_bullet:
                time_to_next_bullet = gf.fire_alien_bullet(si_settings, aliens, alien_bullets, screen)
                frame_number = 0
            gf.update_alien_bullets(alien_bullets, si_settings, ship, stats, screen, aliens, bullets, scoreboard)
        gf.update_screen(
            si_settings, screen, ship, aliens, bullets, stars, alien_bullets, play_button, stats, scoreboard
        )
        clock.tick(si_settings.max_frames_sec)


run_game()

# TODO: make bunkers
# TODO: add sound
# TODO: fix initial 4 ship bug