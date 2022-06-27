# import urllib library
from urllib.request import urlopen
import json
import pymysql
from datetime import datetime

host = 'database-2.cji0mokilyxv.us-west-1.rds.amazonaws.com'
user = 'admin'
password = '12345678'
database_id = 'database-2'
dataBaseName = 'CoinData'

# get datetime formatted for sql 
def get_datetime():
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    
    return formatted_date

def get_url_data(url1):
    # store the response of URL
    response = urlopen(url1)
    # storing the JSON response
    # from url in data
    data_json = json.loads(response.read())

    return data_json

def get_data_address(url_base, address):
    url_access = url_base + address
    data_json = get_url_data(url_access)
    data_address, data_context = data_json['data'][address], data_json['context']

    balance, balance_usd = get_balance(data_address)
    transactions = get_transactions(data_address)

    data_dict = dict()
    data_dict['balance'] = balance
    data_dict['balance_usd'] = balance_usd
    data_dict['transactions'],  data_dict['num_transactions'] = transactions

    return data_dict

# per address get the balance
def get_balance(data_address):
    balance = data_address['address']['balance']
    balance_usd = data_address['address']['balance_usd']

    return balance, balance_usd

# per address get all (last 100) transactions
def get_transactions(data_address):
    transactions = data_address['transactions']
    num_transactions = data_address['address']['transaction_count']

    return transactions, num_transactions

# standardize connecting to the mysql host 
def get_mysql_cursor():
    connection = pymysql.connect(host=host,
                             user=user,
                             password=password)

    mycursor = connection.cursor()
    use_database = "USE " + dataBaseName
    mycursor.execute(use_database)

    return mycursor

# display a table
def show_table(tableName, mycursor=None):

    if mycursor is None:
        mycursor = get_mysql_cursor()

    show_tables = "SELECT * FROM " + tableName
    mycursor.execute(show_tables)
    
    rows = mycursor.fetchall()
    for row in rows:
        print(row)


# adds address and user to address book
# Table: AddressBook
# Columns: addr VARCHAR(34), user VARCHAR(34)
def add_address(address, user1):

    mycursor = get_mysql_cursor()

    add_address = 'INSERT INTO AddressBook (addr, user) VALUES ("' + address + '", "'+ user1 + '")'
    mycursor.execute(add_address)

    show_table('AddressBook', mycursor)
    
# adds address and user to address book
# Table: Balances
# Columns: addr VARCHAR(34), time TIMESTAMP, balance_usd DECIMAL, balance_btc
# DECIMAL
def add_balance(address, balance_btc, balance_usd, datetime=None):

    mycursor = get_mysql_cursor()
    if datetime is None:
        datetime = get_datetime()

    add_balance = 'INSERT INTO Balances (addr, time, balance_usd, balance_btc) VALUES ("' + address + '", "'+ datetime + '", '+ str(balance_usd) + ',' + str(balance_btc) + ')'
    mycursor.execute(add_balance)

    show_table('Balances', mycursor)

# adds address and user to address book
# Table: Transactions
# Columns: addr VARCHAR(34), hash VARCHAR(64), time TIMESTAMP
# DECIMAL
def add_transaction(address, hash1, datetime=None):

    mycursor = get_mysql_cursor()
    if datetime is None:
        datetime = get_datetime()

    add_transaction= 'INSERT INTO Transactions (addr, hash, time) VALUES ("'+ address + '", "'+ hash1 + '", "'+ datetime + '")'
    mycursor.execute(add_transaction)

    show_table('Transactions', mycursor)

# from the address book return all addresses
def get_addresses():
    pass

# from the address book, get the next address
def get_next_address(iterator1):
    pass


def main():
    print('Hello world')

    # store the URL in url as
    # parameter for urlopen
    url_base = 'https://api.blockchair.com/bitcoin/dashboards/address/'
    address = '3E8ociqZa9mZUSwGdSmAEMAoAxBK3FNDcd'
    user1 = "Bobert"
    add_address(address, user1)   
    data_dict = get_data_address(url_base, address)

    datetime = get_datetime() 
    add_balance(address, data_dict['balance'], data_dict['balance_usd'], datetime)
    add_transaction(address, data_dict['transactions'][-1], datetime)

    import pdb; pdb.set_trace()
    
    url = url_base + address
    
    # store the response of URL
    response = urlopen(url)
    
    # storing the JSON response
    # from url in data
    data_json = json.loads(response.read())
    
    # print the json response
    print(data_json)
    
    
    print('ahoy')


if __name__ == "__main__":
    main()
