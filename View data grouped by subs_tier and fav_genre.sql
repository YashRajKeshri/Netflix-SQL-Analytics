use netflix_db;
SELECT * FROM netflix_users;
select count(*),Subscription_Type, Favorite_Genre,
 round(avg(Watch_Time_Hours))as 'Average watch time'from netflix_users
 group by Subscription_Type, Favorite_Genre
order by Subscription_Type, 'Average watch time' desc;
