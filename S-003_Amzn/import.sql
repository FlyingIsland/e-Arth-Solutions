LOAD DATA LOCAL INFILE './Inventory.csv'
INTO TABLE product
FIELDS TERMINATED BY ','
(asin); 
