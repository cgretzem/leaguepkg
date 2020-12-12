import subprocess
import pprint
import asyncio
import requests
import base64
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
"""
Handles classes and methods for an active local LOL Client.
Classes:
    `Client` - Represents an active LOL client.
"""
class Client():
    """
    A class to represent an active LOL client.
    Attributes:
    ----------
    `session` : Session 
        A requests.Session() object loaded with the login info for the LCU.
    `app_port` : str
        The port that the LCU chooses to connect to. Changes every time the client is launched.
    Methods:
    ----------
    `check_connection()` : bool 
        Checks the connection to the client by retrieving current summoner at `/lol-summoner/v1/current-summoner`.
    `get_rune_pages()` : dict
        Retrieves the list of rune pages for the current user.
    `get_current_page()` : dict
        Retrives the currently active rune page details.
    `get_req( str )` : Response
        Auxillary function to aid in making get requests with localhost and app port already filled into the url.
    `patch_req( str )` : Response
        Auxillary function to aid in making patch requests with localhost and app port already filled into the url.
    `put_req( str )` : Response
        Auxillary function to aid in making put requests with localhost and app port already filled into the url.
    `post_req( str )` : Response
        Auxillary function to aid in making post requests with localhost and app port already filled into the url.
    `__login()` : None
        Private method to be run in initalization of Client object. Initalizes session object and connects to LCU.
    """
    def __init__(self):
        """
        Constructor for Client Object, connects to LCU API
        """
        self.session = None
        self.app_port = ""
        self.summoner_id = 0
        self.__login()
        self.check_connection()

    
    def check_connection(self):
        """
        Method to check if a sucessfull connection was established with the LCU API
        Returns
        -----------------
        `bool` : True when the connection is successful
        """
        resp = self.get_req('/lol-summoner/v1/current-summoner')
        self.summoner_id = resp.json()['summonerId']
        return resp.ok

        
    def get_rune_pages(self):
        """
        Method to get all rune pages.
        Returns
        -----------------
        `dict` : All availible rune page details, including default rune pages.
        
        Contents of dict:
        -----------------------------------
        `autoModifiedSelections` : list
        `current` : bool
        `id` : float
        `isActive` : bool
        `isDeletable` : bool
        `isEditable` : bool
        `isValid` : bool
        `lastModified` : float
        `name` : str
        `order` : int
        `primaryStyleId` : int
        `selectedPerkIds : list(int)
        `subStyleId` : int
        
        """
        return self.get_req('/lol-perks/v1/pages').json()


    def get_current_page(self):
        """
        Method to return currently active rune page.
        
        Returns
        -----------------
        `dict` : dictionary with runepage details.
        Contents of dict:
        -----------------------------------
        `autoModifiedSelections` : []
        `current` : bool
        `id` : float
        `isActive` : bool
        `isDeletable` : bool
        `isEditable` : bool
        `isValid` : bool
        `lastModified` : float
        `name` : str
        `order` : int
        `primaryStyleId` : int
        `selectedPerkIds : [int]
        `subStyleId` : int
        
        """

        return self.get_req('/lol-perks/v1/currentpage').json()

    def change_current_page(self, name, primary_tree : int, perks : list, secondary_tree : int):
        """
        Method to change the current runepage to the specified new data.
        Parameters:
        -----------
        name : str
            The new name of the rune page.
        primary_tree : int
            The ID of the new primary tree.
        perks : list
            List of the intended perk IDs. Must have a length of 9.
        secondary_tree : int
            ID of the secondary perk tree.     
        """
        data = self.get_current_page()
        data["name"] = name
        data["selectedPerkIds"] = perks
        data["primaryStyleId"] = primary_tree
        data["subStyleId"] = secondary_tree
        return self.post_req('/lol-perks/v1/currentpage', data)

    def change_summoners(self, spell_1 : int, spell_2 : int):
        """
        Method to change the current summoner spells to new ones.
        Parameters :
        -------------
        `spell_1` : int
            ID code for the left summoner spell.
        `spell_2` : int
            ID code for the right summoner spell.
        Returns : 
        -------------
        `Response` : Response
            Returns response for the patch request.
        """
        data = {
            "spell1Id": spell_1,
            "spell2Id": spell_2
        }
        self.patch_req('/lol-champ-select/v1/session/my-selection', data = data)


    def get_champ_select(self):
        return self.get_req('/lol-champ-select/v1/session').json()
    
    def in_champ_select(self):
        return self.get_req('/lol-champ-select/v1/session').ok

    async def select_champ(self, champID: int):
        cellID = -1
        ID = -1
        data = {}
        select = self.get_champ_select()
        team = select['myTeam']
        for player in team:
            if(team['summonerId'] == self.summoner_id):
                cellID = team['cellId']
        for player in select['actions'][0][0]:
            if player['actorCellId'] == cellID:
                ID = player['id']
                data = player
        data['championId'] = champID
        self.patch_req(f'/lol-champ-select/v1/session/actions/{ID}', data = data)
        asyncio.sleep(1)
        data['completed'] = True
        self.patch_req(f'/lol-champ-select/v1/session/actions/{ID}', data = data)
    def __login(self):
        """
        Method to be called in the constructor of Client in order to interface with the LCU API.
        
        """
        auth = subprocess.run(args = ['wmic', 'PROCESS', 'WHERE', "name='LeagueClientUx.exe'", 'GET', 'commandline'],capture_output=True)
        
        #finding app port
        index = str(auth).find('--app-port=')
        self.app_port = (str(auth))[index+len('--app-port='):index+len('--app-port=') + 5]

        #finding auth token
        index = str(auth).find('--remoting-auth-token=')
        auth_token = str(auth)[index+len('--remoting-auth-token='):index+len('--remoting-auth-token=')+len('_3qGJj4eNN8NKLBDpuBrqg')]

        #creating and encoding login 
        login = f'riot:{auth_token}'
        encodeLogin = 'Basic ' + (base64.b64encode(login.encode('ascii'))).decode('ascii')

        #creating session with login info
        sess = requests.Session()
        headers = {'Authorization' : encodeLogin,
                    'User-Agent': 'insomnia/7.1.1',
                    'Accept': '*/*'}
        sess.headers.update(headers)
        self.session = sess


    def put_req(self, endpoint : str, data : dict):
        """
        General method to make a requests.put() with localhost and app port already filled in.
        
        Parameters : 
        ----------------------
        `endpoint` : str
            The endpoint for the LCU API.
        `data` : dict
            Data to put at the specified endpoint.
        
        Returns
        -----------------
         `Response` : Response from requests.put().
        """
        return self.session.put('https://127.0.0.1:' + self.app_port + endpoint, data = data, verify = False)


    def post_req(self, endpoint : str, data : dict):
        """
        General method to make a requests.post() with localhost and app port already filled in.
        
        Parameters : 
        ----------------------
        `endpoint` : str
            The endpoint for the LCU API.
        `data` : dict
            Data to put at the specified endpoint.
        
        Returns
        -----------------
         `Response` : Response from requests.post().
        """
        return self.session.post('https://127.0.0.1:' + self.app_port + endpoint, data = data, verify = False)


    def patch_req(self, endpoint : str, data : dict ):
        """
        General method to make a requests.patch() with localhost and app port already filled in.
        
        Parameters : 
        ----------------------
        `endpoint` : str
            The endpoint for the LCU API.
        `data` : dict
            Data to put at the specified endpoint.
        
        Returns
        -----------------
         `Response` : Response from requests.patch().
        """
        return self.session.patch('https://127.0.0.1:' + self.app_port + endpoint, data = data, verify = False)


    def get_req(self, endpoint : str):
        """
        General method to make a requests.get() with localhost and app port already filled in.
        
        Parameters : 
        ----------------------
        endpoint : str
            The endpoint for the LCU API.
        Returns
        -----------------
         `Response` : Response from requests.put().
        """
        return self.session.get('https://127.0.0.1:' + self.app_port + endpoint, verify = False)
    
if __name__ == "__main__":
    client = Client()
    print(client.check_connection())
    print(client.summoner_id)
    pprint.pprint(client.select_champion(1,1))