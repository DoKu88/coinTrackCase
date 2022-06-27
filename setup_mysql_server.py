import pymysql
import time
#import pymysql.connect

host = 'database-2.cji0mokilyxv.us-west-1.rds.amazonaws.com'
user = 'admin'
password = '12345678'
database_id = 'database-2'


connection = pymysql.connect(host=host, 
                             user=user, 
                             password=password)

mycursor = connection.cursor() 

#new_database = "CREATE DATABASE ExDataBase" + str(int(time.time()))
#mycursor.execute(new_database)

show_databases = "SHOW DATABASES"
mycursor.execute(show_databases) 

databaseList = mycursor.fetchall()
for database in databaseList:
    print(database)


dataBaseName = 'CoinData'

# if CoinData exists we need to drop it first 
del_database = "DROP DATABASE " + dataBaseName
mycursor.execute(del_database)

# create database 
new_database = "CREATE DATABASE " + dataBaseName
mycursor.execute(new_database)

# connect specificaly to new database 
use_database = "USE " + dataBaseName
mycursor.execute(use_database)

# create addressBook table in database 
# bit coin addresses are 34 characters
create_addressBook = "CREATE TABLE AddressBook (addr VARCHAR(128), user VARCHAR(34), PRIMARY KEY(addr))"
mycursor.execute(create_addressBook)

create_balances = "CREATE TABLE Balances(addr VARCHAR(128), time TIMESTAMP, balance_usd DECIMAL, balance_btc DECIMAL, PRIMARY KEY(addr, time), FOREIGN KEY (addr) REFERENCES AddressBook(addr) ON DELETE CASCADE)"
mycursor.execute(create_balances)

create_transactions = "CREATE TABLE Transactions(addr VARCHAR(128), hash VARCHAR(64), time TIMESTAMP, balance_change DECIMAL, block_id INT, PRIMARY KEY(addr, hash), FOREIGN KEY (addr) REFERENCES AddressBook(addr) ON DELETE CASCADE)"
mycursor.execute(create_transactions)


show_tables = "SHOW TABLES"
mycursor.execute(show_tables) 

tableList = mycursor.fetchall()
for table in tableList:
    print(table)

