
import subprocess
import requests
import base64

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
    `check_connection() : bool` 
        Checks the connection to the client by retrieving current summoner at `/lol-summoner/v1/current-summoner`.
    `get_rune_pages()` : JSON
        Retrieves the list of rune pages for the current user.
    `get_current_page()` : JSON
        Retrives the currently active rune page details.
    `get_req( str )` : Response
        Auxillary function to aid in making get requests with localhost and app port already filled into the url.
    `login()` : None
        Function to be run in initalization of Client object. Initalizes session object and connects to LCU.
    """
    def __init__(self):
        self.session = None
        self.app_port = ""
        self.login()
    
    def check_connection(self):
        """
        Method to check if a sucessfull connection was established with the LCU API
        ------------------
        Returns `boolean`
        """
        resp = self.get_req('/lol-summoner/v1/current-summoner')
        return resp.ok

        
    def get_rune_pages(self):
        """
        Method to get all rune pages.
        ---------------------------
        Returns : `JSON` with all availible rune page details, including default rune pages.
        """
        return self.get_req('/lol-perks/v1/pages').json()

    def get_current_page(self):
        """
        Method to return currently active rune page
        -------------------------------------------
        Returns : `JSON` with rune page details.
        """
        return self.get_req('/lol-perks/v1/currentpage').json()

   
    def login(self):
        """
        Method to be called in the constructor of Client in order to interface with the LCU API.
        ------------------
        """
        auth = subprocess.run(args = ['wmic', 'PROCESS', 'WHERE', "name='LeagueClientUx.exe'", 'GET', 'commandline'],capture_output=True)
        
        index = str(auth).find('--app-port=')
        self.app_port = (str(auth))[index+len('--app-port='):index+len('--app-port=') + 5]
        index = str(auth).find('--remoting-auth-token=')
        auth_token = str(auth)[index+len('--remoting-auth-token='):index+len('--remoting-auth-token=')+len('_3qGJj4eNN8NKLBDpuBrqg')]
        login = f'riot:{auth_token}'
        encodeLogin = 'Basic ' + (base64.b64encode(login.encode('ascii'))).decode('ascii')
        sess = requests.Session()
        headers = {'Authorization' : encodeLogin,
                    'User-Agent': 'insomnia/7.1.1',
                    'Accept': '*/*'}
        sess.headers.update(headers)
        self.session = sess

    def get_req(self, newPath : str):
        """
        General method to make a requests.get() with localhost and app port already filled in
        -----------------------------------------
        Param -- `String` newPath
        -----------------------------------------
        Returns `Response`
        """
        return self.session.get('https://127.0.0.1:' + self.app_port + newPath, verify = False)
    
if __name__ == "__main__":
    client = Client()
    print(client.check_connection())
    print(client.get_rune_pages())
    