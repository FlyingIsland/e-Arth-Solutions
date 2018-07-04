python3 amazon_price.py  --user earth --host earth.delve.tech --password TBD --database earth --path /tmp
export MYSQL_PWD=
echo "show databases" | mysql --user root --host localhost --database earth
echo "show tables" | mysql --user root --host localhost --database earth
echo "desc product" | mysql --user root --host localhost --database earth
echo "select count(asin) from product;" | mysql --user root --host localhost --database earth

