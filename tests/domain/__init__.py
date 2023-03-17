# import dependencies
import pickle
from web3 import Web3, HTTPProvider
import datetime
import requests
from web3.middleware import geth_poa_middleware


start = datetime.datetime(year=2023, month=3, day=8, hour=5, minute=33, second=0)
end = datetime.datetime(year=2023, month=3, day=8, hour=5, minute=34, second=0)

uri = 'https://api.polygonscan.com/' + 'api?module=block&action=getblocknobytime&timestamp={timestamp}&closest=before&apikey=' + 'XTMZ21TVBX93CTGUZMJV6YCFYUMITQWX1Y'
new = '''https://api.polygonscan.com/api?module=account&action=tokentx&contractaddress={address}&startblock={start}&endblock={end}&apikey=XTMZ21TVBX93CTGUZMJV6YCFYUMITQWX1Y'''

r_start = requests.get(uri.format(timestamp=int(start.timestamp()))).json()['result']
r_end = requests.get(uri.format(timestamp=int(end.timestamp()))).json()['result']
start_block = int(r_start)
end_block = int(r_end)

# instantiate a web3 remote provider
provider = HTTPProvider('https://rpc.ankr.com/polygon')
w3 = Web3(provider)

# filter through blocks and look for transactions involving this address
blockchain_address = "0xAE81FAc689A1b4b1e06e7ef4a2ab4CD8aC0A087D"

# create an empty dictionary we will add transaction data to
tx_dictionary = {}

w3.middleware_onion.inject(
    geth_poa_middleware,
    layer=0
)


def getTransactions(start, end, address):
    for x in range(start, end):
        response = requests.get(new.format(address=address, start=start, end=end))
        print(response.json())



getTransactions(start_block, end_block, blockchain_address)
