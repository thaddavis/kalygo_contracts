import json
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk import constants
import config.config_escrow as config
from helpers.utils import get_private_key_from_mnemonic
from modules.AlgodClient import Algod

account_private_key = get_private_key_from_mnemonic(config.account_c_mnemonic)


def main():
    sender = config.account_c_address
    params = Algod.getClient().suggested_params()
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE

    unsigned_txn = transaction.AssetConfigTxn(
        sender=sender,
        sp=params,
        total=1000000,
        default_frozen=False,
        unit_name="USDCa",
        asset_name="USDCa",
        manager=sender,
        reserve=sender,
        freeze=sender,
        clawback=sender,
        url="https://www.circle.com",
        decimals=2,
    )

    print("signing txn")
    signed_txn = unsigned_txn.sign(account_private_key)

    # submit transaction
    print("sending txn")
    tx_id = Algod.getClient().send_transactions([signed_txn])

    # wait for confirmation
    try:
        print("wait for confirmation...")
        confirmed_txn = transaction.wait_for_confirmation(Algod.getClient(), tx_id, 4)

        # print("Transaction information: {}".format(
        #     json.dumps(confirmed_txn, indent=4)))

        print("Created ASA index:", confirmed_txn["asset-index"])
    except Exception as err:
        print(err)
