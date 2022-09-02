from API_KEY import API_KEY 
import requests
from decimal import Decimal
import json
import pprint
import pickle

# API URL
url = 'https://api.etherscan.io/api'

def get_event_log_for_dec_liq(start_block, offset = '10'):
    uniswap_v3_usdc_eth_pool = '0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8' # Uniswap V3 USDC-ETH Pool
    topic0 = '0x70935338e69775456a85ddef226c395fb668b63fa0115f5f20610b388e6ca9c0' # Collect back after burn > decrease liquidity 
    r = requests.get(url,params={
        'module': 'logs', 
        'action': 'getlogs', 
        'address': uniswap_v3_usdc_eth_pool,
        'topic0': topic0,
        'topic0_1_opr': 'and',
        'topic1': '0x000000000000000000000000c36442b4a4522e871399cd717abdd847ab11fe88', # example
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
destakers = []
with open('destakers.pickle', 'wb') as f:
    pickle.dump(destakers, f)

while int(start_block) < 15413286:
    print('start_block: ', start_block, 'iteration: ', i)
    data = get_event_log_for_dec_liq(
    offset='10000', 
    start_block=start_block)
    start_block = str(int(data[-1]['blockNumber'],16))
    i += 1

    with open(file='destakers.pickle', mode='rb') as f:
        destakers = pickle.load(f)
    destakers.extend(data)
    with open('destakers.pickle', 'wb') as f:
        pickle.dump(destakers, f)

print('Done')

