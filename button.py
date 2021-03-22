import pygame.font


class Button:
    """"creates a button"""

    def __init__(self, si_settings, screen, msg, order):
        """"initialize button attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # set button dimensions and properties
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self. screen_rect.centerx
        self.rect.top = self.screen_rect.centery + (order * si_settings.button_spacing)

        # prep button message
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """"turn msg into button in center of screen"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
