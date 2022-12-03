from app.connection import connect
from app.models.user import User
import sys

def test():
    """ Just a simple test function """
    con = connect()
    with con:
        cur = con.cursor()
        cur.execute('USE baseball')

        sql = 'SELECT playerid FROM people LIMIT 10'
        cur.execute(sql)

        rows = cur.fetchall()
        for row in rows:
            print(row[0], file=sys.stdout)


def save_user(user: User):
    """ Saves the given User object to the database """

    con = connect()
    with con:
        cur = con.cursor()

        # set the database
        cur.execute('USE wii_baseball')

        # save the user
        sql = 'INSERT INTO user VALUES (%s, %s)'
        params = [user.username, user.hash]
        cur.execute(sql, params)
        con.commit()


# Gets the user with the given username
def find_user(username: str):
    """
    Gets the user with the given username from the database

    Parameters:
        - username: the username to search for

    Return: a User object if user exists, else None
    """
    con = connect()
    with con:
        cur = con.cursor()

        # set the database
        cur.execute('USE wii_baseball')

        # find the user
        sql = 'SELECT * FROM user WHERE username = %s'
        params = [username]
        cur.execute(sql, params)

        # extract the results
        user = cur.fetchone()
        if not user:
            return None
        return User(user[0], user[1])


# gets all users
def getAllUsers():
    """
    Gets all users from the database to be displayed

    Parameters:
        - none

    Return: all User objects if users exists, else None
    """
    con = connect()
    with con:
        cur = con.cursor()

        # set the database
        cur.execute('USE wii_baseball')

        # find all users
        sql = 'SELECT * FROM user'
        cur.execute(sql)

        # extract the results
        users = cur.fetchall()

        return users
