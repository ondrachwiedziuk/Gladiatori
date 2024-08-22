import pygame
from time import time

from database import Database

RESOlUTION = (800, 600)
# Sand color
BACKGROUND_COLOR = (246,215,176)
# Wooden color
BAR_COLOR = (64, 35, 8)
# Dark red
BUTTON_COLOR = (120,6,6)
GREEN_BUTTON_COLOR = (79, 121, 66)

# Lighter red
BUTTON_HOVER_COLOR = (178, 34, 34)
GREEN_BUTTON_HOVER_COLOR = (34, 139, 34)
# Text silver color
TEXT_COLOR = (229,228,226)
# Black title color
TITLE_COLOR = (0, 0, 0)
SIZE_BUTTON = (300, 50)
SIZE_BUTTON_SMALL = (150, 50)
SIZE_BUTTON_WIDE = (450, 50)
FONT = "data/latin-modern-mono-regular.otf"

class Button:
    def __init__(self, text, location, size, action=None, color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, text_color=TEXT_COLOR, font_size=25, allign='center', secondary_action=None, secondary_action_args=None):
        self.text = text
        self.location = location
        self.size = size
        self.font = pygame.font.Font(FONT, font_size)
        self.color = color
        self.hover_color = hover_color
        self.rect = pygame.Rect(location, size)
        self.text_color = text_color
        self.hover = False
        self.action = action
        self.allign = allign
        self.secondary_action = secondary_action
        self.secondary_action_args = secondary_action_args

    def draw(self, screen):
        if self.hover:
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text = self.font.render(self.text, True, self.text_color)
        if self.allign == 'center':
            text_rect = text.get_rect(center=self.rect.center)
        elif self.allign == 'left':
            text_rect = text.get_rect(left=self.rect.left + 10, centery=self.rect.centery)
        elif self.allign == 'right':
            text_rect = text.get_rect(right=self.rect.right - 10, centery=self.rect.centery)

        screen.blit(text, text_rect)

    def is_hover(self, pos):
        if self.rect.collidepoint(pos):
            self.hover = True
        else:
            self.hover = False

    def click(self):
        if self.secondary_action is not None:
            self.secondary_action(*self.secondary_action_args)

        if self.action is not None:
            return self.action
        return True

class ImageButton:
    def __init__(self, image_path, location, size, action=None, color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, allign='center', secondary_action=None, secondary_action_args=None):
        self.image_path = image_path
        self.location = location
        self.size = size
        self.rect = pygame.Rect(location, size)
        self.color = color
        self.hover = False
        self.hover_color = hover_color
        self.action = action
        self.allign = allign
        self.secondary_action = secondary_action
        self.secondary_action_args = secondary_action_args

    def draw(self, screen):
        if self.hover:
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        image = pygame.image.load(self.image_path)
        # Resize image with keeping aspect ratio
        image = pygame.transform.scale(image, (self.size[1] - 10, self.size[1] - 10))
        image_rect = image.get_rect(center=self.rect.center)
        screen.blit(image, image_rect)

    def is_hover(self, pos):
        if self.rect.collidepoint(pos):
            self.hover = True
        else:
            self.hover = False
        
    def click(self):
        if self.secondary_action is not None:
            self.secondary_action(*self.secondary_action_args)

        if self.action is not None:
            return self.action
        return True


class Menu:
    def __init__(self, screen, status_bar, current_window, title="Gladiátorská aréna"):
        self.buttons = []
        self.running = True
        self.screen = screen
        self.title = title
        self.status_bar = status_bar
        self.current_window = current_window

    def add_button(self, button):
        self.buttons.append(button)

    def run(self):
        while self.running is True:
            if self.status_bar.refresh == 2:
                self.running = self.current_window
                self.status_bar.refresh = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEMOTION:
                    for button in self.buttons:
                        button.is_hover(pygame.mouse.get_pos())
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.hover:
                            self.running = button.click()
            self.screen.fill(BACKGROUND_COLOR)
            title_font = pygame.font.Font(FONT, 60)
            title = title_font.render(self.title, True, TITLE_COLOR)
            title_rect = title.get_rect(center=(RESOlUTION[0] // 2, 100))
            self.screen.blit(title, title_rect)

            for button in self.buttons:
                button.draw(self.screen)
            self.status_bar.draw()
            pygame.display.flip()
        
        return self.running
    

class StatusBar:
    def __init__(self, screen, admin=False):
        # Location at the top of the screen
        # Shows time at the left side and three money types at the right side (ONLY PLAYERS)
        self.screen = screen
        self.size = (RESOlUTION[0], 50)
        self.font = pygame.font.Font(FONT, 25)
        self.admin = admin
        self.location = (0, 0)
        self.current_time = time()
        self.remaining_time = 0
        self.golden_coins = 0
        self.silver_coins = 0
        self.bronze_coins = 0
        self.refresh_time = 1
        self.status = 'N'
        self.team_id = None
        self.tasks = [None, None, None]
        self.refresh = 0

    def update(self, forced=False):
        if self.status == 'R':
            if self.current_time + self.refresh_time < time() and forced is False:
                # Time
                session = Database("gladiatori_time", "Watcher", "localhost", 3306, "gladiatori")
                session.connect()
                self.current_time = time()
                end_time = session.get_end_time()
                self.remaining_time = round(end_time - self.current_time)
                if self.remaining_time < 0:
                    self.remaining_time = 0
                if self.admin is False:
                    # Coins
                    self.golden_coins = session.get_golden_coins(self.team_id)
                    self.silver_coins = session.get_silver_coins(self.team_id)
                    self.bronze_coins = session.get_bronze_coins(self.team_id)
                    # Tasks
                    self.tasks = session.get_tasks(self.team_id)
                    if self.tasks is None:
                        self.tasks = [None, None, None]
                    while len(self.tasks) < 3:
                        self.tasks.append(None)
                if self.refresh == 1:
                    self.refresh = 2
                session.disconnect()
        elif self.status == 'E':
            self.remaining_time = 0


    def draw(self):
        self.update()
        pygame.draw.rect(self.screen, BAR_COLOR, (self.location, self.size))
        # Add time symbol
        time_symbol = pygame.image.load("data/time.png")
        time_symbol = pygame.transform.scale(time_symbol, (30, 30))
        time_rect = time_symbol.get_rect(center=(self.size[0] // 8 - 60, self.size[1] // 2))
        self.screen.blit(time_symbol, time_rect)
        # Time is in seconds, make it human readable
        time_text = self.font.render(f"{self.remaining_time // 60}:{self.remaining_time % 60}", True, TEXT_COLOR)
        # center in in the quarter box
        time_rect = time_text.get_rect(center=(self.size[0] // 8, self.size[1] // 2))
        self.screen.blit(time_text, time_rect)
        if self.admin is False:
            # Load symbols of coins
            golden_coins_symbol = pygame.image.load("data/golden_coins.png")
            golden_coins_symbol = pygame.transform.scale(golden_coins_symbol, (30, 30))
            golden_coins_rect = golden_coins_symbol.get_rect(center=(3 * self.size[0] // 8 - 60, self.size[1] // 2))
            self.screen.blit(golden_coins_symbol, golden_coins_rect)
            silver_coins_symbol = pygame.image.load("data/silver_coins.png")
            silver_coins_symbol = pygame.transform.scale(silver_coins_symbol, (30, 30))
            silver_coins_rect = silver_coins_symbol.get_rect(center=(5 * self.size[0] // 8 - 60, self.size[1] // 2))
            self.screen.blit(silver_coins_symbol, silver_coins_rect)
            bronze_coins_symbol = pygame.image.load("data/bronze_coins.png")
            bronze_coins_symbol = pygame.transform.scale(bronze_coins_symbol, (30, 30))
            bronze_coins_rect = bronze_coins_symbol.get_rect(center=(7 * self.size[0] // 8 - 60, self.size[1] // 2))
            self.screen.blit(bronze_coins_symbol, bronze_coins_rect)
            # Draw text
            golden_coins_text = self.font.render(f'{self.golden_coins}', True, TEXT_COLOR)
            golden_coins_rect = golden_coins_text.get_rect(center=(3 * self.size[0] // 8, self.size[1] // 2))
            self.screen.blit(golden_coins_text, golden_coins_rect)
            silver_coins_text = self.font.render(f'{self.silver_coins}', True, TEXT_COLOR)
            silver_coins_rect = silver_coins_text.get_rect(center=(5 * self.size[0] // 8, self.size[1] // 2))
            self.screen.blit(silver_coins_text, silver_coins_rect)
            bronze_coins_text = self.font.render(f'{self.bronze_coins}', True, TEXT_COLOR)
            bronze_coins_rect = bronze_coins_text.get_rect(center=(7 * self.size[0] // 8, self.size[1] // 2))
            self.screen.blit(bronze_coins_text, bronze_coins_rect)


class Card:
    size = (100, 120)


class SlaveCard(Card):
    def __init__(self, slave, location):
        self.slave = slave
        self.location = location


    def click(self, context):
        if context == 'mine':
            pass
        elif context == 'buy':
            pass
        elif context == 'sell':
            pass
        elif context == 'select':
            pass


def loop(init_process=None, admin=False):
    current_process = init_process
    pygame.init()
    screen = pygame.display.set_mode(RESOlUTION)
    status_bar = StatusBar(screen, admin)
    session = Database("gladiatori_time", "Watcher", "localhost", 3306, "gladiatori")
    session.connect()
    if session.is_game_running():
        status_bar.status = 'R'
    
    while current_process is not None:
        try:
            current_process = current_process(screen, status_bar)
        except TypeError:
            current_process = None
    pygame.quit()