from db_interface import DataBaseInterface 
from blockChair_interface import BlockChairInterface
import time

class DataBaseUpdater:
    def __init__(self, sleepTime=5):
        self.last_numTrans = dict()
        self.last_diff = dict()
        self.sleepTime = sleepTime
        # make objects so that we can interact with the web API and 
        # our database
        self.database = DataBaseInterface()
        self.webAPI   = BlockChairInterface()

    # determine which addresses need to be updated
    # run until one needs to be updated since daemon
    def need_update(self):
        address_update = []
        go = True
        while go:
            time.sleep(self.sleepTime)
            for address in self.last_numTrans:

                # see if there has been more transactions 
                # if so return since we need to update said address
                num_trans = self.webAPI.get_num_transactions(address)
                if self.last_numTrans[address] < num_trans:
                    self.last_diff = num_trans - self.last_numTrans[address]
                    self.last_numTrans[address] = num_trans
                    go = False
                    address_update.append(address)
                    
        return address_update
    
    # for an address update the database 
    def update_database(self, addr):
        # get data for address from webAPI
        num_update = self.last_diff[addr]
        data_dict, data_address = self.webAPI.get_data_address(address,
                                                    num_trans=num_update)

        # update Balance and Transaction Databases
        datetime = data_dict['transactions'][0]['time']
        self.database.add_balance_wrapper(address, data_dict['balance'], 
                                        data_dict['balance_usd'], datetime)


        # update the tranaction data base with the last num_update entries
        self.database.add_n_transactions(address, data_dict, num_update)

    # basically also add_user
    def add_address(self, addr, user):
        self.database.add_address_wrapper(addr, user)

    def del_address(self, addr):
        self.database.del_address(addr)

    def del_user(self, user):
        self.database.del_user(user)



def main():
    updater = DataBaseUpdater() 

    # run this like a Daemon where basically we're always looking to update
    # the database by seeing if any new info came in
    while True:
        addresses = updater.need_update()
    
        for addr in addresses:
            updater.update_database(addr)

    database.show_table("AddressBook")

    # add BitCoin Addresses Per User to DataBase
    address = '3E8ociqZa9mZUSwGdSmAEMAoAxBK3FNDcd'
    address1 = 'bc1q0sg9rdst255gtldsmcf8rk0764avqy2h2ksqs5'
    user1 = "Bobert"
    database.add_address_wrapper(address, user1)
    database.add_address_wrapper(address1, user1)
    print("Address book contents:")
    database.show_table("AddressBook")
    
    # get data for address from webAPI
    data_dict, data_address = webAPI.get_data_address(address)

    # update database with balances and transactions for each address
    datetime = data_dict['transactions'][0]['time']
    database.add_balance_wrapper(address, data_dict['balance'], 
                                    data_dict['balance_usd'], datetime)
    database.add_n_transactions(address, data_dict, 10)
    #database.add_transaction(address, data_dict['transactions'][-1])

    # Get all Bitcoin Addresses for Bobert
    addresses = database.get_addresses(user1)
    print("Bobert's Addresses: ", addresses)

    # Delete Bobert from DataBase and see what happens
    database.del_user(user1)
    addresses = database.get_addresses(user1)
    print("Bobert's Addresses: After del", addresses)

    print("Balances table")
    database.show_table("Balances")



if __name__ == "__main__":
    main()

