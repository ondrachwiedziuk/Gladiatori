import pygame
from guistr import Menu, Button, loop, RESOlUTION, SIZE_BUTTON
from database import Database


def admin_menu(screen, status_bar):
    menu = Menu(screen, status_bar, "Admin")
    # Two columns
    run_button = Button("Spustit hru", (RESOlUTION[0] // 4 - SIZE_BUTTON[0] // 2, 200), SIZE_BUTTON, start_game)
    menu.add_button(run_button)
    stop_button = Button("Zastavit/pustit hru", (3 * RESOlUTION[0] // 4 - SIZE_BUTTON[0] // 2, 200), SIZE_BUTTON, stop_game)
    menu.add_button(stop_button)
    # Two columns
    add_time_button = Button("Přidat 15 minut", (RESOlUTION[0] // 4 - SIZE_BUTTON[0] // 2, 300), SIZE_BUTTON, add_time)
    menu.add_button(add_time_button)
    remove_time_button = Button("Odebrat 15 minut", (3 * RESOlUTION[0] // 4 - SIZE_BUTTON[0] // 2, 300), SIZE_BUTTON, remove_time)
    menu.add_button(remove_time_button)
    # Two columns
    # Escape of gladiators
    escape_button = Button("Útěk gladiátorů", (RESOlUTION[0] // 4 - SIZE_BUTTON[0] // 2, 400), SIZE_BUTTON, None) # TODO: Add action
    menu.add_button(escape_button)
    # Inflation
    inflation_button = Button("INFLACE", (3 * RESOlUTION[0] // 4 - SIZE_BUTTON[0] // 2, 400), SIZE_BUTTON, None) # TODO: Add action
    menu.add_button(inflation_button)

    exit_button = Button("Zpět", (RESOlUTION[0] // 2 - SIZE_BUTTON[0] // 2, 500), SIZE_BUTTON, start_menu)
    menu.add_button(exit_button)
    return menu.run()


def start_game(screen, status_bar):
    db = Database("gladiatori_admin", "VodazDunaje", "localhost", 3306, "gladiatori")
    db.connect()
    db.start_game()
    db.disconnect()
    status_bar.status = 'R'
    return admin_menu


def stop_game(screen, status_bar):
    db = Database("gladiatori_admin", "VodazDunaje", "localhost", 3306, "gladiatori")
    db.connect()
    db.stop_game()
    db.disconnect()
    status_bar.status = 'E'
    return admin_menu


def add_time(screen, status_bar):
    db = Database("gladiatori_admin", "VodazDunaje", "localhost", 3306, "gladiatori")
    db.connect()
    # Add 15 minutes
    db.add_time(15 * 60)
    db.disconnect()
    return admin_menu


def remove_time(screen, status_bar):
    db = Database("gladiatori_admin", "VodazDunaje", "localhost", 3306, "gladiatori")
    db.connect()
    # Remove 15 minutes
    db.add_time(-15 * 60)
    db.disconnect()
    return admin_menu


def arena_menu(screen, status_bar):
    menu = Menu(screen, status_bar, "Aréna")
    # Two columns
    first_team_button = Button("První tým", (RESOlUTION[0] // 4 - SIZE_BUTTON[0] // 2, 200), SIZE_BUTTON, None) # TODO: Add action
    menu.add_button(first_team_button)
    second_team_button = Button("Druhý tým", (3 * RESOlUTION[0] // 4 - SIZE_BUTTON[0] // 2, 200), SIZE_BUTTON, None) # TODO: Add action
    menu.add_button(second_team_button)
    fight_button = Button("Začít souboj", (RESOlUTION[0] // 2 - SIZE_BUTTON[0] // 2, 400), SIZE_BUTTON, None) # TODO: Add action
    menu.add_button(fight_button)
    exit_button = Button("Zpět", (RESOlUTION[0] // 2 - SIZE_BUTTON[0] // 2, 500), SIZE_BUTTON, start_menu)
    menu.add_button(exit_button)
    return menu.run()


def aukce_menu(screen, status_bar):
    menu = Menu(screen, status_bar, "Aukce")
    select_button = Button("Vybrat", (RESOlUTION[0] // 2 - SIZE_BUTTON[0] // 2, 200), SIZE_BUTTON, None) # TODO: Add action
    menu.add_button(select_button)
    sell_button = Button("Prodat", (RESOlUTION[0] // 2 - SIZE_BUTTON[0] // 2, 300), SIZE_BUTTON, None) # TODO: Add action
    menu.add_button(sell_button)
    exit_button = Button("Zpět", (RESOlUTION[0] // 2 - SIZE_BUTTON[0] // 2, 500), SIZE_BUTTON, start_menu)
    menu.add_button(exit_button)
    return menu.run()


def exit_menu():
    return False


def start_menu(screen, status_bar):
    pygame.display.set_caption("Gladiátorská aréna")
    menu = Menu(screen, status_bar)
    # Center buttons
    new_game_button = Button("Admin", (RESOlUTION[0] // 2 - SIZE_BUTTON[0] // 2, 200), SIZE_BUTTON, admin_menu)
    load_game_button = Button("Aréna", (RESOlUTION[0] // 2 - SIZE_BUTTON[0] // 2, 300), SIZE_BUTTON, arena_menu)
    connect_to_server_button = Button("Aukce", (RESOlUTION[0] // 2 - SIZE_BUTTON[0] // 2, 400), SIZE_BUTTON, aukce_menu)
    exit_button = Button("Konec", (RESOlUTION[0] // 2 - SIZE_BUTTON[0] // 2, 500), SIZE_BUTTON, exit_menu)
    menu.add_button(new_game_button)
    menu.add_button(load_game_button)
    menu.add_button(connect_to_server_button)
    menu.add_button(exit_button)
    return menu.run()


if __name__ == "__main__":
    loop(start_menu, True)
