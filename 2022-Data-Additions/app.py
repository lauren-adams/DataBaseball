from scraperHelper import scrapeTeam, scrapePeople
import pandas as pd;
from sqlite3 import Cursor
import pymysql
import config as cfg
import time

teamColumns = ['teamID', 'yearID', 'lgID', 'divID', 'franchID', 'team_name', 'team_rank', 'team_G', 'team_G_home',
              'team_W', 'team_L', 'DivWin', 'WCWin', 'LgWin', 'WSWin', 'team_R', 'team_AB', 'team_H', 'team_2B',
              'team_3B', 'team_HR', 'team_BB', 'team_SO', 'team_SB', 'team_CS', 'team_HBP', 'team_SF', 'team_RA',
              'team_ER', 'team_ERA', 'team_CG', 'team_SHO', 'team_SV', 'team_IPouts', 'team_HA', 'team_HRA',
              'team_BBA', 'team_SOA', 'team_E', 'team_DP', 'team_FP', 'park_name', 'team_attendance', 'team_BPF',
              'team_PPF']

            
peopleColumns = ['playerID', 'birthYear', 'birthMonth', 'birthDay', 'birthCountry', 'birthState', 'birthCity',
                 'deathYear', 'deathMonth', 'deathCountry', 'deathState', 'deathCity', 'nameFirst', 'nameLast',
                 'nameGiven', 'weight', 'height', 'bats', 'throws', 'debutDate', 'finalGameDate']

# franchID mapped to [teamID, team_name]
teams = {}

# Create franchID/teamID mapping from 2021 data
params = []
heading = []

con = pymysql.connect(host=cfg.mysql['location'], user=cfg.mysql['user'], password=cfg.mysql['password'], database=cfg.mysql['database'])

try:
    cur = con.cursor()

    sql = "SELECT distinct franchID, teamID, team_name FROM teams where yearID = 2021"
    cur.execute(sql)

    data = cur.fetchall()

    # {franchID, [teamID, team_name]}
    for r in data:
        teams[r[0]] = [r[1], r[2]]

except Exception:
    con.rollback()
    print("Database exception.")
    raise
else:
    con.commit()
finally:
    con.close()


# TEAMS ///////////////////////////////////////////

# Add scraped data to csv file
if (cfg.teams['filename_read'] == ''):
    df = pd.DataFrame(columns=range(len(teamColumns)))
    df.columns = teamColumns
else:
    df = pd.read_csv(cfg.teams['filename_read'])

for f in teams.keys():
    if f not in df['franchID'].values:
        try:
            row = scrapeTeam(f, 2022, teams)
        except Exception  as e:
            print(e)
            break

        df = pd.concat([df, pd.DataFrame(row, index=[0])], ignore_index=True)
        print(f + ' was added.')
        time.sleep(10)
    
    else:
        print(f + ' already existed.')



# Save csv file
filename_out = 'output.csv'
if cfg.teams['filename_save'] != '':
    filename_out = cfg.teams['filename_save']
    
df.to_csv(filename_out, index=False)

# PEOPLE ///////////////////////////////////////////

if (cfg.people['filename_read'] == ''):
    df = pd.DataFrame(columns=range(len(peopleColumns)))
    df.columns = peopleColumns
else:
    df = pd.read_csv(cfg.people['filename_read'])

teamRows = []
try:
    teamRows = scrapePeople(2022)
except Exception  as e:
    print(e)

for row in teamRows:
    df = pd.concat([df, pd.DataFrame(row, index=[0])], ignore_index=True)


# Save csv file
filename_out = 'output.csv'
if cfg.people['filename_save'] != '':
    filename_out = cfg.people['filename_save']
    
df.to_csv(filename_out, index=False)