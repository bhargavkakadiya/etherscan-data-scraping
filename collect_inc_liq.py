from API_KEY import API_KEY 
import requests
from decimal import Decimal
import json
import pprint
import pickle

# API URL
url = 'https://api.etherscan.io/api'

def get_event_log_for_inc_liq(start_block, offset = '10'):
    uniswap_v3_usdc_eth_pool = '0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8' # Uniswap V3 USDC-ETH Pool
    topic0 = '0x7a53080ba414158be7ec69b987b5fb7d07dee101fe85488f0853ae16239d0bde' # increase liquidity at Uniswap V3    
    r = requests.get(url,params={
        'module': 'logs', 
        'action': 'getlogs', 
        'address': uniswap_v3_usdc_eth_pool,
        'topic0': topic0,
        'fromBlock': start_block,
        'toBlock': 'latest',
        'page': '1',
        'offset': offset,
        'apikey': API_KEY}) 

    res = r.json()

    return res['result']

start_block = '12369738'
i = 1
stakers = []
with open('stakers.pickle', 'wb') as f:
    pickle.dump(stakers, f)

while int(start_block) < 15413286:
    print('start_block: ', start_block, 'iteration: ', i)
    data = get_event_log_for_inc_liq(
    offset='10000', 
    start_block=start_block)
    start_block = str(int(data[-1]['blockNumber'],16))
    i += 1

    with open(file='stakers.pickle', mode='rb') as f:
        stakers = pickle.load(f)
    stakers.extend(data)
    with open('stakers.pickle', 'wb') as f:
        pickle.dump(stakers, f)

print('Done')

