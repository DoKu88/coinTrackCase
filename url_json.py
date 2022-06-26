# import urllib library
from urllib.request import urlopen
import json
# store the URL in url as
# parameter for urlopen
#url = "https://api.blockchair.com/stats"
url_base = 'https://api.blockchair.com/bitcoin/dashboards/address/'
address = '3E8ociqZa9mZUSwGdSmAEMAoAxBK3FNDcd'

url = url_base + address

# store the response of URL
response = urlopen(url)

# storing the JSON response
# from url in data
data_json = json.loads(response.read())

# print the json response
print(data_json)

import pdb; pdb.set_trace()

print('ahoy')

def get_url_data(url1):
    # store the response of URL
    response = urlopen(url1)
    # storing the JSON response
    # from url in data
    data_json = json.loads(response.read())

    return data_json

def get_data_address(address):
    url_access = url_base + address
    data_json = get_url_data(url_access)
    data_address, data_context = data_json['data'][address], data_json['context']

    balance, balance_usd = get_balance(data_address)
    transactions = get_transactions(data_address)

    data_dict = dict()
    data_dict['balance'] = balance
    data_dict['balance_usd'] = balance_usd
    data_dict['transactions'] = transactions

    return data_dict

# per address get the balance
def get_balance(data_address):
    balance = data_address['address']['balance']
    balance_usd = url_data['address']['balance_usd']

    return balance, balance_usd

# per address get all transactions
def get_transactions(data_address):
    transactions = data_address['transactions']

    return transactions

# from the address book return all addresses
def get_addresses():
    pass

# from the address book, get the next address
def get_next_address(iterator1):
    pass
