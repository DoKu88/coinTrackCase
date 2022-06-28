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
    # NOTE: Do not make object field so that if we don't want to commit
    # changes we don't have to, also makes sure that that connection dies
    def get_mysql_cursor(self):
        # connect to SQL server on AWS
        connection = pymysql.connect(host=self.host,
                                 user=self.user,
                                 password=self.password)

        mycursor = connection.cursor()

        # make sure we use our database
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

        #print('addresses: ', addresses)

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

        #print('addresses: ', addresses)

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

        #print('users: ', users)

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

    def add_balance_wrapper(self, address, balance_btc, balance_usd, datetime=None):
        try:
            self.add_balance(address, balance_btc, balance_usd, datetime)
        except:
            print("Balances couldn't be added to")
            print("Address: ", address)
            print("balance_btc: ", balance_btc)
            print("balance_usd: ", balance_usd)
            print("datetime: ", datetime)

    # Need to get latest balance from balance table
    def get_balance_per_address(self, address):
        mycursor, connection = self.get_mysql_cursor()

        '''
        SELECT balance_usd
        FROM Balances AS B1
        INNER JOIN
        (SELECT DISTINCT addr, MAX(time) as maxTime
            FROM Balances
            GROUP BY addr) AS B2
        ON B1.addr = B2.addr AND B1.time = B2.maxTime
        WHERE B1.addr = "address"

        '''

        get_balance = 'SELECT balance_usd '
        get_balance = get_balance + 'FROM Balances AS B1 '
        get_balance = get_balance + 'INNER JOIN '
        get_balance = get_balance + '(SELECT DISTINCT addr, MAX(time) as maxTime '
        get_balance = get_balance + 'FROM Balances '
        get_balance = get_balance + 'GROUP BY addr) AS B2 '
        get_balance = get_balance + 'ON B1.addr = B2.addr AND B1.time = B2.maxTime '
        get_balance = get_balance + 'WHERE B1.addr = "' + address + '";'

        mycursor.execute(get_balance)
        balance_usd = mycursor.fetchone()

        #print('balance_usd: ', balance_usd)
        balance_usd = float(balance_usd[0])

        get_balance = 'SELECT balance_btc '
        get_balance = get_balance + 'FROM Balances AS B1 '
        get_balance = get_balance + 'INNER JOIN '
        get_balance = get_balance + '(SELECT DISTINCT addr, MAX(time) as maxTime '
        get_balance = get_balance + 'FROM Balances '
        get_balance = get_balance + 'GROUP BY addr) AS B2 '
        get_balance = get_balance + 'ON B1.addr = B2.addr AND B1.time = B2.maxTime '
        get_balance = get_balance + 'WHERE B1.addr = "' + address + '";'

        mycursor.execute(get_balance)
        balance_btc = mycursor.fetchone()
        
        #print('balance_btc: ', balance_btc)
        balance_btc = float(balance_btc[0])

        return balance_usd, balance_btc

    
    def get_balance_per_user(self, user):
        
        addresses = self.get_addresses(user)

        balance_usd, balance_btc = 0,0
        for addr in addresses:
            bal_usd, bal_btc = self.get_balance_per_address(addr)
            balance_usd += bal_usd
            balance_btc += bal_btc
            
        return balance_usd, balance_btc

    # requirements state to grab the current transaction, interpret as the 
    # last transaction that occurred
    def get_balance_per_user_dateRange(self, user, startDate, endDate):
        addresses = self.get_addresses(user)

        balances = []
        for addr in addresses:
            balData = get_balance_per_address_dateRange(self, address, startDate, endDate)
            balances.extend(balData)

        return balances

    # requirements state to grab the current transaction, interpret as the 
    # last transaction that occurred
    def get_balance_per_address_dateRange(self, address, startDate, endDate):
        mycursor, connection = self.get_mysql_cursor()

        '''
        SELECT addr, balance_usd, balance_btc 
        FROM Balances
        WHERE addr = "address" AND time BETWEEN startDate AND endDate
        '''

        get_transaction = "SELECT addr, balance_usd, balance_btc, time "
        get_transaction = get_transaction + "FROM Balances"
        get_transaction = get_transaction + 'WHERE addr = "' + address + '" '
        get_transaction = get_transaction + 'AND time BETWEEN "' + startDate + '" AND "' + endDate + '";'
        
        mycursor.execute(get_transaction)
        bal_res = mycursor.fetchall()

        balances = []
    
        for bal in bal_res:
            #print(trans)

            balData = dict()
            balData['address'] = bal[0]
            balData['balance_usd'] = bal[1]
            balData['balance_btc'] = bal[2]
            balData['time'] = bal[3]
            balances.append(balData)
        
        return balances
    
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
            self.add_transaction(address, transData, mycursor=None, show=show)
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

    # requirements state to grab the current transaction, interpret as the 
    # last transaction that occurred
    def get_trans_per_address(self, address):
        mycursor, connection = self.get_mysql_cursor()

        '''
        SELECT T1.addr AS addr, T1.hash AS hash, T1.time AS time, T1.balance_change AS balance_change, T1.block_id AS block_id 
        FROM Transactions AS T1
        INNER JOIN
        (SELECT DISTINCT addr, MAX(time) as maxTime
            FROM Transactions
            GROUP BY addr) AS T2
        ON T1.addr = T2.addr AND T1.time = T2.maxTime
        WHERE T1.addr = "address"


        '''

        get_transaction = "SELECT T1.addr AS addr1, T1.hash AS hash, T1.time AS time1, T1.balance_change AS balance_change, T1.block_id AS block_id "
        get_transaction = get_transaction + "FROM Transactions AS T1 "
        get_transaction = get_transaction + "INNER JOIN "
        get_transaction = get_transaction + "(SELECT DISTINCT addr, MAX(time) as maxTime FROM Transactions GROUP BY addr) AS T2 "
        get_transaction = get_transaction + "ON T1.addr = T2.addr AND T1.time = T2.maxTime "
        get_transaction = get_transaction + 'WHERE T1.addr = "' + address + '";'
        
        mycursor.execute(get_transaction)
        last_trans = mycursor.fetchone()

        transData = dict()
        transData['address'] = last_trans[0]
        transData['hash'] = last_trans[1]
        transData['time'] = last_trans[2]
        transData['balance_change'] = float(last_trans[3])
        transData['block_id'] = last_trans[4]
        
        return transData

    # requirements state to grab the current transaction, interpret as the 
    # last transaction that occurred
    def get_trans_per_address_dateRange(self, address, startDate, endDate):
        mycursor, connection = self.get_mysql_cursor()

        '''
        SELECT addr, hash, time, balance_change, block_id
        FROM Transactions 
        WHERE T1.addr = "address" AND time BETWEEN startDate AND endDate
        '''

        get_transaction = "SELECT addr, hash, time, balance_change, block_id "
        get_transaction = get_transaction + "FROM Transactions "
        get_transaction = get_transaction + 'WHERE addr = "' + address + '" '
        get_transaction = get_transaction + 'AND time BETWEEN "' + startDate + '" AND "' + endDate + '";'
        
        mycursor.execute(get_transaction)
        trans_res = mycursor.fetchall()

        transactions = []
    
        for trans in trans_res:
            #print(trans)

            transData = dict()
            transData['address'] = trans[0]
            transData['hash'] = trans[1]
            transData['time'] = trans[2]
            transData['balance_change'] = float(trans[3])
            transData['block_id'] = trans[4]
            transactions.append(transData)
        
        return transactions

    # get each of the last transactions per Bitcoin Address
    def get_trans_per_user(self, user):
        addresses = self.get_addresses(user)

        last_trans = [] 
        for addr in addresses:
            trans = self.get_trans_per_address(addr)
            last_trans.append(trans)
            
        return last_trans

    # get each of the last transactions per Bitcoin Address
    def get_trans_per_user_dateRange(self, user, startDate, endDate):
        addresses = self.get_addresses(user)

        last_trans = [] 
        for addr in addresses:
            trans = self.get_trans_per_address_dateRange(addr, startDate, endDate)
            last_trans.extend(trans)
            
        return last_trans

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
