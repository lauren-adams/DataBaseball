from app import app
from app.connection import connect

import sys

'''
function: search_teamYear
params: takes yearid and team_name in params
return: results with name, year, wins, losses, win percent, runs...
searches data associated with team's division and displays it
'''
def search_teamYear(params):
    con = connect()
    with con:
        cur = con.cursor()

        # set the database
        cur.execute('USE baseball')
        sql1 = 'select divId, lgId from teams where yearId = %s and team_name = %s;'

        cur.execute(sql1, params)
        result = cur.fetchall()
        app.logger.info(result)


        # if empty set return nothing
        if (result == ()):
            return ""


        #if no dvision search by league
        if result[0][0] == None:
            # get max wins from databse
            getMax = 'select team_w from teams where yearId = %s and lgId = %s and team_rank = \'1\';'
            paramsMax = [params[0], result[0][1]]

            cur.execute(getMax, paramsMax)
            wins = cur.fetchall()

            # get records from database by league
            sql = "select team_name, yearId, team_rank, team_W, team_L, divid, team_w/(team_w + team_l) as percent, " + str(wins[0][0]) + " - team_w as gb, team_r, team_ra, team_r - team_ra, team_w * power(team_r, 1.82)/(power(team_ra, 1.82) + power(team_r, 1.82)) from teams where yearId = %s and lgId = %s order by team_W DESC;"
            params2 = [params[0], result[0][1]]



            cur.execute(sql, params2)
            results = cur.fetchall()
            con.commit()
            return results

        # select max from list
        getMax = 'select team_w from teams where yearId = %s and divid = %s and lgId = %s and team_rank = \'1\';'
        paramsMax = [params[0], result[0][0], result[0][1]]

        cur.execute(getMax, paramsMax)
        wins = cur.fetchall()
        win = int(wins[0][0])



        # get data from division
        sql = "select team_name, yearId, team_rank, team_W, team_L, divid, team_w/(team_w + team_l) as percent, " + str(wins[0][0]) + " - team_w as gb, team_r , team_ra, team_r - team_ra from teams where yearId = %s and divId = %s and lgId = %s order by team_W DESC;"
        print(sql)
        params2 = [ params[0], result[0][0], result[0][1]]

        cur.execute(sql, params2)
        results = cur.fetchall()


        con.commit()
        return results


'''
function: getTeams()
params: none
return: list of all teams in the database
searches data for teams and returns results which is a list of teams
'''
def getTeams():
    con = connect()
    with con:
        cur = con.cursor()

        # set the database
        cur.execute('USE baseball')

        # querey fro teams
        sql = 'select distinct team_name from teams order by team_name;'
        cur.execute(sql)
        results = cur.fetchall()
        con.commit()
        return results

'''
function: getYears()
params: none
return: list of all years in the database
searches data for years and returns results which is a list of years
'''
def getYears():
    con = connect()
    with con:
        cur = con.cursor()

        # set the database
        cur.execute('USE baseball')

        # query for years
        sql = 'select distinct yearId from teams order by yearID DESC;'
        cur.execute(sql)
        results = cur.fetchall()
        con.commit()
        return results

'''
function: getDiv()
params: params which has team and year
return: string that has full division name
searches for division name that matches team and year
'''
def getDiv(params):
    con = connect()
    with con:
        cur = con.cursor()

        # set the database
        cur.execute('USE baseball')

        # get query for league and division
        sql1 = 'select lgId, divId from teams where yearId = %s and team_name = %s;'
        cur.execute(sql1, params)
        results = cur.fetchall()

        if (results == ()):
            return "no results in "

        if results[0][1] == None:
            return results[0][0]

        # iterate through to get the correct division
        div = results[0][0]
        if results[0][1] == 'E':
            div += " East"
        elif results[0][1] == 'C':
            div += " Central"
        elif results[0][1] == 'W':
            div += " West"


        con.commit()
        return div
'''
function: getPlayoffs(year)
params: yearid
return: list of all teams that made playoffs in a specific year
searches by year to get all of the data
'''
def getPlayOffs(year):
    con = connect()
    with con:
        cur = con.cursor()

        # set the database
        cur.execute('USE baseball')

        # query for playoffs
        sql = 'select team_name from teams where (WCWin = \'y\' or DivWin = \'y\' or LgWin = \'y\') and yearId = %s;'
        cur.execute(sql, year)
        results = cur.fetchall()
        con.commit()
        return results

'''
function: getTeams()
params: params which has years and team
return: bool of whether team is in the playoffs
searches teams in playoffs and tells whether team is in the playoffs
'''
def inPlayOffs(params):
    con = connect()
    with con:
        cur = con.cursor()

        # set the database
        cur.execute('USE baseball')


        # save the playoff data from database
        sql = 'select team_name from teams where (WCWin = \'y\' or DivWin = \'y\' or LgWin = \'y\') and yearId = %s and team_name = %s;'
        cur.execute(sql, params)
        results = cur.fetchall()
        con.commit()
        if len(results) == 0:
            return 0
        else:
            return 1
'''
function: getWinner()
params: yearid
return: winner of playoffs in this year
searches data for winner of playoffs in a specified year
'''
def getWinner(year):
    con = connect()
    with con:
        cur = con.cursor()

        # set the database
        cur.execute('USE baseball')

        # search for the winner
        sql = 'select team_name from teams where (WCWin = \'y\' or DivWin = \'y\' or LgWin = \'y\') and yearId = %s and WSWin = \'y\';'
        cur.execute(sql, year)
        results = cur.fetchall()
        con.commit()
        return results

