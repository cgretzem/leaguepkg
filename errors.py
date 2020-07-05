"""
Errors
-------

`RequestError(str)`
`PlayerNotFoundException(str)`
"""


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
