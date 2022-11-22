class User:
    """
    This class should be the Python equivalent of the
    'user' table in the database
    """

    def __init__(self, username: str, hash: str):
        self.username = username
        self.hash = hash
