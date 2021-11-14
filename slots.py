import pygame
import sys
from random import randint

symbols = ["bar.png", "barbar.png", "barbarbar.png", "seven.png", "lemon.png",
           "melon.png", "grape.png", "orange.png", "banana.png", "cherry.png"]


class Wheel:
    def __init__(self, slots):
        self.value = 3
        self.image = pygame.image.load(symbols[self.value])
        self.rect = self.image.get_rect()
        self.screen = slots.screen
        self.spinning = False

    def update(self):
        if self.spinning == True:
            self.spin()
        self.screen.blit(self.image, self.rect)

    def spin(self):
        """Spin the wheels"""
        self.value = randint(0, 9)
        self.image = pygame.image.load(symbols[self.value])


class SlotMachine:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Slot Machine")
        self.background = pygame.image.load('background.png')
        self.background_rect = self.background.get_rect()
        self.background_rect.center = self.screen_rect.center
        self.jackpot = 1000
        self.winnings = 0
        self.bet = 1

        self.wheel_left = Wheel(self)
        self.wheel_middle = Wheel(self)
        self.wheel_right = Wheel(self)

        self.wheel_left_rect = self.wheel_left.rect
        self.wheel_left_rect.center = self.screen_rect.center
        self.wheel_left_rect.x = self.wheel_left_rect.x - 197
        self.wheel_left_rect.y = self.wheel_left_rect.y + 100

        self.wheel_middle_rect = self.wheel_middle.rect
        self.wheel_middle_rect.center = self.screen_rect.center
        self.wheel_middle_rect.x = self.wheel_middle_rect.x - 32
        self.wheel_middle_rect.y = self.wheel_middle_rect.y + 100

        self.wheel_right_rect = self.wheel_right.rect
        self.wheel_right_rect.center = self.screen_rect.center
        self.wheel_right_rect.x = self.wheel_right_rect.x + 133
        self.wheel_right_rect.y = self.wheel_right_rect.y + 100

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mouse.set_visible(True)
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                """Respond to keydown presses."""
                if event.key == pygame.K_SPACE:
                    self._spin()
                if event.key == pygame.K_LEFT:
                    self.wheel_left.spinning = True
                    self.wheel_middle.spinning = True
                    self.wheel_right.spinning = True
                if event.key == pygame.K_RIGHT:
                    self.wheel_left.spinning = False
                    self.wheel_middle.spinning = False
                    self.wheel_right.spinning = False
            # elif event.type == pygame.KEYUP:
            #     if event.key == pygame.K_LEFT:
            #         self.wheel_left.spinning = False

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, self.background_rect)
        self.wheel_left.update()
        self.wheel_middle.update()
        self.wheel_right.update()
        self._update_display()
        pygame.display.flip()

    def _spin(self):
        self.jackpot += self.bet
        self.wheel_left.spinning = True
        self.wheel_middle.spinning = True
        self.wheel_right.spinning = True
        for i in range(301):
            if i > 100:
                self.wheel_left.spinning = False
            if i > 200:
                self.wheel_middle.spinning = False
            if i == 300:
                self.wheel_right.spinning = False
            self.wheel_left.update()
            self.wheel_middle.update()
            self.wheel_right.update()
            pygame.display.flip()
        self._check_win()

    def _check_win(self):
        # Wheel keys are:
        # 0 - bar
        # 1 - barbar
        # 2 - barbarbar
        # 3 - seven
        # 4 - lemon
        # 5 - melon
        # 6 - grape
        # 7 - orange
        # 8 - banana
        # 9 - cherry
        if self.wheel_left.value == self.wheel_middle.value and self.wheel_left.value == self.wheel_right.value:
            self.winnings += ((self.wheel_left.value + 1) * 10)
        if self.wheel_left.value == 0 or self.wheel_left.value == 1 or self.wheel_left.value == 2:
            if self.wheel_middle.value == 0 or self.wheel_middle.value == 1 or self.wheel_middle.value == 2:
                if self.wheel_right.value == 0 or self.wheel_right.value == 1 or self.wheel_right.value == 2:
                    self.winnings += (((self.wheel_left.value + 1) + (
                        self.wheel_middle.value + 1) + (self.wheel_right.value + 1)) * 10)
        if self.wheel_left.value == 3 and self.wheel_middle.value == 3 and self.wheel_right.value == 3:
            self.winnings += self.jackpot
            self.jackpot = 1000

    def _update_display(self):
        self.text_color = (30, 30, 30)
        self.bg_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        jackpot_str = "Jackpot = {:,}".format(self.jackpot)
        self.jackpot_image = self.font.render(
            jackpot_str, True, self.text_color, self.bg_color)
        # Display the jackpot at the top right of the screen.
        self.jackpot_rect = self.jackpot_image.get_rect()
        self.jackpot_rect.right = self.screen_rect.right - 20
        self.jackpot_rect.top = 20
        self.screen.blit(self.jackpot_image, self.jackpot_rect)

        winnings_str = "Winnings = {:,}".format(self.winnings)
        self.winnings_image = self.font.render(
            winnings_str, True, self.text_color, self.bg_color)
        # Display the winnings at the top left of the screen.
        self.winnings_rect = self.winnings_image.get_rect()
        self.winnings_rect.left = self.screen_rect.left + 20
        self.winnings_rect.top = 20
        self.screen.blit(self.winnings_image, self.winnings_rect)


if __name__ == '__main__':
    # Make a game instance, and run the game.
    slots = SlotMachine()
    slots.run_game()
