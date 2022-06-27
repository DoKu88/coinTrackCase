import pymysql
from datetime import datetime
import sys

# =============================================================================
# DATA BASE INTERACTIONS
# =============================================================================

class DataBaseInterface:
    def __init__(self, host=None, user=None, password=None, database_id=None,
                    dataBaseName=None):

        self.host = host
        if host is None:
            self.host = 'database-2.cji0mokilyxv.us-west-1.rds.amazonaws.com'

        self.user = user
        if user is None:
            self.user = 'admin'

        self.password = password
        if password is None:
            self.password = '12345678'

        self.database_id = database_id
        if database_id is None:
            self.database_id = 'database-2'

        self.dataBaseName = dataBaseName
        if dataBaseName is None:
            self.dataBaseName = 'CoinData'

    # get datetime formatted for sql
    def get_datetime(self):
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

        return formatted_date

    # standardize connecting to the mysql host
    # NOTE: Should we make object field???--------------------------------------
    def get_mysql_cursor(self):
        connection = pymysql.connect(host=self.host,
                                 user=self.user,
                                 password=self.password)

        mycursor = connection.cursor()
        use_database = "USE " + self.dataBaseName
        mycursor.execute(use_database)

        return mycursor, connection

    # display a table
    def show_table(self, tableName, mycursor=None):

        if mycursor is None:
            mycursor, connection = self.get_mysql_cursor()

        show_tables = "SELECT * FROM " + tableName
        mycursor.execute(show_tables)

        rows = mycursor.fetchall()
        for row in rows:
            print(row)

    # adds address and user to address book
    # Table: AddressBook
    # Columns: addr VARCHAR(34), user VARCHAR(34)
    def add_address(self, address, user1):

        mycursor, connection = self.get_mysql_cursor()

        add_address = 'INSERT INTO AddressBook (addr, user) VALUES ("' + address + '", "'+ user1 + '")'
        mycursor.execute(add_address)
        connection.commit()

        #self.show_table('AddressBook', mycursor)
        #self.show_table('AddressBook')

    def add_address_wrapper(self, address, user1):
        try:
            self.add_address(address, user1)
        except:
            print("AddressBook couldn't be added to")
            print("Address: ", address)
            print("user: ", user1)

    # from the address book return all addresses, for a given user
    def get_addresses(self, user):
        mycursor, connection = self.get_mysql_cursor()

        get_addr_query = 'SELECT addr FROM AddressBook WHERE user="'+ user + '";'
        mycursor.execute(get_addr_query)
        rows = mycursor.fetchall()

        addresses = []

        for row in rows:
            addresses.append(row[0])

        print('addresses: ', addresses)

        return addresses

    # from the address book return all users
    def get_all_addresses(self):
        mycursor, connection = self.get_mysql_cursor()

        get_addr_query = 'SELECT addr FROM AddressBook;' 
        mycursor.execute(get_addr_query)
        rows = mycursor.fetchall()

        addresses = []

        for row in rows:
            addresses.append(row[0])

        print('addresses: ', addresses)

        return addresses 

    # from the address book return all users
    def get_users(self):
        mycursor, connection = self.get_mysql_cursor()

        get_user_query = 'SELECT DISTINCT(user) FROM AddressBook;' 
        mycursor.execute(get_user_query)
        rows = mycursor.fetchall()

        users = []

        for row in rows:
            users.append(row[0])

        print('users: ', users)

        return users

    # adds address and user to address book
    # Table: Balances
    # Columns: addr VARCHAR(34), time TIMESTAMP, balance_usd DECIMAL, balance_btc
    # DECIMAL
    def add_balance(self, address, balance_btc, balance_usd, datetime=None):

        mycursor, connection = self.get_mysql_cursor()
        if datetime is None:
            datetime = get_datetime()

        add_balance = 'INSERT INTO Balances (addr, time, balance_usd, balance_btc) VALUES ("' + address + '", "'+ datetime + '", '+ str(balance_usd) + ',' + str(balance_btc) + ')'
        mycursor.execute(add_balance)
        connection.commit()

        #self.show_table('Balances')

    def add_balance_wrapper(self, address, balance_btc, balance_usd, datetime=None):
        try:
            self.add_balance(address, balance_btc, balance_usd, datetime)
        except:
            print("Balances couldn't be added to")
            print("Address: ", address)
            print("balance_btc: ", balance_btc)
            print("balance_usd: ", balance_usd)
            print("datetime: ", datetime)

    def get_balance_per_address(self, address):
        pass

    def get_balance_per_user(self, user):
        pass

    # adds address and user to address book
    # Table: Transactions
    # Columns: addr VARCHAR(34), hash VARCHAR(64), time TIMESTAMP
    # DECIMAL
    def add_transaction(self, address, transData, mycursor=None, show=True):

        connection = None
        if mycursor is None:
            mycursor, connection = self.get_mysql_cursor()
        block_id = transData['block_id']
        hash1    = transData['hash']
        time     = transData['time']
        balance_change = transData['balance_change']

        add_transaction= 'INSERT INTO Transactions (addr, hash, time, balance_change, block_id) VALUES ("'+ address + '", "'+ hash1 + '", "'+ time + '", ' + str(balance_change) + ', ' + str(block_id) + ')'
        mycursor.execute(add_transaction)

        if connection is not None:
            connection.commit()

        if show:
            self.show_table('Transactions', mycursor)

    def add_transaction_wrapper(self, address, transData, mycursor=None, show=True):
        try:
            self.add_transaction(address, transData, mycursor=None, show=True)
        except:
            print("Transactions couldn't be added to")
            print("Address: ", address)
            print("transData: ", transData)

    # iterate through transactions
    def add_n_transactions(self, address, data_dict, n=None):
        tot_trans = data_dict['num_transactions']
        if n is None:
            n = len(data_dict['transactions'])

        mycursor, connection = self.get_mysql_cursor()
        for i in range(n):
            self.add_transaction_wrapper(address, data_dict['transactions'][i], mycursor,
                    show=False)

        #self.show_table('Transactions', mycursor)
        connection.commit()
        mycursor.close()

    def get_trans_per_address(self, address):
        pass

    def get_trans_per_user(self, user):
        pass

    # since address in AddressBook is foreign key for everyone and
    # deletes on cascade, only need to delete from AddressBook
    def del_address(self, address):
        mycursor, connection = self.get_mysql_cursor()

        del_addr_query = 'DELETE FROM AddressBook WHERE addr="'+ address + '";'
        mycursor.execute(del_addr_query)
        connection.commit()

    # since address in AddressBook is foreign key for everyone and
    # deletes on cascade, only need to delete from AddressBook
    # will delete all addresses associated with user
    def del_user(self, user):
        mycursor, connection = self.get_mysql_cursor()

        del_user_query = 'DELETE FROM AddressBook WHERE user="'+ user + '";'
        mycursor.execute(del_user_query)
        connection.commit()

