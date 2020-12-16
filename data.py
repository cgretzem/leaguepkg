"""

"""
import json
import urllib.request
import requests
import os, tarfile
from os import path
from update import set_champions, set_items, set_runes, set_stat_mods

class Data:
    """
    

    Attributes
    ----------
    `champions` : list
        

    `items` : dict
        
    

    Methods
    ----------
    `get_champions` : list


    `get_items` : list


    `get_runes` : dict


    `get_stat_mods` : 


    `check_data` : None


    `update_data` : None

    """
    def __init__(self):
        self.dragon_version = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()[0]
        self.check_data()

        self.champ_list = self.get_champions()
        self.item_dict = self.get_items()
        self.runes_dict = self.get_runes()
        self.stat_mods_list = self.get_stat_mods()
        
        

    def __str__(self):
        main = "LOL Data\n"
        div = "----------\n"
        champs = "Champion List\n" + div + f"{self.champ_list}\n\n"
        items = "Items Dict\n" + div + f"{self.item_dict}\n\n"
        runes = "Runes Dict\n" + div + f"{self.runes_dict}\n\n"
        stat_mods = "Stat Mods List\n" + div + f"{self.stat_mods_list}\n\n"

        return main + div + champs + items + runes + stat_mods


    def get_champions(self):
        """ """
        with open("dragon/champions.txt", "r") as f:
            champ_list = json.load(f)
        
        return champ_list


    def get_items(self):
        """ """
        with open("dragon/items.txt", "r") as f:
            item_dict = json.load(f)

        return item_dict


    def get_runes(self):
        """ """
        with open("dragon/runes.txt", "r") as f:
            runes_dict = json.load(f)
        
        return runes_dict

    
    def get_stat_mods(self):
        """ """
        with open("dragon/stat_mods.txt", "r") as f:
            stat_mods_list = json.load(f)

        return stat_mods_list


    def check_data(self):
        """ """
        zip_path = f'/dragon/dragontail-{self.dragon_version}.tgz'
        if not path.exists(zip_path):
            if not path.exists('dragon'):
                os.mkdir('dragon')
            url = f'https://ddragon.leagueoflegends.com/cdn/dragontail-{self.dragon_version}.tgz'
            

            outDir = f'{os.getcwd()}/dragon/dragontail-{self.dragon_version}.tgz'
            urllib.request.urlretrieve(url, outDir)
            tar = tarfile.open(outDir, 'r:gz')
            tar.extractall(path = 'dragon')
            

        data_files = ['dragon/champions.txt', 'dragon/items.txt', 'dragon/runes.txt', 'dragon/stat_mods.txt']
        for txt in data_files:
            if not path.exists(txt):
                self.update_data()
                break
    
    
    def update_data(self):
        """ Updates and stores LOL dicts in respective .txt files """
        with open("dragon/champions.txt", "w") as f:
            json.dump(set_champions(self.dragon_version), f, indent=2)

        with open("dragon/items.txt", "w") as f:
            json.dump(set_items(self.dragon_version), f, indent=2)

        with open("dragon/runes.txt", "w") as f:
            json.dump(set_runes(self.dragon_version), f, indent=2)

        with open("dragon/stat_mods.txt", "w") as f:
            json.dump(set_stat_mods(), f, indent=2)

if __name__ == '__main__':
    data = Data()
