import mariadb
import objects
from time import time

class Database:
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mariadb.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.cursor.close()
        self.connection.close()

    def create_tables(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS gladiators (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), health INT, defense INT, attack INT, price INT, level INT, experience INT, special_ability VARCHAR(255), picture_path VARCHAR(255), head_id INT, chest_id INT, legs_id INT, right_hand_id INT, left_hand_id INT, status VARCHAR(255), team_id INT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS weapons (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), damage INT, price INT, head_bonus INT, chest_bonus INT, legs_bonus INT, animal_bonus INT, special_ability VARCHAR(255), picture_path VARCHAR(255))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS armors (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), kind VARCHAR(255), defense INT, price INT, special_ability VARCHAR(255), picture_path VARCHAR(255))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS teams (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), golden_coins INT, silver_coins INT, bronze_coins INT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS game (id INT PRIMARY KEY AUTO_INCREMENT, start_time INT, end_time INT, status VARCHAR(255))")

    def add_gladiator(self, gladiator):
        # insert gladiator into table
        self.cursor.execute("""INSERT INTO gladiators (name, health, defense, attack, price, level, experience, special_ability, picture_path, head_id, chest_id, legs_id, right_hand_id, left_hand_id, status, team_id) VALUES (?,
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (gladiator.name, gladiator.health, gladiator.defense, gladiator.attack, gladiator.price, gladiator.level, gladiator.experience, gladiator.special_ability, gladiator.picture_path, gladiator.head, gladiator.chest, gladiator.legs, gladiator.right_hand, gladiator.left_hand, gladiator.status, gladiator.team_id))

        self.connection.commit()
    
    def remove_gladiator(self, gladiator):
        if gladiator is None:
            return
        self.cursor.execute("DELETE FROM gladiators WHERE id = ?", (gladiator.id,))
        self.connection.commit()

    def get_gladiator(self, gladiator_id):
        self.cursor.execute("SELECT * FROM gladiators WHERE id = ?", (gladiator_id,))
        result = self.cursor.fetchone()
        if result is None:
            return None
        return objects.Gladiator(*result)
    
    def get_start_time(self):
        self.cursor.execute("SELECT start_time FROM game")
        # return last row
        result = self.cursor.fetchall()[-1]
        return result[0]
    
    def get_end_time(self):
        self.cursor.execute("SELECT end_time FROM game")
        # return last row
        result = self.cursor.fetchall()[-1]
        return result[0]

    def get_team_ids(self):
        self.cursor.execute("SELECT id FROM teams")
        result = self.cursor.fetchall()
        return [x[0] for x in result]
    
    def create_team(self, name):
        self.cursor.execute("INSERT INTO teams (name, golden_coins, silver_coins, bronze_coins) VALUES (?, 0, 0, 0)", (name,))
        self.connection.commit()

    def add_team(self, team):
        self.cursor.execute("INSERT INTO teams (name, golden_coins, silver_coins, bronze_coins) VALUES (?, ?, ?, ?)", (team.name, team.golden_coins, team.silver_coins, team.bronze_coins))
        self.connection.commit()
    
    def get_team(self, team_id):
        self.cursor.execute("SELECT * FROM teams WHERE id = ?", (team_id,))
        result = self.cursor.fetchone()
        return objects.Team(*result)

    def get_slaves_of_team(self, team_id):
        self.cursor.execute("SELECT * FROM gladiators WHERE team_id = ?", (team_id,))
        result = self.cursor.fetchall()
        return [objects.Gladiator(*x) for x in result]
    
    def add_golden_coins(self, team_id, coins):
        self.cursor.execute("UPDATE teams SET golden_coins = golden_coins + ? WHERE id = ?", (coins, team_id))
        self.connection.commit()
    
    def add_silver_coins(self, team_id, coins):
        self.cursor.execute("UPDATE teams SET silver_coins = silver_coins + ? WHERE id = ?", (coins, team_id))
        self.connection.commit()

    def add_bronze_coins(self, team_id, coins):
        self.cursor.execute("UPDATE teams SET bronze_coins = bronze_coins + ? WHERE id = ?", (coins, team_id))
        self.connection.commit()

    def get_golden_coins(self, team_id):
        if team_id is None:
            return 0
        self.cursor.execute("SELECT golden_coins FROM teams WHERE id = ?", (team_id,))
        result = self.cursor.fetchone()
        return result[0]
    
    def get_silver_coins(self, team_id):
        if team_id is None:
            return 0
        self.cursor.execute("SELECT silver_coins FROM teams WHERE id = ?", (team_id,))
        result = self.cursor.fetchone()
        return result[0]
    
    def get_bronze_coins(self, team_id):
        if team_id is None:
            return 0
        self.cursor.execute("SELECT bronze_coins FROM teams WHERE id = ?", (team_id,))
        result = self.cursor.fetchone()
        return result[0]
    
    def start_game(self):
        self.cursor.execute("INSERT INTO game (start_time, end_time, status) VALUES (?, ?, ?)", (time(), time() + 3 * 60 * 60, 'R'))
        self.connection.commit()

    def stop_game(self):
        # set end_time to current time of the last row in table game
        self.cursor.execute("UPDATE game SET end_time = ? WHERE id = (SELECT MAX(id) FROM game)", (time(),))
        self.cursor.execute("UPDATE game SET status = 'E' WHERE id = (SELECT MAX(id) FROM game)")
        self.connection.commit()

    def add_time(self, seconds):
        self.cursor.execute("UPDATE game SET end_time = end_time + ? WHERE id = (SELECT MAX(id) FROM game)", (seconds,))
        self.connection.commit()

    def drop_database(self):
        self.cursor.execute("DROP DATABASE gladiatori")
        self.connection.commit()

    def is_game_running(self):
        self.cursor.execute("SELECT status FROM game WHERE id = (SELECT MAX(id) FROM game)")
        result = self.cursor.fetchone()
        if result is None:
            return False
        return result[0] == 'R'


def main():
    db = Database("gladiatori_admin", "VodazDunaje", "localhost", 3306, "gladiatori")
    db.connect()
    # db.create_tables()
    # db.create_team("RED")
    # db.add_gladiator(gladiator)
    # gladiator = db.get_gladiator(1)
    # db.remove_gladiator(gladiator)
    # gladiator = objects.Gladiator(0, "servus Testovni", 100, 10, 10, 100, 1, 0, "Testovni specialni schopnost", "testovni.png")
    # db.add_gladiator(gladiator)
    db.add_bronze_coins(1, 100)
    db.disconnect()

if __name__ == "__main__":
    main()