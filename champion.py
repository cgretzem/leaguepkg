"""


Classes:
    `Champion` - represents LOL champion

    
    `Item` - represents an item in game


    `Rune` - represents a rune choice


"""
class Champion:
    """

    
    Attributes
    ----------
    `name` : str


    `champ_id` : str


    `img` : str


    """
    def __init__(self, name, champ_id, img):
        self.name = name
        self.champ_id = champ_id
        self.img = img


    def __str__(self):
        return f"{self.name}: {self.champ_id}"
        


class Item:
    """


    Attributes
    ----------

    `name` : str


    `item_id` : str


    `img` : str


    """
    def __init__(self, name, item_id, img):
        self.name = name
        self.item_id = item_id
        self.img = img
    

    def __str__(self):
        return f"{self.name}: {self.item_id}"


class Rune:
    """
    

    Attributes
    ----------
    `name` : str


    `rune_id` : str


    `img` : str


    """
    def __init__(self, name, rune_id, img):
        self.name = name
        self.rune_id = rune_id
        self.img = img


    def __str__(self):
        return f"{self.name}: {self.rune_id}"


    
