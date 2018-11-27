Running the script :
python3 greatschools.py -url https://www.greatschools.org/schools/cities/California/CA/ -user root -host localhost -port 3306 -password TBD -database greatschools -interval 5 -skipcity 1

Other info :
-interval parameter is of number od seconds to wailt after each request
-skipcity => When 1 then skip the state and city extraction part and jump to school list extraction part
	  => When 0 then will extract te state and city also. And then do school list extraction part

The schema.sql under sql folder will create a database schema "greatschools" and create two tables "city" and "school". So while importing the sql file no need to specify the database schema name.

update city set list_school = 1 where city_url = 'https://www.greatschools.org/california/agoura-hills/';
