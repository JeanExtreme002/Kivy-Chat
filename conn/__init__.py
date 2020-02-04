class Connection(object):

    """
    Classe Abstrata.
    """

    separator = "</[$sep2xOC#]/>"
    
    timeout = 5

    warningMessages = {
        "connected": "{} joined the chat.",
        "connection_lost": "Lost connection to the server.",
        "disconnected": "{} has left the chat."
    }

    def close(self): 
        raise NotImplementedError

    def run(self): 
        raise NotImplementedError

    def send(self): 
        raise NotImplementedError
