class Settings:

    def __init__(self):
        # text attributes
        self.text_color = (25, 25, 25)
        self.text_color_white = (255, 255, 255)
        self.text_color_yellow = (255, 255, 0)
        self.text_size_lg = 48
        self.text_size_med = 36
        self.text_size_sm = 24

        # background colors
        self.bg_color = (255, 255, 255)
        self.bg_color_dark = (60, 60, 60)
        self.bg_color_red = (232, 62, 51)

        # screen dimensions
        self.screen_width = 800
        self.screen_height = 600

        # gambling settings
        self.jackpot = 1000
        self.bet = 1
        self.bet_max = 3
        self.winnings = 0
        self.coins = 0
        self.coins_max = 30


def check_win(self):
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
        self.winnings += ((self.wheel_left.value + 1) * 10) * self.bet
    elif self.wheel_left.value == 0 or self.wheel_left.value == 1 or self.wheel_left.value == 2:
        if self.wheel_middle.value == 0 or self.wheel_middle.value == 1 or self.wheel_middle.value == 2:
            if self.wheel_right.value == 0 or self.wheel_right.value == 1 or self.wheel_right.value == 2:
                self.winnings += (((self.wheel_left.value + 1) + (
                    self.wheel_middle.value + 1) + (self.wheel_right.value + 1)) * 10) * self.bet
            else:
                self.jackpot += self.bet * 10
        else:
            self.jackpot += self.bet * 10
    elif self.wheel_left.value == 3 and self.wheel_middle.value == 3 and self.wheel_right.value == 3:
        self.winnings += self.jackpot * self.bet
        self.jackpot = 1000
    else:
        self.jackpot += self.bet * 10

    # Update gambling values based on wins
    self.bet_max = max(self.bet_max, int(self.winnings / 100))
    self.coins_max = max(self.coins_max, int(self.winnings / 10))
