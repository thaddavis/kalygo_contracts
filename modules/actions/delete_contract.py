from algosdk import account
from algosdk.future import transaction
from modules.helpers.utils import (
    wait_for_confirmation,
    get_private_key_from_mnemonic,
)
import config.config_escrow as config
from modules.AlgodClient import Algod
from modules.helpers.get_txn_params import get_txn_params


def delete_contract(
    app_id: int,
    creator_mnemonic: str = config.account_a_mnemonic,
):
    creator_private_key = get_private_key_from_mnemonic(creator_mnemonic)
    sender = account.address_from_private_key(creator_private_key)
    params = get_txn_params(Algod.getClient())
    txn = transaction.ApplicationDeleteTxn(sender, params, app_id)
    print("Deleting application...")

    # sign transaction
    signed_txn = txn.sign(creator_private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    Algod.getClient().send_transactions([signed_txn])
    # await confirmation
    wait_for_confirmation(Algod.getClient(), tx_id)
    # display results
    # transaction_response = Algod.getClient().pending_transaction_info(tx_id)
    # print(transaction_response)
    print("Successfully deleted contract")
