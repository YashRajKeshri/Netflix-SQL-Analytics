use netflix_db;
select * from netflix_users;
select count(*)as 'Total users', Country, Subscription_Type, round(avg(Age),1)as 'Average Age',
round(avg(Watch_Time_Hours))as 'Average Watch Hours'
from netflix_users
group by  Country , Subscription_Type
order by Country;