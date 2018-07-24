If only CSV operation perform:
python3 currensee.py -db_operation 0 -csv_operation 1 -user root -host localhost -port 3306 -password TBD -database earth -path /tmp/

If only DB operation to perform :
python3 currensee.py -db_operation 1 -csv_operation 0 -user root -host localhost -port 3306 -password TBD -database earth -path /tmp/

If CSV and DB operations to perform :
python3 currensee.py -db_operation 1 -csv_operation 1 -user root -host localhost -port 3306 -password TBD -database earth -path /tmp/

