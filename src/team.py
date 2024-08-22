import pygame
from configparser import ConfigParser

from guistr import Menu, Button, ImageButton, loop, RESOlUTION, SIZE_BUTTON, GREEN_BUTTON_COLOR, GREEN_BUTTON_HOVER_COLOR, BUTTON_COLOR
from database import Database


def login(status_bar=None):
    credentials = ConfigParser()
    credentials.read("credentials - red.ini")
    db = Database(credentials["TEAM"]["user"], credentials["TEAM"]["password"], credentials["TEAM"]["host"], int(credentials["TEAM"]["port"]), credentials["TEAM"]["database"])
    db.connect()
    if status_bar is not None:
        status_bar.team_id = credentials["TEAM"]["id"]
    return db


def start_menu(screen, status_bar):
    menu = Menu(screen, status_bar, start_menu)
    pygame.display.set_caption("Gladiátorská aréna")

    if status_bar.team_id is None:
        db = login(status_bar)
        db.disconnect()

    # Two columns
    slave_market_button = Button("Trh s otroky", (RESOlUTION[0] // 4 - SIZE_BUTTON[0] // 2, 200), SIZE_BUTTON, slave_market_menu)

    forge_button = Button("Kovárna", (3 * RESOlUTION[0] // 4 - SIZE_BUTTON[0] // 2, 200), SIZE_BUTTON, forge_menu)

    fight_button = Button("Aréna", (RESOlUTION[0] // 4 - SIZE_BUTTON[0] // 2, 300), SIZE_BUTTON, arena_menu)

    training_button = Button("Cvičiště", (3 * RESOlUTION[0] // 4 - SIZE_BUTTON[0] // 2, 300), SIZE_BUTTON, training_menu)

    mine_button = Button("Důl", (RESOlUTION[0] // 4 - SIZE_BUTTON[0] // 2, 400), SIZE_BUTTON, None)

    inventory_button = Button("Inventář", (3 * RESOlUTION[0] // 4 - SIZE_BUTTON[0] // 2, 400), SIZE_BUTTON, None)

    menu.add_button(slave_market_button)
    menu.add_button(forge_button)
    menu.add_button(fight_button)
    menu.add_button(training_button)
    menu.add_button(mine_button)
    menu.add_button(inventory_button)

    exit_button = Button("Konec", (RESOlUTION[0] // 2 - SIZE_BUTTON[0] // 2, 500), SIZE_BUTTON, exit)
    menu.add_button(exit_button)

    return menu.run()

def slave_market_menu():
    pass

def forge_menu():
    pass

def arena_menu():
    pass


def training_menu(screen, status_bar):
    # Make screen wider
    menu = Menu(screen, status_bar, training_menu, "Cvičiště")

    # Three rows
    for i in range(3):
        task_row(menu, status_bar, i)

    exit_button = Button("Zpět", (RESOlUTION[0] // 2 - SIZE_BUTTON[0] // 2, 500), SIZE_BUTTON, start_menu)
    menu.add_button(exit_button)

    return menu.run()


def task_row(menu, status_bar, number):
    if status_bar.status == 'R':
        if status_bar.tasks[number] is None:
            blank = Button("", (10, 200 + 100 * number), (RESOlUTION[0] - 60, 50), hover_color=BUTTON_COLOR)
            menu.add_button(blank)
            # Add button for refresh (new task)
            refresh_button = ImageButton("data/refresh.png", (RESOlUTION[0] - 60, 200 + 100 * number), (50, 50), training_menu, secondary_action=add_task, secondary_action_args=(status_bar, status_bar.team_id,))
            menu.add_button(refresh_button)
        else:
            # Add text as button withou action
            task_label = Button(status_bar.tasks[number].description, (10, 200 + 100 * number), (RESOlUTION[0] - 210, 50), None, hover_color=BUTTON_COLOR)
            menu.add_button(task_label)
            # Add symbol of bronz coins
            bronze_coins = ImageButton("data/bronze_coins.png", (RESOlUTION[0] - 210, 200 + 100 * number), (50, 50), None, hover_color=BUTTON_COLOR)
            menu.add_button(bronze_coins)
            # Add reward
            reward_label = Button(str(status_bar.tasks[number].reward), (RESOlUTION[0] - 160, 200 + 100 * number), (50, 50), None, hover_color=BUTTON_COLOR)
            menu.add_button(reward_label)
            # Add button for complete task
            complete_button = ImageButton("data/tick.png", (RESOlUTION[0] - 110, 200 + 100 * number), (50, 50), training_menu, color=GREEN_BUTTON_COLOR, hover_color=GREEN_BUTTON_HOVER_COLOR, secondary_action=complete_task, secondary_action_args=(status_bar, status_bar.tasks[number].id,))
            menu.add_button(complete_button)
            # Add button for refresh (new task)
            refresh_button = ImageButton("data/refresh.png", (RESOlUTION[0] - 60, 200 + 100 * number), (50, 50), training_menu, secondary_action=reassign_task, secondary_action_args=(status_bar, status_bar.tasks[number].id,status_bar.team_id))
            menu.add_button(refresh_button)


def reassign_task(status_bar, task_id, team_id):
    db = login()
    if task_id is not None:
        db.complete_task(task_id, False)
    db.assign_task(team_id)
    db.disconnect()
    status_bar.refresh = 1


def add_task(status_bar, team_id):
    if team_id is None:
        return None
    db = login()
    db.assign_task(team_id)
    db.disconnect()
    status_bar.refresh = 1


def complete_task(status_bar, task_id, reward=True):
    if task_id is None:
        return None
    db = login()
    db.complete_task(task_id, reward)
    db.disconnect()
    status_bar.refresh = 1


def exit_menu():
    return False

if __name__ == "__main__":
    loop(start_menu)
