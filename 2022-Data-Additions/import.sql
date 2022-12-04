-- Make sure this is in the same directory as database to run it

LOAD DATA LOCAL INFILE 'teams.csv' 
INTO TABLE teams 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 LINES 
(teamID,yearID,lgID,divID,franchID,team_name,team_rank,team_G,team_G_home,team_W,team_L,DivWin,WCWin,LgWin,WSWin,team_R,team_AB,team_H,team_2B,team_3B,team_HR,team_BB,team_SO,team_SB,team_CS,team_HBP,team_SF,team_RA,team_ER,team_ERA,team_CG,team_SHO,team_SV,team_IPouts,team_HA,team_HRA,team_BBA,team_SOA,team_E,team_DP,team_FP,park_name,team_attendance,team_BPF,team_PPF);

LOAD DATA LOCAL INFILE 'people.csv' 
INTO TABLE people 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 LINES 
(playerID,birthYear,birthMonth,birthDay,birthCountry,birthState,birthCity,deathYear,deathMonth,deathCountry,deathState,deathCity,nameFirst,nameLast,nameGiven,weight,height,bats,throws,debutDate,finalGameDate);