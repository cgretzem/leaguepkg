import subprocess
import pprint
import requests
import base64
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
"""
Handles classes and methods for an active local LOL Client.

Classes:
----------------------
    `Client` - Represents an active LOL client.

    `Aysnc_Client` - Represents an active lol client with Async support.

Errors:
--------------------
    `ClientConnectionError` - Error occurs when the program is unable to make a connection to the local client.
"""
class ClientConnectionError(Exception):
    def __init__(self, msg):
        self.msg = msg

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

    `get_pickable_champions()` : list
        Returns list of pickable champions.

    `change_current_page`(`name` : str, `primary_tree` : int, `perks` : list, `secondary_tree` : int)
        Changes runes and name of a rune page.

    `change_summoners`(`spell_1` : int, `spell_2` : int) : Response
        Changes the summoner spells to the new summoner IDs. Returns response code.
    
    `get_game_phase()` : str
        Returns the current game phase.

    `get_player_champ_select()` : list
        Returns a list of actions for the current champ select

    select_champ(`champID`: int) : bool
        Locks in the champion with the specified ID. Returns true if lock was successful.

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
        Constructor for Client Object, connects to LCU API.

        Returns : 
        -------------
        `Client` 
        """
        self.session = None
        self.app_port = ""
        self.summoner_id = 0
        self.__login()
        if self.check_connection() == False:
            raise ClientConnectionError('Unable to establish connection to League Client.')

    
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

    
    def get_pickable_champions(self):
        """
        Method to get all the pickable champion IDs for a given champ select.

        Returns:
        -----------------
        `list` : full of champion IDs that can be picked
        """

        return self.get_req('/lol-champ-select/v1/pickable-champion-ids').json()

    
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

        Returns : 
        --------------------
        `Response` : the response object from the post request.
        """
        data = self.get_current_page()
        page_id = data['id']
        data["name"] = name
        data["selectedPerkIds"] = perks
        data["primaryStyleId"] = primary_tree
        data["subStyleId"] = secondary_tree
        return self.put_req(f'/lol-perks/v1/pages/{page_id}', json.dumps(data))

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
        return self.patch_req('/lol-champ-select/v1/session/my-selection', data = json.dumps(data))


    def get_champ_select(self):
        """
        Method to return all data from a given champ select.

        Returns : 
        --------------------
        `dict` : all data from champ select
        """
        return self.get_req('/lol-champ-select/v1/session').json()
    
    def get_game_phase(self):
        """
        Method to return the current game phase.

        Returns : 
        -------------
        `str` : current game phase
        """
        return self.get_req('/lol-gameflow/v1/gameflow-phase').json()

    def get_player_champ_select(self):
        """
        Method to get only the local players actions in champ select.

        Returns : 
        -----------------
        `list` : list of actions for the local player.
        """
        cellID = -1
        select = self.get_champ_select()
        team = select['myTeam']

        for player in team:
            if(player['summonerId'] == self.summoner_id):
                cellID = player['cellId']
        actions = []
        for player in select['actions']:
            for act in player:

                if act['actorCellId'] == cellID:
                    actions.append(act)
        return actions

    def select_champ(self, champID: int):
        """
        Method to lock in the champion with the specified ID.

        Parameters : 
        -------------------
        `ChampID` : int
            ID that corresponds to the champion to be locked in.

        Returns : 
        ----------------
        `bool` : True if both the hover operation and the lock operation return code 200.
        """
        cellID = -1
        playerID = -1
        summoner_data = self.get_player_champ_select()
        data = {'championId': champID,}
        for entry in summoner_data:
            if entry['isAllyAction'] == True and entry['isInProgress'] == True:
                playerID = entry['id']
                hover = self.patch_req(f'/lol-champ-select/v1/session/actions/{playerID}', data = json.dumps(data))
                lock = self.post_req(f'/lol-champ-select/v1/session/actions/{playerID}/complete', data = json.dumps(data))
                return (hover.ok and lock.ok)
        return False

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

    
class Async_Client():

    """
    A class to represent an active LOL client with asyncronus support.

    Attributes:
    ----------
    `session` : Session 
        A requests.Session() object loaded with the login info for the LCU.
    `app_port` : str
        The port that the LCU chooses to connect to. Changes every time the client is launched.

    Methods:
    ----------
    `async check_connection()` : bool 
        Checks the connection to the client by retrieving current summoner at `/lol-summoner/v1/current-summoner`.

    `async get_rune_pages()` : dict
        Retrieves the list of rune pages for the current user.

    `async get_current_page()` : dict
        Retrives the currently active rune page details.

    `async get_pickable_champions()` : list
        Returns list of pickable champions.

    `async change_current_page`(`name` : str, `primary_tree` : int, `perks` : list, `secondary_tree` : int)
        Changes runes and name of a rune page.

    `async change_summoners`(`spell_1` : int, `spell_2` : int) : Response
        Changes the summoner spells to the new summoner IDs. Returns response code.
    
    `async get_game_phase()` : str
        Returns the current game phase.
        
     `async get_player_champ_select()` : list
        Returns a list of actions for the current champ select

    `async select_champ`(`champID`: int) : bool
        Locks in the champion with the specified ID. Returns true if lock was successful.

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
        Constructor for Client Object, connects to LCU API.

        Returns : 
        -------------
        `Client` 
        """
        self.session = None
        self.app_port = ""
        self.summoner_id = 0
        self.__login()

    
    async def check_connection(self):
        """
        Method to check if a sucessfull connection was established with the LCU API

        Returns
        -----------------
        `bool` : True when the connection is successful
        """
        response = await self.get_req('/lol-summoner/v1/current-summoner')
        return response.ok
        

    
    async def get_pickable_champions(self):
        """
        Method to get all the pickable champion IDs for a given champ select.

        Returns:
        -----------------
        `list` : full of champion IDs that can be picked
        """
        pickable_champs = await self.get_req('/lol-champ-select/v1/pickable-champion-ids')
        return pickable_champs.json()

    
    async def get_rune_pages(self):
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
        rune_pages = await self.get_req('/lol-perks/v1/pages')
        return rune_pages.json()


    async def get_current_page(self):
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
        current_page = await self.get_req('/lol-perks/v1/currentpage')
        return current_page.json()

    async def change_current_page(self, name, primary_tree : int, perks : list, secondary_tree : int):
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

        Returns : 
        --------------------
        `Response` : the response object from the post request.
        """
        data = await self.get_current_page()
        data["name"] = name
        data["selectedPerkIds"] = perks
        data["primaryStyleId"] = primary_tree
        data["subStyleId"] = secondary_tree
        response = await self.post_req('/lol-perks/v1/currentpage', data = json.dumps(data))
        return response

    async def change_summoners(self, spell_1 : int, spell_2 : int):
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
        response = await self.patch_req('/lol-champ-select/v1/session/my-selection', data = json.dumps(data))
        return response 


    async def get_champ_select(self):
        """
        Method to return all data from a given champ select.

        Returns : 
        --------------------
        `dict` : all data from champ select
        """
        champ_select = await (self.get_req('/lol-champ-select/v1/session'))

        return champ_select.json()
    
    async def get_game_phase(self):
        """
        Method to return the current game phase.

        Returns : 
        -------------
        `str` : current game phase
        """
        game_phase = await self.get_req('/lol-gameflow/v1/gameflow-phase')
        return game_phase.json()

    async def get_player_champ_select(self):
        """
        Method to get only the local players actions in champ select.

        Returns : 
        -----------------
        `list` : list of actions for the local player.
        """
        cellID = -1
        select = await self.get_champ_select()
        team = select['myTeam']
        for player in team:
            if(player['summonerId'] == self.summoner_id):
                cellID = player['cellId']
        actions = []
        for player in select['actions']:
            for act in player:

                if act['actorCellId'] == cellID:
                    actions.append(act)
        return actions

    async def select_champ(self, champID: int):
        """
        Method to lock in the champion with the specified ID.

        Parameters : 
        -------------------
        `ChampID` : int
            ID that corresponds to the champion to be locked in.

        Returns : 
        ----------------
        `bool` : True if both the hover operation and the lock operation return code 200.
        """
        cellID = -1
        playerID = -1
        summoner_data = await self.get_player_champ_select()
        data = {'championId': champID,}
        for entry in summoner_data:
            if entry['isAllyAction'] == True and entry['isInProgress'] == True:
                playerID = entry['id']
                
                hover = await self.patch_req(f'/lol-champ-select/v1/session/actions/{playerID}', data = json.dumps(data))
                lock = await self.post_req(f'/lol-champ-select/v1/session/actions/{playerID}/complete', data = json.dumps(data))
                return (hover.ok and lock.ok)
        return False
        
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
        try:
            self.summoner_id = self.session.get('https://127.0.0.1:' + self.app_port + '/lol-summoner/v1/current-summoner', verify = False).json()['summonerId']
        except Exception as e:
            raise ClientConnectionError('Unable to establish connection to League Client.')


    async def put_req(self, endpoint : str, data : dict):
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


    async def post_req(self, endpoint : str, data : dict):
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


    async def patch_req(self, endpoint : str, data : dict ):
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


    async def get_req(self, endpoint : str):
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
