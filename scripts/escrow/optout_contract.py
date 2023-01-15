from helpers.utils import get_private_key_from_mnemonic
import config.config_escrow as config
from algosdk import account, constants, logic
from algosdk.future import transaction
from algosdk.error import AlgodHTTPError
from modules.AlgodClient import Algod
from modules.utils.get_txn_params import get_txn_params

sender_private_key = get_private_key_from_mnemonic(config.account_a_mnemonic)
stablecoin_ASA: int = config.stablecoin_ASA


def main():
    print("stablecoin_ASA", stablecoin_ASA)

    app_address = logic.get_application_address(config.app_id)

    print("app_id", config.app_id)
    print("app_address", app_address)

    sender = account.address_from_private_key(sender_private_key)

    params = get_txn_params(Algod.getClient(), constants.MIN_TXN_FEE, 2)

    app_args = ["optout_contract", stablecoin_ASA]
    unsigned_txn = transaction.ApplicationNoOpTxn(
        sender, params, config.app_id, app_args, foreign_assets=[stablecoin_ASA]
    )

    signed_txn = unsigned_txn.sign(sender_private_key)

    tx_id = Algod.getClient().send_transactions([signed_txn])

    # wait for confirmation
    try:
        print("wait for confirmation...")
        confirmed_txn = transaction.wait_for_confirmation(Algod.getClient(), tx_id, 4)

        # print("Transaction information: {}".format(
        #     json.dumps(confirmed_txn, indent=4)))

        print("Successfully Opted-out Contract to ASA's")
        print("Result confirmed in round: {}".format(confirmed_txn["confirmed-round"]))
    except Exception as err:
        print("ERROR", err)
