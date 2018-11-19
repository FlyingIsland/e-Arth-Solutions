LOAD DATA INFILE './Inventory.csv'
INTO TABLE your_temp_table
FIELDS TERMINATED BY ','
(id, product, sku, department, quantity); 
