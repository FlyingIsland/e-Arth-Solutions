python3 amazon_price.py  --user root --host localhost --port 3306 --password TBD --database amazon --path /tmp
export MYSQL_PWD=
echo "show databases" | mysql --user root --host localhost --database earth
echo "show tables" | mysql --user root --host localhost --database earth
echo "desc product" | mysql --user root --host localhost --database earth
echo "select count(asin) from product;" | mysql --user root --host localhost --database earth

