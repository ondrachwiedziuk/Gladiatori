from objects import Mine
from database import Database
from time import time, sleep

def mine_loop(session):
    # Get all team ids
    team_ids = session.get_team_ids()
    # Get all slaves
    for team in team_ids:
        slaves = session.get_slaves_of_team(team)
        mine = Mine()
        mine.slaves = slaves
        mine.update(session)
        session.add_silver_coins(team, mine.production)
    return True

def main_loop():
    while True:
        session = Database("gladiatori_time", "Watcher", "localhost", 3306, "gladiatori")
        session.connect()
        if session.get_end_time() > time():
            mine_loop(session)
        session.disconnect()
        sleep(60)
