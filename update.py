"""
Handles data for LOL champions, items, runes and stat mods.

Methods:
    `set_champion_list()` : list


    `set_items()` : dict


    `set_runes()` : dict


    `set_stat_mods()` : list


"""
import json

champ_list = []
item_dict = {}
runes_dict = {}
stat_mods_list = []


def set_champions(version : int):
    """ Creates champion dict from LOL champion json file """
    with open(f"dragon/{version}/data/en_US/champion.json", "r", encoding="utf8") as f:
        champion_data = (json.load(f)["data"])
        for champion in champion_data:
            champ_list.append(dict(name = champion_data[champion]["name"], id = champion_data[champion]["key"], image = champion_data[champion]["image"]["full"]))
    return champ_list
    

def set_items(version : int):
    """ Creates mythic, legendary, and boots dicts from LOL items json file """
    mythics_list = []
    legendaries_list = []
    boots_list = []

    with open(f"dragon/{version}/data/en_US/item.json", "r", encoding="utf8") as f:
        items_data = (json.load(f)["data"])
        for item in items_data:
            name = items_data[item]["name"]
            item_id = item
            img = items_data[item]["image"]["full"]
            if "Mythic" in items_data[item]["description"]:
                mythics_list.append(dict(name = name, id = item_id, image = img))
            if not "Mythic" in items_data[item]["description"] and int(items_data[item]["gold"]["total"]) > 2000:
                legendaries_list.append(dict(name = name, id = item_id, image = img))
            if "Boots" in items_data[item]["tags"] and int(items_data[item]["gold"]["total"]) > 300:
                boots_list.append(dict(name = name, id = item_id, image = img))
    
    item_dict["Boots"] = boots_list
    item_dict["Mythic"] = mythics_list
    item_dict["Legendary"] = legendaries_list
    
    return item_dict

    

def set_runes(version : int):
    """ Creates a runes dict from LOL runes json file """

    with open(f"dragon/{version}/data/en_US/runesReforged.json", "r", encoding="utf8") as f:
        runes_data = (json.load(f))

        trees_list = []

        for tree in runes_data:
            runes_row = 0
            keystones_list = []
            slot1_list = []            
            slot2_list = []
            slot3_list = []            

            trees_list.append(tree["name"])

            for runes in tree["slots"]:
                runes_row = runes_row + 1
                for rune in runes["runes"]:
                    if (runes_row == 1):
                        keystones_list.append(dict(name = rune["name"], id = rune["id"], image = rune["icon"]))
                    elif (runes_row == 2):
                        slot1_list.append(dict(name = rune["name"], id = rune["id"], image = rune["icon"]))
                    elif (runes_row == 3):
                        slot2_list.append(dict(name = rune["name"], id = rune["id"], image = rune["icon"]))
                    elif (runes_row == 4):
                        slot3_list.append(dict(name = rune["name"], id = rune["id"], image = rune["icon"]))

            runes_dict[tree["name"]] = dict(Keystones = keystones_list, Slot1 = slot1_list, Slot2 = slot2_list, Slot3 = slot3_list)
        
        return runes_dict
    

def set_stat_mods():
    """ Creates a stat mods list """
    adaptive_force = dict(name = "Adaptive Force", id = 5008, image = "StatModsAdaptiveForceIcon.png")
    attack_speed = dict(name = "Attack Speed", id = 5005, image = "StatModsAttackSpeedIcon.png")
    scaling_cdr = dict(name = "Scaling CDR", id = 5007, image = "StatModsCDRScalingIcon.png")
    armor = dict(name = "Armor", id = 5003, image = "StatModsArmorIcon.png")
    magic_resist = dict(name = "Magic Resist", id = 5003, image = "StatModsMagicResIcon.png")
    health = dict(name = "Health", id = 5001, image = "StatModsHealthScalingIcon.png")

    slot1_list = [adaptive_force, attack_speed, scaling_cdr]
    slot2_list = [adaptive_force, magic_resist, armor]
    slot3_list = [health, magic_resist, armor]

    stat_mods_list.append(slot1_list)
    stat_mods_list.append(slot2_list)
    stat_mods_list.append(slot3_list)

    return stat_mods_list