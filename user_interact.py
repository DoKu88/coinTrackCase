from db_interface import DataBaseInterface
from db_updater import DataBaseUpdater
import time
from datetime import datetime

class DateEncap:
    def __init__(self, year, month, day, hour=0, minute=0, second=0):
        self.dateDict = dict()

        self.dateDict['year']   = year
        self.dateDict['month']  = month
        self.dateDict['day']    = day
        self.dateDict['hour']   = hour
        self.dateDict['minute'] = minute
        self.dateDict['second'] = second

    def get_data(self):
        return self.dateDict

    def get_formatted_date(self):

        dateStr = datetime(self.dateDict['year'], self.dateDict['month'],
                 self.dateDict['day'], self.dateDict['hour'], self.dateDict['minute'],
                 self.dateDict['second']).strftime('%Y-%m-%d %H:%M:%S')

        return dateStr

class UserInterface:
    def __init__(self):
        self.database = DataBaseInterface()
        self.updater  = DataBaseUpdater()
        self.tableNames = ["AddressBook", "Balances", "Transactions"]

    # basically also add_user
    def add_address(self, addr, user):
        self.database.add_address_wrapper(addr, user)
        self.updater.update_database(addr)

    def add_user(self, addr, user):
        self.add_address(addr, user)

    def get_users(self):
        return self.database.get_users()

    def get_all_addresses(self):
        return self.database.get_all_addresses()

    def del_address(self, addr):
        self.database.del_address(addr)

    def del_user(self, user):
        self.database.del_user(user)

    def get_user_addrs(self, user):
        return self.database.get_addresses(user)

    def get_balance_addr(self, addr):
        balance_usd, balance_btc = self.database.get_balance_per_address(addr) 
        return [balance_usd, balance_btc]

    def get_balance_user(self, user):
        balance_usd, balance_btc = self.database.get_balance_per_user(user)
        return [balance_usd, balance_btc]

    def get_balance_addr_range(self, addr, startDate, endDate):
        startDate1 = startDate.get_formatted_date()
        endDate1   = endDate.get_formatted_date()

    # get all transactions for a bitcoin address within certain dates
    def get_balance_addr_range(self, addr, startDate, endDate):

        startDate1 = startDate.get_formatted_date()
        endDate1   = endDate.get_formatted_date()

        balances = self.database.get_balance_per_address_dateRange(addr,
                startDate1, endDate1)

        print('balances for address: ', addr, ' in range', startDate1, ' ',
                endDate1)

        for bals in balances:
            print('balance : ')
            print(bal)

        return balances

    def get_balance_user_range(self, user, startDate, endDate):
        startDate1 = startDate.get_formatted_date()
        endDate1   = endDate.get_formatted_date()

        balances = self.database.get_balance_per_user_dateRange(user,
                startDate1, endDate1)

        print('balances for user: ', user, ' in range', startDate1, ' ',
                endDate1)

        for bals in balances:
            print('balance : ')
            print(bals)

        return transactions

    def get_transactions_addr(self, addr):
        last_transaction = self.database.get_trans_per_address(addr)

        print('last transaction: ', last_transaction)

        return last_transaction

    # get a transaction for every bitcoin address the user has 
    def get_transactions_user(self, user):
        last_transactions = self.database.get_trans_per_user(user)

        print('last transactions for user: ', user)
        for trans in last_transactions:
            print('transaction: ')
            print(trans)

        return last_transactions

    # get all transactions for a bitcoin address within certain dates
    def get_transactions_addr_range(self, addr, startDate, endDate):

        startDate1 = startDate.get_formatted_date()
        endDate1   = endDate.get_formatted_date()

        transactions = self.database.get_trans_per_address_dateRange(addr,
                startDate1, endDate1)

        print('transactions for address: ', addr, ' in range', startDate1, ' ',
                endDate1)

        for trans in transactions:
            print('transaction: ')
            print(trans)

        return transactions

    def get_transactions_user_range(self, user, startDate, endDate):
        startDate1 = startDate.get_formatted_date()
        endDate1   = endDate.get_formatted_date()

        transactions = self.database.get_trans_per_user_dateRange(user,
                startDate1, endDate1)

        print('transactions for user: ', user, ' in range', startDate1, ' ',
                endDate1)

        for trans in transactions:
            print('transaction: ')
            print(trans)

        return transactions

    def show_table(self, tableName):
        self.database.show_table(tableName)

    def list_table_names(self):
        print("Table Names:")

        for table in self.tableNames:
            print(table)


def main():

    # =========================================================================
    # Make UI object and list the tables that we have
    UI = UserInterface()
    UI.list_table_names()
    # =========================================================================

    # =========================================================================
    # Show Database before adding addressses
    print('Before adding addresses:')
    print('AddressBook')
    UI.show_table("AddressBook")
    print('-------------------')
    # =========================================================================

    # =========================================================================
    # Add users and bitcoin addresses 
    user1 = "Bobert"
    address = '3E8ociqZa9mZUSwGdSmAEMAoAxBK3FNDcd'
    address1 = 'bc1q0sg9rdst255gtldsmcf8rk0764avqy2h2ksqs5'

    user2 = "Nancy"
    address2 = '12xQ9k5ousS8MqNsMBqHKtjAtCuKezm2Ju'

    UI.add_user(address, user1)
    UI.add_address(address1, user1)

    UI.add_address(address2, user2)

    print('AddressBook after adding addr and users')
    UI.show_table("AddressBook")
    print('-------------------')
    import pdb; pdb.set_trace()
    
    print('Balances after adding addr and users')
    UI.show_table("Balances")
    print('-------------------')
    import pdb; pdb.set_trace()
    
    print('Transactions after adding addr and users')
    UI.show_table("Transactions")
    print('-------------------')
    import pdb; pdb.set_trace()
    # =========================================================================

    # =========================================================================
    # Get all Bitcoin Addresses for Bobert
    addresses = UI.get_user_addrs(user1)
    print(user1 + "'s Addresses: ", addresses)
    import pdb; pdb.set_trace()
    # =========================================================================

    # =========================================================================
    # Delete Bobert from DataBase and see that balances and transactions
    # changed too
    UI.del_user(user1)
    addresses = UI.get_user_addrs(user1)
    print("Bobert's Addresses: After del", addresses)
    import pdb; pdb.set_trace()
    
    print("Balances table after Bobert Deleted")
    UI.show_table("Balances")
    import pdb; pdb.set_trace()

    print("Transactions table after Bobert Deleted")
    UI.show_table("Transactions")
    import pdb; pdb.set_trace()
    # =========================================================================

    # =========================================================================
    # Add user1 bak into fold and get the balances
    UI.add_address(address1, user1)
    UI.add_address(address, user1)

    UI.get_balance_addr(address)
    UI.get_balance_user(user1)

    UI.get_transactions_addr(address)
    UI.get_transactions_user(user1)
    import pdb; pdb.set_trace()
    # =========================================================================

    # =========================================================================
    # Get ranged transactions 
    
    #endDate = DateEncap(2022, 6, 27)
    #startDate = DateEncap(2022, 6, 20)

    endDate = DateEncap(2021, 10, 28)
    startDate = DateEncap(2021, 10, 20)

    UI.get_transactions_addr_range(address, startDate, endDate)
    import pdb; pdb.set_trace()

    UI.get_transactions_user_range(user1, startDate, endDate)
    import pdb; pdb.set_trace()

    UI.show_table("Balances")
    import pdb; pdb.set_trace()
    # =========================================================================

    print('goodbye!')


if __name__ == "__main__":
    main()
