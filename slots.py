import pygame
import sys
from random import randint
from settings import Settings
from settings import check_win

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
        self.settings = Settings()
        self.screen = pygame.display.set_mode((
            self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Slot Machine")
        self.background = pygame.image.load('background.png')
        self.background_rect = self.background.get_rect()
        self.background_rect.center = self.screen_rect.center
        self.jackpot = self.settings.jackpot
        self.winnings = self.settings.winnings
        self.bet = self.settings.bet
        self.bet_max = self.settings.bet_max
        self.coins = self.settings.coins
        self.coins_max = self.settings.coins_max
        self.running = False

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                bet_inc_clicked = self.bet_inc_rect.collidepoint(mouse_pos)
                bet_dec_clicked = self.bet_dec_rect.collidepoint(mouse_pos)
                spin_clicked = self.spin_rect.collidepoint(mouse_pos)
                coin_clicked = self.coin_image_rect.collidepoint(mouse_pos)
                if bet_inc_clicked and self.bet < self.bet_max:
                    self.bet += 1
                if bet_dec_clicked and self.bet > 1:
                    self.bet -= 1
                if spin_clicked:
                    self._spin()
                if coin_clicked and self.coins < self.coins_max:
                    self.coins += 10
                    if self.coins > self.coins_max:
                        self.coins = self.coins_max

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.background, self.background_rect)
        self.wheel_left.update()
        self.wheel_middle.update()
        self.wheel_right.update()
        self._update_display()
        pygame.display.flip()

    def _spin(self):
        if self.coins >= self.bet:
            self.coins -= self.bet
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
            check_win(self)

    def _update_display(self):
        self.text_color = self.settings.text_color
        self.text_color_white = self.settings.text_color_white
        self.text_color_yellow = self.settings.text_color_yellow
        self.bg_color = self.settings.bg_color
        self.bg_color_dark = self.settings.bg_color_dark
        self.bg_color_red = self.settings.bg_color_red
        self.font_size_lg = self.settings.text_size_lg
        self.font_size_med = self.settings.text_size_med
        self.font_size_sm = self.settings.text_size_sm

        self.font_lg = pygame.font.SysFont(None, self.font_size_lg)
        self.font_med = pygame.font.SysFont(None, self.font_size_med)
        self.font_sm = pygame.font.SysFont(None, self.font_size_sm)

        bet_str = "Bet: {:,}".format(self.bet)
        self.bet_image = self.font_med.render(
            bet_str, True, self.text_color_white, self.bg_color_dark)
        self.bet_rect = self.bet_image.get_rect()
        self.bet_rect.center = self.screen_rect.center
        self.bet_rect.x = self.bet_rect.x - 205
        self.bet_rect.y = self.bet_rect.y + 206
        self.screen.blit(self.bet_image, self.bet_rect)

        coins_str = "Coins: {:,}".format(self.coins)
        self.coins_image = self.font_med.render(
            coins_str, True, self.text_color_white, self.bg_color_dark)
        self.coins_rect = self.coins_image.get_rect()
        self.coins_rect.center = self.screen_rect.center
        self.coins_rect.x = self.coins_rect.x + 133
        self.coins_rect.y = self.coins_rect.y + 206
        self.screen.blit(self.coins_image, self.coins_rect)

        coins_max_str = "(max {:,})".format(self.coins_max)
        self.coins_max_image = self.font_sm.render(
            coins_max_str, True, self.text_color_white, self.bg_color_dark)
        self.coins_max_rect = self.coins_max_image.get_rect()
        self.coins_max_rect.center = self.screen_rect.center
        self.coins_max_rect.x = self.coins_max_rect.x + 133
        self.coins_max_rect.y = self.coins_max_rect.y + 230
        self.screen.blit(self.coins_max_image, self.coins_max_rect)

        insert_coins_str = "Insert coins to play!   >>>"
        self.insert_coins_image = self.font_med.render(
            insert_coins_str, True, self.text_color_yellow, self.bg_color_dark)
        self.insert_coins_rect = self.insert_coins_image.get_rect()
        self.insert_coins_rect.center = self.screen_rect.center
        self.insert_coins_rect.x = self.insert_coins_rect.x - 100
        self.insert_coins_rect.y = self.insert_coins_rect.y - 15
        self.screen.blit(self.insert_coins_image, self.insert_coins_rect)

        self.coin_image = pygame.image.load("coin.png")
        self.coin_image_rect = self.coin_image.get_rect()
        self.coin_image_rect.center = self.screen_rect.center
        self.coin_image_rect.x = self.coin_image_rect.x + 80
        self.coin_image_rect.y = self.coin_image_rect.y - 15
        self.screen.blit(self.coin_image, self.coin_image_rect)

        bet_max_str = "(max {:,})".format(self.bet_max)
        self.bet_max_image = self.font_sm.render(
            bet_max_str, True, self.text_color_white, self.bg_color_dark)
        self.bet_max_rect = self.bet_max_image.get_rect()
        self.bet_max_rect.center = self.screen_rect.center
        self.bet_max_rect.x = self.bet_max_rect.x - 205
        self.bet_max_rect.y = self.bet_max_rect.y + 230
        self.screen.blit(self.bet_max_image, self.bet_max_rect)

        bet_inc_str = "+"
        self.bet_inc_image = self.font_sm.render(
            bet_inc_str, True, self.text_color_white, self.bg_color_red)
        self.bet_inc_image_rect = self.bet_inc_image.get_rect()
        self.bet_inc_rect = pygame.Rect(0, 0, 20, 20)
        self.bet_inc_rect.center = self.screen_rect.center
        self.bet_inc_rect.x = self.bet_inc_rect.x - 150
        self.bet_inc_rect.y = self.bet_inc_rect.y + 202
        self.screen.fill(self.bg_color_red, self.bet_inc_rect)
        self.bet_inc_image_rect.center = self.bet_inc_rect.center
        self.screen.blit(self.bet_inc_image, self.bet_inc_image_rect)

        bet_dec_str = "-"
        self.bet_dec_image = self.font_sm.render(
            bet_dec_str, True, self.text_color_white, self.bg_color_red)
        self.bet_dec_image_rect = self.bet_dec_image.get_rect()
        self.bet_dec_rect = pygame.Rect(0, 0, 20, 20)
        self.bet_dec_rect.center = self.screen_rect.center
        self.bet_dec_rect.x = self.bet_dec_rect.x - 150
        self.bet_dec_rect.y = self.bet_dec_rect.y + 226
        self.screen.fill(self.bg_color_red, self.bet_dec_rect)
        self.bet_dec_image_rect.center = self.bet_dec_rect.center
        self.screen.blit(self.bet_dec_image, self.bet_dec_image_rect)

        spin_str = "SPIN"
        self.spin_image = self.font_med.render(
            spin_str, True, self.text_color_white, self.bg_color_red)
        self.spin_image_rect = self.spin_image.get_rect()
        self.spin_rect = pygame.Rect(0, 0, 100, 40)
        self.spin_rect.center = self.screen_rect.center
        self.spin_rect.x = self.spin_rect.x - 32
        self.spin_rect.y = self.spin_rect.y + 213
        self.screen.fill(self.bg_color_red, self.spin_rect)
        self.spin_image_rect.center = self.spin_rect.center
        self.screen.blit(self.spin_image, self.spin_image_rect)

        jackpot_str = "Jackpot: {:,}".format(self.jackpot)
        self.jackpot_image = self.font_lg.render(
            jackpot_str, True, self.text_color, self.bg_color)
        # Display the jackpot at the top right of the screen.
        self.jackpot_rect = self.jackpot_image.get_rect()
        self.jackpot_rect.right = self.screen_rect.right - 20
        self.jackpot_rect.top = 20
        self.screen.blit(self.jackpot_image, self.jackpot_rect)

        winnings_str = "Winnings: {:,}".format(self.winnings)
        self.winnings_image = self.font_lg.render(
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
