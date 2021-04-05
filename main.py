import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from pygame.time import Clock
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from text_input_box import TextInputBox


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

    # make the menu buttons
    play_button = Button(si_settings, screen, "Play", 1)
    high_scores_button = Button(si_settings, screen, "High scores", 2)
    settings_button = Button(si_settings, screen, "Settings", 3)
    credits_button = Button(si_settings, screen, "Credits", 4)
    main_menu_button = Button(si_settings, screen, "Main menu", 1)

    # make the text input box
    high_score_input = TextInputBox(si_settings, screen, "new high score", 5)


    # Make a ship, bullets and aliens
    ship = Ship(si_settings, screen)
    ship.center_ship()
    ship.update()
    bullets = Group()
    aliens = Group()
    alien_bullets = Group()

    # calculate star positions
    stars = []
    gf.star_field(si_settings, stars)
    gf.create_fleet(si_settings, screen, ship, aliens)

    # load high scores
    stats.load_highscore()
    scoreboard.prep_high_score(stats)

    # Start mainloop for the game.
    while True:
        gf.check_events(
            si_settings, screen, ship, aliens, bullets, alien_bullets, stats, play_button, scoreboard,
            high_scores_button, main_menu_button, settings_button, credits_button, high_score_input
            )

        if stats.game_active:
            frame_number = gf.frame_counter(frame_number)
            ship.update()
            gf.update_bullets(si_settings, screen, ship, aliens, bullets, stats, scoreboard)
            gf.update_aliens(
                aliens, si_settings, ship, stats, screen, bullets, alien_bullets, scoreboard, high_score_input
                )
            if frame_number == time_to_next_bullet:
                time_to_next_bullet = gf.fire_alien_bullet(si_settings, aliens, alien_bullets, screen)
                frame_number = 0
            gf.update_alien_bullets(
                alien_bullets, si_settings, ship, stats, screen, aliens, bullets, scoreboard, high_score_input
                )
        gf.update_display(
                si_settings, screen, ship, aliens, bullets, stars, alien_bullets, play_button, stats, scoreboard,
                high_scores_button, settings_button, credits_button, main_menu_button
        )
        clock.tick(si_settings.max_frames_sec)


run_game()


# TODO: add sound

