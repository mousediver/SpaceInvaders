import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
import random
from alien_bullet import AlienBullet


def check_keydown_events(event, si_settings, screen, ship, bullets, stats, scoreboard):
    """"respond to key presses."""
    if event.key == pygame.K_q:
        sys.exit()
    if event.key == pygame.K_RETURN and stats.game_active is False:
        press_play(si_settings, stats, scoreboard)
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE and stats.game_active:
        fire_bullet(si_settings, screen, ship, bullets)


def check_keyup_events(event, ship):
    """"respond to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(si_settings, screen, ship, bullets, stats, play_button, scoreboard):
    """"Watch for keyboard and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, si_settings, screen, ship, bullets, stats, scoreboard)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, si_settings, scoreboard)


def reset_game(stats):
    """"resets the game"""
    stats.reset_stats()


def check_play_button(stats, play_button, mouse_x, mouse_y, si_settings, scoreboard):
    """"check if play button is pressed"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        press_play(si_settings, stats, scoreboard)


def press_play(si_settings, stats, scoreboard):
    """"starts the game"""
    reset_game(stats)
    stats.game_active = True
    si_settings.initialize_dynamic_settings()
    set_mouse_visibility(si_settings)

    # reset scoreboard images
    scoreboard.prep_score()
    scoreboard.prep_high_score()
    scoreboard.prep_level()
    scoreboard.prep_ships()


def set_mouse_visibility(si_settings):
    si_settings.mouse_visible = not si_settings.mouse_visible
    pygame.mouse.set_visible(si_settings.mouse_visible)


def update_screen(si_settings, screen, ship, aliens, bullets, stars, alien_bullets, play_button, stats, scoreboard):
    """"Update images on the screen and flip to new screen"""
    # redraw the screen during each pass through the loop.
    screen.fill(si_settings.bg_color)
    for star in stars:
        pygame.draw.circle(screen, si_settings.star_color, star, si_settings.star_width)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for alien_bullet in alien_bullets.sprites():
        alien_bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # draw the scoreboard
    scoreboard.show_score()

    # draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # Make most recent screen visible
    pygame.display.flip()


def update_bullets(si_settings, screen, ship, aliens, bullets, stats, scoreboard):
    """"Update bullets on screen."""
    bullets.update()

    # delete old bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_collisions(aliens, bullets, stats, si_settings, scoreboard)
    if len(aliens) == 0:
        # Destroy existing bullets and create a new fleet
        bullets.empty()
        si_settings.increase_difficulty()
        create_fleet(si_settings, screen, ship, aliens)

        # increase level
        stats.level += 1
        scoreboard.prep_level()


def check_bullet_collisions(aliens, bullets, stats, si_settings, scoreboard):
    """"respond to bullet-alien collisions"""
    # Remove any bullets and aliens that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += si_settings.alien_points * len(aliens)
            scoreboard.prep_score()
            check_high_score(stats, scoreboard)


def check_alien_bullet_collisions(ship, alien_bullets):
    """"check if alien bullet hits ship"""
    # remove the bullets
    hit = pygame.sprite.spritecollideany(ship, alien_bullets, collided=None)
    if hit is None:
        return False
    else:
        return True


def fire_bullet(si_settings, screen, ship, bullets):
    """"fire a bullet."""
    if len(bullets) < si_settings.bullets_allowed:
        new_bullet = Bullet(si_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(si_settings, alien_width):
    """"Calculate the number of aliens in a row"""
    if si_settings.classic_rules:
        number_aliens_x = 11
        return number_aliens_x
    else:
        # Create an alien and find out the max number of aliens on a row.
        available_space_x = (si_settings.fleet_max_width - 2 * alien_width)
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x


def get_number_rows(si_settings, alien_height, ship_height):
    """"Calculate the number of rows"""
    if si_settings.classic_rules:
        number_rows = 5
        return number_rows
    else:
        available_space_y = (si_settings.fleet_max_height - (3 * alien_height) - ship_height)
        number_rows = int(available_space_y / (2 * alien_height))
        return number_rows


def create_alien(si_settings, screen, aliens, alien_number, row_number):
    """"Create an alien and place it in the row"""
    alien = Alien(si_settings, screen)
    alien_width = alien.rect.width
    alien_x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien_x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(si_settings, screen, ship, aliens):
    """"Create a fleet of aliens."""
    alien = Alien(si_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    ship_height = ship.rect.height

    number_aliens_x = get_number_aliens_x(si_settings, alien_width)
    number_rows = get_number_rows(si_settings, alien_height, ship_height)

    # Create fleet
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(si_settings, screen, aliens, alien_number, row_number)


def ship_hit(si_settings, stats, screen, ship, aliens, bullets, alien_bullets, scoreboard):
    """"respond to ship being hit"""
    if stats.ships_left > 0:
        # decrement ships_left
        stats.ships_left -= 1

        scoreboard.prep_ships()

        # empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        alien_bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(si_settings, screen, ship, aliens)
        ship.center_ship()

        # pause
        sleep(0.5)

    else:
        stats.game_active = False
        check_lowest_high_score(stats)
        set_mouse_visibility(si_settings)


def update_aliens(aliens, si_settings, ship, stats, screen, bullets, alien_bullets, scoreboard):
    """"check is fleet is at edges and update aliens"""
    check_fleet_edges(si_settings, aliens)
    aliens.update(si_settings)

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(si_settings, stats, screen, ship, aliens, bullets, alien_bullets, scoreboard)

    check_aliens_bottom(si_settings, stats, screen, ship, aliens, bullets, alien_bullets, scoreboard)


def get_star_cols(si_settings):
    """"determine how many columns"""
    star_cols = si_settings.screen_width / si_settings.star_spacing
    star_cols = int(star_cols)
    return star_cols


def get_star_rows(si_settings):
    """"determine how many rows"""
    star_rows = si_settings.screen_height / si_settings.star_spacing
    star_rows = int(star_rows)
    return star_rows


def create_star(si_settings, star_col, star_row, stars):
    """"create stars for background"""
    random_pos = random.randint(si_settings.star_rand_min, si_settings.star_rand_max)
    star_pos_x = (si_settings.star_spacing * star_col) + (si_settings.star_spacing / 2) + random_pos
    star_pos_y = (si_settings.star_spacing * star_row) + (si_settings.star_spacing / 2) + random_pos
    star_pos_x = int(star_pos_x)
    star_pos_y = int(star_pos_y)
    star_pos = [star_pos_x, star_pos_y]
    stars.append(star_pos)


def star_field(si_settings, stars):
    """"make a grid of stars"""
    star_cols = (get_star_cols(si_settings))
    star_rows = (get_star_rows(si_settings))

    for star_col in range(star_cols):
        for star_row in range(star_rows):
            create_star(si_settings, star_col, star_row, stars)


def check_fleet_edges(si_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(si_settings, aliens)
            break


def change_fleet_direction(si_settings, aliens):
    """"Drop the entire fleet and change the direction."""
    for alien in aliens.sprites():
        alien.rect.y += si_settings.alien_speedfactor_y
    si_settings.fleet_direction *= -1


def frame_counter(frame_number):
    """"Counting frame numbers"""
    frame_number += 1
    return frame_number


def select_firing_alien(aliens):
    """Select a random alien"""
    selected_alien = random.choice(aliens.sprites())
    return selected_alien


def fire_alien_bullet(si_settings, aliens, alien_bullets, screen):
    """"Fire a bullet from a random alien once every couple of hundred frames"""
    # set firing time
    random_fire = random.randint(-si_settings.alien_firing_spread, si_settings.alien_firing_spread)
    time_to_next_bullet = si_settings.alien_firing_rate + random_fire

    if len(alien_bullets) < si_settings.alien_bullets_allowed and len(aliens) > 0:
        alien = select_firing_alien(aliens)
        new_alien_bullet = AlienBullet(si_settings, screen, alien)
        alien_bullets.add(new_alien_bullet)

    return time_to_next_bullet


def update_alien_bullets(alien_bullets, si_settings, ship, stats, screen, aliens, bullets, scoreboard):
    """"update alien bullets"""
    alien_bullets.update()
    for alien_bullet in alien_bullets.copy():
        if alien_bullet.rect.top >= si_settings.screen_height:
            alien_bullets.remove(alien_bullet)

    hit = check_alien_bullet_collisions(ship, alien_bullets)
    if hit:
        ship_hit(si_settings, stats, screen, ship, aliens, bullets, alien_bullets, scoreboard)


def check_aliens_bottom(si_settings, stats, screen, ship, aliens, bullets, alien_bullets, scoreboard):
    """"check if any aliens have reached the bottom"""
    for alien in aliens.sprites():
        if alien.rect.bottom >= ship.rect.top:
            # treat as if ship got hit
            ship_hit(si_settings, stats, screen, ship, aliens, bullets, alien_bullets, scoreboard)
            break


def check_high_score(stats, scoreboard):
    """"check if score is new high score"""
    if stats.score > stats.highest_score:
        stats.highest_score = stats.score
        scoreboard.prep_high_score()


def check_lowest_high_score(stats):
    """"check if score is higher than lowest high score"""
    if stats.score > stats.lowest_high_score:
        stats.update_highscores()
