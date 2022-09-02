from API_KEY import API_KEY 
import requests
from decimal import Decimal
import json
import pprint
import pickle

# API URL
url = 'https://api.etherscan.io/api'

def get_erc721_token_transfers(contract_address, page='1', offset='10', start_block='12369738'):
    r = requests.get(url,params={
        'module': 'account', 
        'action': 'tokennfttx', 
        'contractaddress': contract_address,
        'sort': 'asc',
        'page': page,
        'offset': offset,
        'startblock': start_block,
        'endblock': 'latest',
        'apikey': API_KEY}) 

    res = r.json()
    return res['result']

uniswap_v3_positions_nft_contract_address = '0xc36442b4a4522e871399cd717abdd847ab11fe88' # created at block 12369739

start_block = '12369738'
i = 1
uniswap_positions = []
with open('data/uniswap_positions.pickle', 'wb') as f:
    pickle.dump(uniswap_positions, f)

while int(start_block) < 15413286:
    print('start_block: ', start_block, 'iteration: ', i)
    data = get_erc721_token_transfers(uniswap_v3_positions_nft_contract_address, 
    offset='10000', 
    start_block=start_block)

    with open(file='data/uniswap_positions.pickle', mode='rb') as f:
        uniswap_positions = pickle.load(f)
    uniswap_positions.extend(data)
    with open('data/uniswap_positions.pickle', 'wb') as f:
        pickle.dump(uniswap_positions, f)

    start_block = data[-1]['blockNumber']
    i += 1


print('Done')

