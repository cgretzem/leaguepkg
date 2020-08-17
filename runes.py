"""
Handles runes and builds for all LOL champions.


Classes:
    `Rune` - Represents a rune choice
    `RunePage` - represents a Rune Page
    `Ability` - Represents an ability of a champion
    `Item` - represents an item in game
    `Champion` - represents a LOL champion

Methods:
    

Errors:


Misc Variables:

"""
from requests_html import HTMLSession

class Rune():
    """ 
    A class to represent a rune in League of Legends

    Attributes
    ----------
    `name` : str
        Holds the name of the rune.

    `img`: TBD
        represents the image asset for the rune
    """
    def __init__(self, name:str, img):
        self.name = name
        self.img = img

    def __str__(self):
        return f'Name : {self.name}\nImg Src : {self.img}'
class RunePage():
    """ 
    A class to represent a rune in League of Legends

    Attributes
    ----------
    `keystone` : Rune
        Holds the rune page Keystone.
    `prim1` : Rune
        Holds first rune in primary tree.
    `prim2` : Rune
        Holds second rune in primary tree.
    `prim3` : Rune
        Holds third rune in primary tree.
    `sec1`: Rune
        Holds first rune in secondary tree.
    `sec2`: Rune
        Holds second rune in secondary tree.
    `mods` : tuple
        Holds the offensive, flex, and defensive stats
    
    """
    def __init__(self, rune_tup : tuple, img):
        self.keystone = rune_tup[0]
        self.prim1 = rune_tup[1]
        self.prim2 = rune_tup[2]
        self.prim3 = rune_tup[3]
        self.sec1 = rune_tup[4]
        self.sec2 = rune_tup[5]
        self.mods = (rune_tup[6],rune_tup[7],rune_tup[8])

    
class Ability():
    """
    A class to represent an ability for a champion.

    Attributes
    ----------
    `activator` : str
        Says what activates the ability, Q W E R P (P is passive).
    `name` : str
        Holds the name of the ability.

    `img`: TBD
        represents the image asset for the ability
    """
    def __init__(self, activator : str, name : str, desc : str, img):
        self.activator = activator
        self.name = name
        self.img = img

class Champion():
    """
    A class to represent a champion.

    Attributes
    ----------
    name : str
        Holds name of champion.
    abilities : list[Abilities]
        Holds a list of all abilities for the champion
    runes : RunePage
        Holds meta runes for the champion
    max_order : list[str]
        Holds a list of strings with which abilities to level up levels 1-18
    img : TBD
        Represents an image asset for the champion

    """

    def __init__(self, name : str, abilities : list, runes : RunePage, max_order : list, img):
        self.name = name,
        self.abilities = abilities
        self.runes = runes
        self.max_order = max_order
        self.img = img




