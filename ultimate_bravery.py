"""
bah 
"""
import json
from random import choice, sample
from champion import Champion, Item, Rune
from data import Data
import leaguepkg

class UltimateBravery:
    """


    Attributes
    ----------

    `data` : Data


    `client_data` : Client **currently is avail_champ_ids


    `champion` : Champion


    `items` : list (Item)


    `runes` : runes


    Methods
    ----------

    `randomize_champion` : Champion


    `randomize_items` : items


    `randomize_runes` : runes


    """
    def __init__(self, client : leaguepkg.Client_interface.Client):
        self.data = Data()
        self.client = client
        self.avail_champ_ids = self.client.get_pickable_champions()
        self.champion = self.randomize_champion(self.avail_champ_ids)
        self.ban = self.randomize_champion(self.avail_champ_ids)
        self.items = self.randomize_items()
        self.runes = self.randomize_runes()

    
    def __str__(self):
        main = "Ultimate Bravery\n"
        div = "----------\n"

        champ = "Champion\n" + div + f"{self.champion}\n\n"
        
        items = "Item Set\n" + div + f"{self.items[0]}, {self.items[1]}, {self.items[2]}, {self.items[3]}, {self.items[4]}, {self.items[5]}\n\n"
        
        perks = self.runes[1]
        prims = f"Primary - {self.runes[0]}, {perks[0]}, {perks[1]}, {perks[2]}, {perks[3]}\n"
        secs = f"Secondary - {self.runes[2]}: {perks[4]}, {perks[5]}\n"
        stat_mods = f"Stat Mods - {perks[6]}, {perks[7]}, {perks[8]}\n"
        runes = "Runes\n" + div + prims + secs + stat_mods

        return main + div + champ + items + runes




    def randomize_champion(self, avail_champ_ids):
        """ """
        random_champ_id = choice(self.avail_champ_ids)

        for champ in self.data.champ_list:
            if int(random_champ_id) == int(champ["id"]):
                return Champion(champ["name"], champ["id"], champ["image"])
        

    def randomize_items(self):
        """ """
        items = []
        num_legendaries = 4
        boots = True

        if(self.champion.name == "Cassiopeia"):
            num_legendaries = 5
            boots = False

        if boots:
            boots = choice(self.data.item_dict["Boots"])
            items.append(Item(boots["name"], boots["id"], boots["image"]))
        
        mythic = choice(self.data.item_dict["Mythic"])
        items.append(Item(mythic["name"], mythic["id"], mythic["image"]))

        legendaries = sample(self.data.item_dict["Legendary"], num_legendaries)
        for legendary in legendaries:
            items.append(Item(legendary["name"], legendary["id"], legendary["image"]))
        
        return items


    def randomize_runes(self):
        """ """
        trees = sample(list(self.data.runes_dict.keys()), 2)
        prim_tree = trees[0]
        sec_tree = trees[1]

        prim_perks = self.__randomize_prims(prim_tree, ["Slot1", "Slot2", "Slot3"])
        sec_perks = self.__randomize_secs(sec_tree, ["Slot1", "Slot2"])
        stat_mod_perks = self.__randomize_stat_mods()
        perks = prim_perks + sec_perks + stat_mod_perks
        runes = [prim_tree, perks, sec_tree]

        return runes


    def __randomize_prims(self, prim_tree, slots):
        """ """
        prim_perks = []

        prim_keystone = choice((self.data.runes_dict[prim_tree]["Keystones"]))
        prim_perks.append(Rune(prim_keystone["name"], prim_keystone["id"], prim_keystone["image"]))

        for slot in slots:
            prim_rune = choice(list(self.data.runes_dict[prim_tree][slot]))
            prim_perks.append(Rune(prim_rune["name"], prim_rune["id"], prim_rune["image"]))
            
        return prim_perks


    def __randomize_secs(self, sec_tree, slots):
        """ """
        sec_perks = []

        for slot in slots:
            sec_rune = choice(list(self.data.runes_dict[sec_tree][slot]))
            sec_perks.append(Rune(sec_rune["name"], sec_rune["id"], sec_rune["image"]))
            
        return sec_perks


    def __randomize_stat_mods(self):
        """ """
        stat_mod_perks = []
        for slot in self.data.stat_mods_list:
            random_stat_mod = choice(slot)
            stat_mod = Rune(random_stat_mod["name"], random_stat_mod["id"], random_stat_mod["image"])
            stat_mod_perks.append(stat_mod)

        return stat_mod_perks