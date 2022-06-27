from db_interface import DataBaseInterface
import time

class UserInterface:
    def __init__(self):
        self.database = DataBaseInterface()
        self.tableNames = ["AddressBook", "Balances", "Transactions"]

    # basically also add_user
    def add_address(self, addr, user):
        self.database.add_address_wrapper(addr, user)

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

    def show_table(self, tableName):
        self.database.show_table(tableName)

    # call update daemon manually
    def force_update(self):
        pass

    def list_table_names(self):
        print("Table Names:")

        for table in self.tableNames:
            print(table)


def main():

    UI = UserInterface()
    UI.list_table_names()

    print('Before adding addresses:')
    print('AddressBook')
    UI.show_table("AddressBook")
    print('-------------------')

    address = '3E8ociqZa9mZUSwGdSmAEMAoAxBK3FNDcd'
    address1 = 'bc1q0sg9rdst255gtldsmcf8rk0764avqy2h2ksqs5'
              #'bc1q0sg9rdst255gtldsmcf8rk0764avqy2h2ksqs5'
    user1 = "Bobert"

    UI.add_user(address, user1)
    UI.add_address(address1, user1)
    print('AddressBook after adding addr and users')
    UI.show_table("AddressBook")
    print('-------------------')

    # Get all Bitcoin Addresses for Bobert
    addresses = UI.get_user_addrs(user1)
    print(user1 + "'s Addresses: ", addresses)

    # Delete Bobert from DataBase and see what happens
    #UI.del_user(user1)
    #addresses = UI.get_user_addrs(user1)
    #print("Bobert's Addresses: After del", addresses)

    print("Balances table")
    UI.show_table("Balances")

    UI.get_balance_addr(address)
    UI.get_balance_user(user1)
    UI.get_transactions_addr(address)
    UI.get_transactions_user(user1)


if __name__ == "__main__":
    main()
