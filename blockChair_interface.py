from urllib.request import urlopen
import json
from datetime import datetime
import sys

# =============================================================================
# API URL INTERACTIONS
# =============================================================================

class BlockChairInterface:
    def __init__(self):
        self.url_base = 'https://api.blockchair.com/bitcoin/dashboards/address/'

    # gets JSON data from webpage
    def get_url_data(self, url1):
        # store the response of URL
        response = urlopen(url1)
        # storing the JSON response
        # from url in data
        data_json = json.loads(response.read())

        return data_json

    # processes data for given BitCoin Address from blockchair API
    def get_data_address(self, address, url_base=None, num_trans=10000):
        if url_base is None:
            url_base = self.url_base

        # get the number of transactions we want
        trans_deets = '?transaction_details=true'
        num_trans = '&limit=' + str(num_trans)

        # build url to extract data from
        url_access = url_base + address + trans_deets + num_trans
        data_json = self.get_url_data(url_access)
        data_address, data_context = data_json['data'][address], data_json['context']

        # process data and get balances and transactions out
        balance, balance_usd = self.get_balance(data_address)
        transactions = self.get_transactions(data_address)

        # format data nicely into dictionary
        data_dict = dict()
        data_dict['balance'] = balance
        data_dict['balance_usd'] = balance_usd
        data_dict['transactions'],  data_dict['num_transactions'] = transactions

        return data_dict, data_address

    # per address get the balance
    def get_balance(self, data_address):
        balance = data_address['address']['balance']
        balance_usd = data_address['address']['balance_usd']

        return balance, balance_usd

    # returns the complete n latest transactions
    # already pre-specified
    def get_transactions(self, data_address):
        # NOTE: Each transaction is a dictionary with detailed information
        # about each transaction
        transactions = data_address['transactions']
        num_transactions = data_address['address']['transaction_count']

        return transactions, num_transactions
