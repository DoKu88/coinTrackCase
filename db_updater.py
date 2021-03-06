from db_interface import DataBaseInterface 
from blockChair_interface import BlockChairInterface
import time

class DataBaseUpdater:
    def __init__(self, sleepTime=5):

        # key address, value number of transactions
        self.last_numTrans = dict()
        # key address, value difference between # of current and last trans
        self.last_diff = dict()
        
        self.sleepTime = sleepTime
        # make objects so that we can interact with the web API and 
        # our database
        self.database = DataBaseInterface()
        self.webAPI   = BlockChairInterface()

        # intialize number of transactions per address
        self.init_last_numTrans()
        # update database 1x through
        addresses = self.database.get_all_addresses()
        for addr in addresses:
            self.update_database(addr)

        self.numAddr = len(addresses)
        print('Update complete')

    # get all addresses in the database and their number of transactions
    def init_last_numTrans(self):

        addresses = self.database.get_all_addresses()

        for addr in addresses:
            self.last_numTrans[addr] = self.webAPI.get_num_transactions(addr)
            self.last_diff[addr] = self.last_numTrans[addr] 

    # determine which addresses need to be updated
    # run until one needs to be updated since daemon
    def need_update(self):
        address_update = []
        go = True
        print('Pinging for updates...')
        while go:
            time.sleep(self.sleepTime)
            addresses = self.database.get_all_addresses()
            for address in addresses:
            #for address in self.last_numTrans:

                # if new address, need to update it and table
                if address not in self.last_numTrans:
                    go = False 
                    address_update.append(address)
                    self.last_numTrans[address] = self.webAPI.get_num_transactions(address)
                    self.last_diff[address] = self.last_numTrans[address] 
                    continue
    
                # see if there has been more transactions 
                # if so return since we need to update said address
                num_trans = self.webAPI.get_num_transactions(address)
                if self.last_numTrans[address] < num_trans:
                    self.last_diff = num_trans - self.last_numTrans[address]
                    self.last_numTrans[address] = num_trans
                    go = False
                    address_update.append(address)

        print('New transaction! Update...')
                    
        return address_update
    
    # for an address update the database 
    def update_database(self, address):
        # get data for address from webAPI
        if address in self.last_diff:
            num_update = self.last_diff[address]
            data_dict, data_address = self.webAPI.get_data_address(address,
                                                    num_trans=num_update)
        else:
            data_dict, data_address = self.webAPI.get_data_address(address)
            num_update = len(data_dict['transactions'])


        # update Balance and Transaction Databases
        if num_update == 0:
            return 

        datetime = data_dict['transactions'][0]['time']
        self.database.add_balance_wrapper(address, data_dict['balance'], 
                                        data_dict['balance_usd'], datetime)


        # update the tranaction data base with the last num_update entries
        self.database.add_n_transactions(address, data_dict, num_update)



def main():

    updater = DataBaseUpdater(5) 

    # run this like a Daemon where basically we're always looking to update
    # the database by seeing if any new info came in
    while True:
        addresses = updater.need_update()
    
        for addr in addresses:
            updater.update_database(addr)
        print('Update complete')


if __name__ == "__main__":
    main()

