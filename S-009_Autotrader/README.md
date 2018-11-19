Running the script : python3 autotrader.py -user root -host localhost -port 3306 -password TBD -database autotrader -interval 3

Other info : -interval parameter is of number of seconds to wailt after each request

The schema.sql under sql folder will create a database schema "autotrader" and create 3 tables "search", "listing" and "price". 
So while importing the sql file no need to specify the database schema name.
