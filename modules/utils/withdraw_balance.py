from helpers.utils import get_private_key_from_mnemonic
import config.config_escrow as config
from algosdk import account, constants, logic
from algosdk.future import transaction
from algosdk.error import AlgodHTTPError
from algosdk.v2client.algod import AlgodClient


def withdraw_balance(
    algod_client: AlgodClient, params, sender: str, sender_private_key: str, app_id: int
):
    print("Withdrawing balance from contract")
    app_address = logic.get_application_address(app_id)
    print("app_id", app_id, "app_address", app_address)

    app_args = ["withdraw_balance"]
    unsigned_txn = transaction.ApplicationNoOpTxn(sender, params, app_id, app_args)

    signed_txn = unsigned_txn.sign(sender_private_key)
    tx_id = algod_client.send_transactions([signed_txn])

    # wait for confirmation
    print("wait for confirmation...")
    confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 4)
    # print("Transaction information: {}".format(
    #     json.dumps(confirmed_txn, indent=4)))
    print("Successfully withdrew balance from contract")
    # print("Result confirmed in round: {}".format(confirmed_txn["confirmed-round"]))
