Running the script :
python3 greatschools.py -url https://www.greatschools.org/schools/cities/California/CA/ -user root -host localhost -port 3306 -password S0lutions! -database greatschools -interval 5

Other info :
-interval parameter is of number od seconds to wailt after each request

The schema.sql under sql folder will create a database schema "greatschools" and create two tables "city" and "school". So while importing the sql file no need to specify the database schema name.

