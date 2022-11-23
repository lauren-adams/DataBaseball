from app.connection import connect

import sys


def search_teamYear(params):
    """ Saves the given User object to the database """

    con = connect()
    with con:
        cur = con.cursor()

        # set the database
        cur.execute('USE baseball')
        sql1 = 'select divId from teams where yearId = %s and team_name = %s;'

        cur.execute(sql1, params)
        result = cur.fetchall()

        if len(result) < 1:
            return ""

        # save the user
        sql = 'select team_name, yearId, team_rank, team_W, team_L, divid from teams where yearId = %s and divId = %s order by team_W DESC;'
        params2 = [params[0], result[0]]

        cur.execute(sql, params2)
        results = cur.fetchall()

        con.commit()
        return results


def getTeams():
    con = connect()
    with con:
        cur = con.cursor()

        # set the database
        cur.execute('USE baseball')

        # save the user
        sql = 'select distinct team_name from teams;'
        cur.execute(sql)
        results = cur.fetchall()
        con.commit()
        return results


def getYears():
    con = connect()
    with con:
        cur = con.cursor()

        # set the database
        cur.execute('USE baseball')

        # save the user
        sql = 'select distinct yearId from teams order by yearID DESC;'
        cur.execute(sql)
        results = cur.fetchall()
        con.commit()
        return results


def getDiv(params):
    con = connect()
    with con:
        cur = con.cursor()

        # set the database
        cur.execute('USE baseball')

        # save the user
        sql1 = 'select lgId, divId from teams where yearId = %s and team_name = %s;'
        cur.execute(sql1, params)
        results = cur.fetchall()

        if len(results) < 1:
            return ""

        div = results[0][0]
        if results[0][1] != 'C':
            div += " East"
        elif results[0][1] == 'E':
            div += " Central"
        elif results[0][1] == 'W':
            div += " West"


        con.commit()
        return div

def getPlayOffs(year):
    con = connect()
    with con:
        cur = con.cursor()

        # set the database
        cur.execute('USE baseball')

        # save the user
        sql = 'select team_name from teams where (WCWin = \'y\' or DivWin = \'y\' or LgWin = \'y\') and yearId = %s;'
        cur.execute(sql, year)
        results = cur.fetchall()
        con.commit()
        return results

def inPlayOffs(params):
    con = connect()
    with con:
        cur = con.cursor()

        # set the database
        cur.execute('USE baseball')


        # save the user
        sql = 'select team_name from teams where (WCWin = \'y\' or DivWin = \'y\' or LgWin = \'y\') and yearId = %s and team_name = %s;'
        cur.execute(sql, params)
        results = cur.fetchall()
        con.commit()
        if len(results) == 0:
            return 0
        else:
            return 1

def getWinner(year):
    con = connect()
    with con:
        cur = con.cursor()

        # set the database
        cur.execute('USE baseball')

        # save the user
        sql = 'select team_name from teams where (WCWin = \'y\' or DivWin = \'y\' or LgWin = \'y\') and yearId = %s and WSWin = \'y\';'
        cur.execute(sql, year)
        results = cur.fetchall()
        con.commit()
        return results

