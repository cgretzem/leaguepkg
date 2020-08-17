"""
Handles classes and methods for an active local Game.

Classes:
    `ActiveGame` - Represents an active LOL game
    `Player` - represents a player inside the game
    `ActivePlayer` - subclass of player, represents host
    `Item` - represents an item in game

Methods:
    `check_status()` -> bool

Errors:
    `RequestError(str)` - Cannot connect to LOL api

Misc Variables:
__version__
"""

import requests, json, random, time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Error(Exception):
    """Base class for custom exceptions."""
    pass

class RequestError(Error):
    """Occurs when there is an issue retrieving a data.json from Riot API"""
    def __init__(self, msg):
        self.msg = msg

class PlayerNotFoundException(Error):
    """Occurs when a player is not found in the live client API"""
    def __init__(self, msg):
        self.msg = msg



def check_status():
    """Checks if a player is in a live game, returns false if not in a game."""
    try:
        output = requests.get('https://127.0.0.1:2999/liveclientdata/playerlist', verify = False)
    except:
        return False
    response = output.json()
    if not type(response) == list:
        return False
    else:
        return True

class Item:
    """
    A class to represent an item 

    Attributes:
    ----------
    `can_use` : bool
        True if item is an active item.
    `consumable` : bool
        True if item is a consumable.
    `count` : int
        Represents how many charges an item has left.
    `display_name` : str
        In-Game name of item.
    `item_ID` :
        ID of the item.
    `price` : int
        Cost of the item in the shop.
    `slot` : int
        Represents the slot the player has the item in.
    """
    def __init__(self, item_dict : dict):
        """Constructor that initializes the item based on a dict of values"""
        self.can_use = item_dict['canUse']
        self.consumable = item_dict['consumable']
        self.count = item_dict['count']
        self.display_name = item_dict['displayName']
        self.price = item_dict['price']
        self.slot = item_dict['slot']
    

class Player:
    """
    A class to represent a player inside an active game

    Attributes:
    ----------
    `champion_name` : str
        name of the champion the player is piloting
    `is_bot` : bool
        true if the player is a bot
    `is_dead` : bool
        true if the player is dead
    `items` : list[Item]
        a list of items in the players inventory
    `level` : int
        current level of player
    `position` : str
        returns the expected position of the player (may not always be accurate)
    `respawn_timer` : double
        the remaining time on the respawn timer
    `runes` : tuple(str) 
        a tuple of the basic rune paths in the format - (keystone, primaryTree, secondary Tree)
    `score` : dict
        a dictionary that holds assists, creepScore, deaths, kills, and ward score
    `skin_ID` : int
        ID of skin player is using, default skin is 0
    `summoner_name` : str
        name of the player
    `summoner_spells` : tuple(str)
        tuple of the two summoner spells 
    `team` : str
        either CHAOS or ORDER

  
    """

    def __init__(self, player_dict : dict):
        """A constructor that accepts a dict with player information inside to create values."""
        self.champion_name = player_dict['championName']
        self.is_bot = player_dict['isBot']
        self.is_dead = player_dict['isDead']
        self.items = []
        for item in player_dict['items']:
            self.items.append(Item(item))
        self.level = player_dict['level']
        self.position = player_dict['position']
        self.respawn_timer = player_dict['respawnTimer']
        self.runes = (player_dict['runes']['keystone']['displayName'],player_dict['runes']['primaryRuneTree']['displayName'],player_dict['runes']['secondaryRuneTree']['displayName'])
        self.scores = player_dict['scores']
        self.skin_ID = player_dict['skinID']
        self.summoner_name = player_dict['summonerName']
        self.summoner_spells = (player_dict['summonerSpells']['summonerSpellOne']['displayName'],player_dict['summonerSpells']['summonerSpellTwo']['displayName'])
        self.team = player_dict['team']


class ActivePlayer(Player):
    """
    A subclass of player that represents an active player, with more information
    
    Attributes:
    ----------
    `abilities` : dict of dicts
        holds ability level, name, and ID
    `champion_stats` : dict
        represents all champion stats such as AP and armor
    `gold` : double
        gold value in players inventory
    `full_runes` : list[dict]
        gets the full runes of player
    `stat_runes` : list[dict]
        contains stat runes such as armor, mr, attack speed, or cooldown reduction
    
    """
    def __init__(self, player_dict : dict, active_dict : dict):
        Player.__init__(self, player_dict)
        self.abilities = active_dict['abilities']
        self.champion_stats = active_dict['championStats']
        self.gold = active_dict['currentGold']
        self.full_runes = active_dict['fullRunes']['generalRunes']
        self.stat_runes = active_dict['fullRunes']['statRunes']


    

class ActiveGame:
    """ 
    A class to represent an active League of Legends Game.

    Attributes
    ----------
    `eventList` : list[dict]
        list of all events in the game
    `players` : list[str]
        list of players in current game
    `friends`: list[dict]
        list of friends from friends.json

    Methods:
    ----------
    `updateEventList()`: bool
        updates the game event list
    `getLastEvent()` : dict
        returns the most recent event, or None if no events happened
    """
    def __init__(self):
        """Initializes a new instance of an active game."""
        self.event_list = []
        self.active_player = None
        self.players = []
        
        self.updateEventList()
        self.loadPlayerList()
    def updateEventList(self):
        """Adds new Events to event_list, returns list of new events."""
        #gets json data from leagueAPI

        temp_event_list = self.event_list
        url = "https://127.0.0.1:2999/liveclientdata/eventdata"
        try:
            response = requests.get(url, verify = False)
            output = response.json()
            self.event_list = output['Events']
        except Exception:
            raise RequestError('Unable to retrieve Game Events')
        #checks if a new event has been added
        eventIDList = []
        newEvents = [] 
        count = 0
        for event in temp_event_list:
            eventIDList.append(event['EventID'])
        for event in self.event_list:
            if not event['EventID'] in eventIDList:
                newEvents.append(event)
        
        return newEvents

    def getLastEvent(self):
        """Gets the most recent event in the event_list, returns None if event_list is empty."""
        if not self.event_list:
            return None
        else:
            return self.event_list[-1]

    def loadPlayerList(self):
        try:
            res = requests.get('https://127.0.0.1:2999/liveclientdata/playerlist', verify = False)
            active = requests.get('https://127.0.0.1:2999/liveclientdata/activeplayer', verify = False)
        except:
            raise RequestError('Unable to retrieve playerlist')
        output = res.json()

        active_out = active.json()
        
        self.players.clear()
        for user in output: 
            if Player(user).summoner_name == active_out['summonerName']:
                actPlayer = ActivePlayer(user, active_out)
                self.players.append(actPlayer)
                self.active_player = actPlayer
            else:
                self.players.append(Player(user))
            

    def isPlayerPresent(self, player:str):
        """Checks if a player is in the current game"""
        for user in self.players:
            if user.summoner_name == player:
                return True
        return False


    def getChampName(self, player:str):
        """Gets the champion name of specified player based on IGN."""
        for user in self.players:
            if user.summoner_name == player:
                return user.champion_name
        raise PlayerNotFoundException('Could not find player in playerlist')


    
    

    
