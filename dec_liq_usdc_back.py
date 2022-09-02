from API_KEY import API_KEY 
import requests
from decimal import Decimal
import json
import pprint
import pickle

# API URL
url = 'https://api.etherscan.io/api'

def get_event_log_for_dec_liq(start_block, offset = '10'):
    uniswap_v3_usdc_eth_pool = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48' # USDC
    topic0 = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef' # Transfer from to value
    r = requests.get(url,params={
        'module': 'logs', 
        'action': 'getlogs', 
        'address': uniswap_v3_usdc_eth_pool,
        'topic0': topic0,
        'topic0_1_opr': 'and',
        'topic1': '0x000000000000000000000000c36442b4a4522e871399cd717abdd847ab11fe88', # from address
        # https://etherscan.io/tx/0x2472e0ee92fd200cbcfc95d5eccab085a10c1c13c31ed8764fcaade221715cad#eventlog
        'fromBlock': start_block,
        'toBlock': 'latest',
        'page': '1',
        'offset': offset,
        'apikey': API_KEY}) 

    res = r.json()

    return res['result']

start_block = '12369738'
i = 1
destakers_usdc = []
with open('data/destakers_usdc.pickle', 'wb') as f:
    pickle.dump(destakers_usdc, f)

while int(start_block) < 15413286:
    print('start_block: ', start_block, 'iteration: ', i)
    data = get_event_log_for_dec_liq(
    offset='10000', 
    start_block=start_block)
    start_block = str(int(data[-1]['blockNumber'],16))
    i += 1

    with open(file='data/destakers_usdc.pickle', mode='rb') as f:
        destakers_usdc = pickle.load(f)
    destakers_usdc.extend(data)
    with open('data/destakers_usdc.pickle', 'wb') as f:
        pickle.dump(destakers_usdc, f)

print('Done')

