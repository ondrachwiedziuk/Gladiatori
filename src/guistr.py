import pygame
from time import time

from database import Database

RESOlUTION = (800, 600)
# Sand color
BACKGROUND_COLOR = (246,215,176)
# Wooden color
BAR_COLOR = (188,106,60)
# Dark red
BUTTON_COLOR = (120,6,6)
# Lighter red
BUTTON_HOVER_COLOR = (178, 34, 34)
# Text silver color
TEXT_COLOR = (229,228,226)
# Black title color
TITLE_COLOR = (0, 0, 0)
SIZE_BUTTON = (300, 50)
FONT = "data/PlayfairDisplaySC-Bold.ttf"

class Button:
    def __init__(self, text, location, size, action=None):
        self.text = text
        self.location = location
        self.size = size
        self.font = pygame.font.Font(FONT, 25)
        self.color = BUTTON_COLOR
        self.hover_color = BUTTON_HOVER_COLOR
        self.rect = pygame.Rect(location, size)
        self.hover = False
        self.action = action

    def draw(self, screen):
        if self.hover:
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        # Center text
        text = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def is_hover(self, pos):
        if self.rect.collidepoint(pos):
            self.hover = True
        else:
            self.hover = False

    def click(self):
        if self.action is not None:
            return self.action
        return True


class Menu:
    def __init__(self, screen, status_bar, title="Gladiátorská aréna"):
        self.buttons = []
        self.running = True
        self.screen = screen
        self.title = title
        self.status_bar = status_bar

    def add_button(self, button):
        self.buttons.append(button)

    def run(self):
        while self.running is True:
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

    def update(self):
        if self.status == 'R':
            if self.current_time + self.refresh_time < time():
                session = Database("gladiatori_time", "Watcher", "localhost", 3306, "gladiatori")
                session.connect()
                self.current_time = time()
                end_time = session.get_end_time()
                self.remaining_time = round(end_time - self.current_time)
                if self.remaining_time < 0:
                    self.remaining_time = 0
                if self.admin is False:
                    self.golden_coins = session.get_golden_coins(self.team_id)
                    self.silver_coins = session.get_silver_coins(self.team_id)
                    self.bronze_coins = session.get_bronze_coins(self.team_id)
                session.disconnect()
        elif self.status == 'E':
            self.remaining_time = 0


    def draw(self):
        self.update()
        pygame.draw.rect(self.screen, BAR_COLOR, (self.location, self.size))
        # Time is in seconds, make it human readable
        time_text = self.font.render(f"Čas: {self.remaining_time // 60} : {self.remaining_time % 60}", True, TEXT_COLOR)
        # center in in the quarter box
        time_rect = time_text.get_rect(center=(self.size[0] // 8, self.size[1] // 2))
        self.screen.blit(time_text, time_rect)
        if self.admin is False:
            golden_coins_text = self.font.render(f"Z: {self.golden_coins}", True, TEXT_COLOR)
            golden_coins_rect = golden_coins_text.get_rect(center=(3 * self.size[0] // 8, self.size[1] // 2))
            self.screen.blit(golden_coins_text, golden_coins_rect)
            silver_coins_text = self.font.render(f"S: {self.silver_coins}", True, TEXT_COLOR)
            silver_coins_rect = silver_coins_text.get_rect(center=(5 * self.size[0] // 8, self.size[1] // 2))
            self.screen.blit(silver_coins_text, silver_coins_rect)
            bronze_coins_text = self.font.render(f"B: {self.bronze_coins}", True, TEXT_COLOR)
            bronze_coins_rect = bronze_coins_text.get_rect(center=(7 * self.size[0] // 8, self.size[1] // 2))
            self.screen.blit(bronze_coins_text, bronze_coins_rect)


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