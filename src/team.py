import pygame
from configparser import ConfigParser

from guistr import Menu, Button, loop, RESOlUTION, SIZE_BUTTON
from database import Database


def start_menu(screen, status_bar):
    menu = Menu(screen, status_bar)

    credentials = ConfigParser()
    credentials.read("credentials - red.ini")
    db = Database(credentials["TEAM"]["user"], credentials["TEAM"]["password"], credentials["TEAM"]["host"], int(credentials["TEAM"]["port"]), credentials["TEAM"]["database"])
    db.connect()

    status_bar.team_id = credentials["TEAM"]["id"]
    
    slave_market_button = Button("Trh s otroky", (RESOlUTION[0] // 2 - SIZE_BUTTON[0] // 2, 200), SIZE_BUTTON, slave_market_menu)
    menu.add_button(slave_market_button)

    forge_button = Button("Kovárna", (RESOlUTION[0] // 2 - SIZE_BUTTON[0] // 2, 300), SIZE_BUTTON, forge_menu)
    menu.add_button(forge_button)

    fight_button = Button("Aréna", (RESOlUTION[0] // 2 - SIZE_BUTTON[0] // 2, 400), SIZE_BUTTON, arena_menu)
    menu.add_button(fight_button)

    exit_button = Button("Konec", (RESOlUTION[0] // 2 - SIZE_BUTTON[0] // 2, 500), SIZE_BUTTON, exit)
    menu.add_button(exit_button)

    return menu.run()

def slave_market_menu():
    pass

def forge_menu():
    pass

def arena_menu():
    pass

def exit_menu():
    return False

if __name__ == "__main__":
    loop(start_menu)
