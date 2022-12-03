# seperate awardid and award name attributes
Alter table awards rename column awardID to award_name;
Alter table awards rename column ID to award_id;
# move repeated playerid and notes attribute to new table
create table awardees as select playerID, notes, award_id from awards where notes != '\n';
alter table awardsshare add column award_id int(12);
update awardsshare aws inner join awards aw on aws.playerID = aw.playerID and aws.yearID = aw.yearID and aw.award_name = aws.awardID set aws.award_id = aw.award_id;
# remove repeated columns
alter table awardsshare drop column yearId, drop Column lgId, drop column awardID;
alter table awards drop foreign key fk_awd_peo;
alter table awards drop column playerId, drop Column notes;