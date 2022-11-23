ALTER TABLE batting RENAME COLUMN ID TO batting_id;
ALTER TABLE allstarfull RENAME COLUMN ID TO allstarfull_id;
ALTER TABLE appearances RENAME COLUMN ID TO appearances_id;
ALTER TABLE awards RENAME COLUMN ID TO awards_id;
ALTER TABLE awardsshare RENAME COLUMN ID TO awardsshare_id;
ALTER TABLE battingpost RENAME COLUMN ID TO battingpost_id;
ALTER TABLE collegeplaying RENAME COLUMN ID TO collegeplaying_id;
ALTER TABLE divisions RENAME COLUMN ID TO divisions_id;
ALTER TABLE fielding RENAME COLUMN ID TO fielding_id;
ALTER TABLE fieldingpost RENAME COLUMN ID TO fieldingpost_id;
ALTER TABLE halloffame RENAME COLUMN ID TO halloffame_id;
ALTER TABLE homegames RENAME COLUMN ID TO homegames_id;
ALTER TABLE managers RENAME COLUMN ID TO managers_id;
ALTER TABLE pitchingpost RENAME COLUMN ID TO pitchingpost_id;
ALTER TABLE salaries RENAME COLUMN ID TO salaries_id;
ALTER TABLE seriespost RENAME COLUMN ID TO seriespost_id;
ALTER TABLE teams RENAME COLUMN ID TO teams_id;

//fix inconsistency between naming of awards
update awards set awardID = 'MVP' where awardID = 'Most Valuable Player';
update awards set awardID = 'Cy Young' where awardID = 'Cy Young Award';