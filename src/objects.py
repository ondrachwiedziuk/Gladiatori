from random import random


class Gladiator:
    def __init__(self, id_, name, health, defense, attack, price, level, experience, special_ability, picture_path, head=None, chest=None, legs=None, right_hand=None, left_hand=None, status='A', team_id=None):
        self.id = id_
        self.name = name
        self.health = health
        self.defense = defense
        self.attack = attack
        self.price = price
        self.level = level
        self.experience = experience
        self.special_ability = special_ability
        self.picture_path = picture_path
        self.head = head
        self.chest = chest
        self.legs = legs
        self.right_hand = right_hand
        self.left_hand = left_hand
        self.status = status
        self.team_id = team_id


class Weapon:
    def __init__(self, id_, name, damage, price, head_bonus, chest_bonus, legs_bonus, animal_bonus, special_ability, picture_path, status='A', team_id=None):
        self.id = id_
        self.name = name
        self.damage = damage
        self.price = price
        self.head_bonus = head_bonus
        self.chest_bonus = chest_bonus
        self.legs_bonus = legs_bonus
        self.animal_bonus = animal_bonus
        self.special_abilities = special_ability
        self.picture_path = picture_path
        self.status = 'A'
        self.team_id = None

class Armor:
    def __init__(self, id_, name, kind, defense, price, special_ability, picture_path, status='A', team_id=None):
        self.id = id_
        self.name = name
        self.kind = kind
        self.defense = defense
        self.price = price
        self.special_abilities = special_ability
        self.picture_path = picture_path
        self.status = status
        self.team_id = team_id

class SpecialAbility:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Animal:
    def __init__(self, id_, name, health, defense, attack, price, special_abilities, picture_path):
        self.id = id_
        self.name = name
        self.health = health
        self.defense = defense
        self.attack = attack
        self.price = price
        self.special_abilities = special_abilities
        self.picture_path = picture_path

class Team:
    def __init__(self, name):
        self.name = name
        self.golden_coins = 0
        self.silver_coins = 0
        self.bronze_coins = 0
        self.gladiators = []
        self.weapons = []
        self.armors = []

class Mine:
    def __init__(self):
        self.slaves = []
        self.production = 0

    def update(self, session):
        for slave in self.slaves:
            if slave.status == 'M1':
                self.production += 1
            elif slave.status == 'M2':
                self.production += 3
                if random() < 0.1:
                    slave.status = 'D'
                    slave.team_id = None
                    session.update_gladiator(slave)

            elif slave.status == 'M3':
                self.production += 5
                if random() < 0.3:
                    slave.status = 'D'
                    slave.team_id = None
                    session.update_gladiator(slave)