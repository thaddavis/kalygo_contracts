from helpers.utils import get_private_key_from_mnemonic
import config.config_escrow as config
from algosdk import account, constants, logic
from algosdk.future import transaction
from modules.AlgodClient import Algod

account_private_key = get_private_key_from_mnemonic(config.account_a_mnemonic)
stablecoin_ASA: int = config.stablecoin_ASA


def main():
    print("stablecoin_ASA", stablecoin_ASA)
    app_info = Algod.getClient().application_info(config.app_id)

    creator_address = app_info["params"]["creator"]
    account_address = account.address_from_private_key(account_private_key)

    assert creator_address == account_address

    app_address = logic.get_application_address(config.app_id)
    print("app_address", app_address)

    params = Algod.getClient().suggested_params()
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE

    sender = account_address

    unsigned_txn_A = transaction.AssetTransferTxn(
        sender,  # sender (str): address of the sender
        params,  # sp (SuggestedParams): suggested params from algod
        sender,  # receiver (str): address of the receiver
        0,  # amt (int): amount of asset base units to send
        stablecoin_ASA,  # index (int): index of the asset
    )

    print("signing opt-in txn")
    signed_txn_A = unsigned_txn_A.sign(account_private_key)

    # submit transaction
    print("sending txn")
    tx_id = Algod.getClient().send_transactions([signed_txn_A])

    # wait for confirmation
    try:
        print("wait for confirmation...")
        confirmed_txn = transaction.wait_for_confirmation(Algod.getClient(), tx_id, 4)

        # print("Transaction information: {}".format(
        #     json.dumps(confirmed_txn, indent=4)))

        print("Opted-in successfully")
        print("Result confirmed in round: {}".format(confirmed_txn["confirmed-round"]))
    except Exception as err:
        print("ERROR", err)
