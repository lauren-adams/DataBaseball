from app.connection import connect
import sys

def saveQuery(username: str, query: str):
    """ Saves the given Query to the database """

    con = connect()
    with con:
        cur = con.cursor()

        # set the database
        cur.execute('USE wii_baseball')

        # save the user
        sql = 'INSERT INTO query VALUES (%s, %s)'
        params = [username, query]
        cur.execute(sql, params)
        con.commit()

def countQuery(users):
    con = connect()

    result = [];

    with con:
        cur = con.cursor()

        # set the database
        cur.execute('USE wii_baseball')

        for u in users:
            # find the user
            sql = 'SELECT count(*) FROM query WHERE username = %s'
            params = [u[0]]
            cur.execute(sql, params)
            temp = cur.fetchone()
            result.append([u[0], temp[0]])

    return result

