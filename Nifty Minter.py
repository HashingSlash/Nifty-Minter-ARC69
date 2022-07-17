import json
import base64
import csv
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk.future import transaction

def nifty_loop_mint(private_key, my_address, loop_name, loop_ticker, quantity, loop_address, metadata):
    
    ###     Build txn
    params = algod_client.suggested_params()
    unsigned_txn = transaction.AssetConfigTxn(
    sender=my_address,
    sp=params,
    index=None,
    total=quantity,
    default_frozen=False,
    manager=my_address,
    reserve=my_address,
    freeze='',
    clawback='',
    unit_name=loop_ticker,
    asset_name=loop_name,
    url=loop_address,
    strict_empty_address_check=False, 
    decimals=0,
    note=metadata)

    ###     Sign
    signed_txn = unsigned_txn.sign(private_key)
    ###     Submit
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))
    ###     Confirm
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)  
    except Exception as err:
        print(err)
        return   
    print('Minted : ' + str(confirmed_txn['asset-index']))
    print('Block : ' + str(confirmed_txn['confirmed-round']))

testnet=True

if testnet==True:
        algod_address = 'https://node.testnet.algoexplorerapi.io'
elif testnet==False:
    algod_address = 'https://node.algoexplorerapi.io'
algod_token = ''
algod_client = algod.AlgodClient(algod_token, algod_address)

with open('nftinfo.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    row_number = 0
    for row in csv_reader:
        row_number += 1
        if row_number == 2:
            my_address = row[0]
            private_key = row[1]
            print('Loaded wallet : ' + my_address)
            #print("My passphrase : {}".format(mnemonic.from_private_key(private_key)))
            account_info = algod_client.account_info(my_address)
            print("Account balance: {} microAlgos".format(account_info.get('amount')))
        if row_number >= 5:
            nifty_loop_mint(private_key, my_address, row[0], row[1], row[2], row[3], row[4])
    account_info = algod_client.account_info(my_address)
    print("Final Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

