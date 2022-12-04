from bs4 import BeautifulSoup
from bs4 import Comment
import requests
import math

def scrapeTeam(franchID, year, teams):
    row = {'teamID': teams[franchID][0], 'yearID': year, 'franchID': franchID, 'team_name': teams[franchID][1]}

    web_team = franchID

    url = 'https://www.baseball-reference.com/teams/' + web_team + '/' + str(year) + '.shtml'
    result = requests.get(url)

    team_page = BeautifulSoup(result.text, 'html.parser')

    summary = team_page.find(attrs={'data-template': 'Partials/Teams/Summary'})

    if(summary == None):
        web_team = teams[franchID][0]

        url = 'https://www.baseball-reference.com/teams/' + web_team + '/' + str(year) + '.shtml'
        result = requests.get(url)

        team_page = BeautifulSoup(result.text, 'html.parser')
        summary = team_page.find(attrs={'data-template': 'Partials/Teams/Summary'})


    # Parsing Record section of summary
    record = summary.find('strong', string='Record:').next_sibling
    record_s = record.split('\n')

    # team_rank, team_G, team_W, team_L
    if(len(record_s) == 10):
        row['team_rank'] = int(record_s[3].strip()[0:-2])
        if(row['team_rank'] == 1):
            row['DivWin'] = 'Y'
        else:
            row['DivWin'] = 'N'
        record_list = record_s[1].strip().split('-')
        row['team_W'] = int(record_list[0])
        row['team_L'] = int(record_list[1])
        row['team_G'] = int(record_list[0]) + int(record_list[1])

    # lgID, divId, 
    lg_div = record.next_sibling.string
    index = lg_div.index('_')
    if(index != -1):
        row['lgID'] = lg_div[0:index]
        row['divID'] = lg_div[index + 1:index + 2]

    # team_name
    heading = summary.find('h1').find_all('span')
    if(len(heading) >= 2):
        row['team_name'] = heading[1].string
    else:
        print('Could not find team_name')

    # team_attendance
    attendance = str(summary.find('strong', string='Attendance:').parent)
    attendance = attendance[attendance.index('</strong>') + len('</strong>'): attendance.index('(')].strip()
    a = ""
    for c in attendance:
        if c.isnumeric():
            a += c
    row['team_attendance'] = int(a)
    
    # park_name
    park_name = str(summary.find('strong', string='Ballpark:').parent)
    row['park_name'] = park_name[park_name.index('</strong>') + len('</strong>'): park_name.index('</p>')].strip()

    multi = str(summary.find('strong', string='Multi-year:').parent)
    # team_BPF
    temp = multi[multi.index('Batting - ') + len('Batting - '):]
    row['team_BPF'] = temp[: temp.index(',')].strip()

    # team_PPF
    temp = multi[multi.index('Pitching - ') + len('Pitching - '):]
    row['team_PPF'] = temp[: temp.index('<')].strip()

    # batting fields
    batting = team_page.find(id='team_batting').find(string='Team Totals').parent.parent
    row['team_R'] = int(batting.find(attrs={'data-stat': 'R'}).string)
    row['team_AB'] = int(batting.find(attrs={'data-stat': 'AB'}).string)
    row['team_H'] = int(batting.find(attrs={'data-stat': 'H'}).string)
    row['team_2B'] = int(batting.find(attrs={'data-stat': '2B'}).string)
    row['team_3B'] = int(batting.find(attrs={'data-stat': '3B'}).string)
    row['team_HR'] = int(batting.find(attrs={'data-stat': 'HR'}).string)
    row['team_BB'] = int(batting.find(attrs={'data-stat': 'BB'}).string)
    row['team_SO'] = int(batting.find(attrs={'data-stat': 'SO'}).string)
    row['team_SB'] = int(batting.find(attrs={'data-stat': 'SB'}).string)
    row['team_CS'] = int(batting.find(attrs={'data-stat': 'CS'}).string)
    row['team_HBP'] = int(batting.find(attrs={'data-stat': 'HBP'}).string)
    row['team_SF'] = int(batting.find(attrs={'data-stat': 'SF'}).string)

    # pitching fields
    pitching = team_page.find(id='team_pitching').find(string='Team Totals').parent.parent
    row['team_RA'] = int(pitching.find(attrs={'data-stat': 'R'}).string)
    row['team_ER'] = int(pitching.find(attrs={'data-stat': 'ER'}).string)
    row['team_ERA'] = float(pitching.find(attrs={'data-stat': 'earned_run_avg'}).string)
    row['team_CG'] = int(pitching.find(attrs={'data-stat': 'CG'}).string)
    row['team_SHO'] = int(pitching.find(attrs={'data-stat': 'SHO'}).string)
    row['team_SV'] = int(pitching.find(attrs={'data-stat': 'SV'}).string)
    row['team_IPouts'] = math.ceil(float(pitching.find(attrs={'data-stat': 'IP'}).string) * 3)
    row['team_HA'] = int(pitching.find(attrs={'data-stat': 'H'}).string)
    row['team_HRA'] = int(pitching.find(attrs={'data-stat': 'HR'}).string)
    row['team_BBA'] = int(pitching.find(attrs={'data-stat': 'BB'}).string)
    row['team_SOA'] = int(pitching.find(attrs={'data-stat': 'SO'}).string)

    # fielding fields
    url = 'https://www.baseball-reference.com/leagues/' + row['lgID'] + '/' + str(year) + '-standard-fielding.shtml'
    result = requests.get(url)
    fielding_page = BeautifulSoup(result.text, 'html.parser')

    fielding = fielding_page.find('table', id='teams_standard_fielding').find('tbody').find(string=row['team_name']).parent.parent.parent
    row['team_E'] = int(fielding.find(attrs={'data-stat': 'E_def'}).string)
    row['team_DP'] = int(fielding.find(attrs={'data-stat': 'DP_def'}).string)
    row['team_FP'] = float(fielding.find(attrs={'data-stat': 'fielding_perc'}).string)

    # win/loss
    url = 'https://www.baseball-reference.com/teams/' + web_team + '/' + str(year) + '-schedule-scores.shtml'
    result = requests.get(url)
    splits_page = BeautifulSoup(result.text, 'html.parser')

    win_loss = splits_page.find(id='all_win_loss').find_all(string=lambda text: isinstance(text, Comment))
    
    with open("temp.html", "w", encoding='utf-8') as file:
        file.write(str(win_loss))
    
    file.close()
    
    with open('temp.html', 'r') as f:
        splits_page = BeautifulSoup(f, 'html.parser')
    
    # team_G_home
    home_game_wins = splits_page.find('td', string='Home').next_sibling.next_sibling
    row['team_G_home'] = int(home_game_wins.string) + int(home_game_wins.next_sibling.next_sibling.string)


    # Post Season Games
    url = 'https://www.baseball-reference.com/leagues/majors/' + str(year) + '.shtml'
    result = requests.get(url)
    post_page = BeautifulSoup(result.text, 'html.parser')

    post_table = post_page.find(id='all_postseason').find_all(string=lambda text: isinstance(text, Comment))

    with open("temp.html", "w", encoding='utf-8') as file:
        file.write(str(post_table))
    
    file.close()
    
    with open('temp.html', 'r') as f:
        post_page = BeautifulSoup(f, 'html.parser')


    post = post_page.find_all('td')

    row['WSWin'] = 'N'
    row['LgWin'] = 'N'
    row['WCWin'] = 'N'

    for t_post in post:
        if t_post.string == 'World Series' and t_post.next_sibling.next_sibling.next_sibling.next_sibling.find('a').string == row['team_name']:
           row['WSWin'] = 'Y'
        if t_post.string == row['lgID'] + 'CS' and t_post.next_sibling.next_sibling.next_sibling.next_sibling.find('a').string == row['team_name']:
            row['LgWin'] = 'Y'
        if t_post.string == 'Wild Card Series' and t_post.next_sibling.next_sibling.next_sibling.next_sibling.find('a').string == row['team_name']:
            row['WCWin'] = 'Y'

    return row



def scrapePeople(year):
    rows = []

    url = 'https://www.baseball-reference.com/leagues/majors/' + year + '-debuts.shtml'

    result = requests.get(url)

    people_page = BeautifulSoup(result.text, 'html.parser')

    people = people_page.find(id="misc_bio").find('tbody').find_all('tr')

    for person in people:
        row = {}

        if person.find(attrs={'data-stat': 'ranker'})['scope'] == 'col':
            continue

        row['playerID'] = person.find(attrs={'data-stat': 'player'})['data-append-csv']

        birthdate = person.find(attrs={'data-stat': 'birthdate'})['csk'].split('-')
        row['birthYear'] = int(birthdate[0])
        row['birthMonth'] = int(birthdate[1])
        row['birthDay'] = int(birthdate[2])

        birthPlace = person.find(attrs={'data-stat': 'birthplace'})['csk'].split(', ')
        if len(birthPlace) == 3:
            row['birthCountry'] = birthPlace[0]
            row['birthState'] = birthPlace[1]
            row['birthCity'] = birthPlace[2]
        elif len(birthPlace) == 2:
            row['birthCountry'] = birthPlace[0]
            row['birthCity'] = birthPlace[1]

        name = person.find(attrs={'data-stat': 'player'})['csk'].split(',')
        row['nameFirst'] = name[1]
        row['nameLast'] = name[0]
        row['nameGiven'] = name[1] + " " + name[0]

        row['weight'] = int(person.find(attrs={'data-stat': 'weight'}).string)

        height = person.find(attrs={'data-stat': 'height'}).string.split('-')
        row['height'] = (int(height[0]) * 12) + int(height[1])

        row['bats'] = person.find(attrs={'data-stat': 'bats'})
        row['throws'] = person.find(attrs={'data-stat': 'throws'})

        row['debutDate'] = person.find(attrs={'data-stat': 'debut'})['csk']

        rows.append(row)

    return rows

    
def scrapeBatting(franchID, year, teams):
    row = {}
