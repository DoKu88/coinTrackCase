from db_interface import DataBaseInterface 
from blockChair_interface import BlockChairInterface


def main():
    # make objects so that we can interact with the web API and 
    # our database
    database = DataBaseInterface()
    webAPI   = BlockChairInterface()
    
    database.show_table("AddressBook")

    address = '3E8ociqZa9mZUSwGdSmAEMAoAxBK3FNDcd'
    address1 = 'bc1q0sg9rdst255gtldsmcf8rk0764avqy2h2ksqs5'
    user1 = "Bobert"
    database.add_address_wrapper(address, user1)
    database.add_address_wrapper(address1, user1)
    print("Address book contents:")
    database.show_table("AddressBook")

    data_dict, data_address = webAPI.get_data_address(address)

    datetime = data_dict['transactions'][0]['time']
    database.add_balance_wrapper(address, data_dict['balance'], data_dict['balance_usd'], datetime)
    database.add_n_transactions(address, data_dict, 10)
    #add_transaction(address, data_dict['transactions'][-1])

    addresses = database.get_addresses(user1)
    print("Bobert's Addresses: ", addresses)

    database.del_user(user1)
    addresses = database.get_addresses(user1)
    print("Bobert's Addresses: After del", addresses)

    print("Balances table")
    database.show_table("Balances")



if __name__ == "__main__":
    main()

