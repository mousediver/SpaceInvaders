from button import Button
import pygame.font


class TextInputBox(Button):
    """"make a text input box"""

    def __init__(self, si_settings, screen, msg, order):
        super(TextInputBox, self).__init__(si_settings, screen, msg, order)
        self.user_input = 'Please enter your name'

        # set button dimensions and properties
        self.width, self.height = 400, 100
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.prompt_color = (105, 105, 105)
        self.font = pygame.font.SysFont(None, 48)

    def draw_button(self):
        super().draw_button()
