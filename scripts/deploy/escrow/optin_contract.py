from helpers.utils import get_private_key_from_mnemonic
import config.config_escrow as config
from algosdk import account, constants, logic
from algosdk.future import transaction
from algosdk.error import AlgodHTTPError
from modules.AlgodClient import Algod

sender_private_key = get_private_key_from_mnemonic(config.account_a_mnemonic)
stablecoin_ASA: int = config.stablecoin_ASA


def main():
    print("ASA_asset_id", stablecoin_ASA)

    app_address = logic.get_application_address(config.app_id)
    print("app_address", app_address)

    sender_address = account.address_from_private_key(sender_private_key)

    params = Algod.getClient().suggested_params()
    params.flat_fee = True
    # "* 2" is how to pool fees for optin inner group txn
    params.fee = constants.MIN_TXN_FEE * 2

    sender = sender_address
    receiver = app_address

    note = "Optin to ASAs".encode()
    amount = (
        100000 * 2
    )  # once for being able to issue transactions from contract and once for opting into stablecoin ASA

    unsigned_txn_A = transaction.PaymentTxn(
        sender, params, receiver, amount, None, note
    )

    app_args = ["optin_contract", stablecoin_ASA]
    unsigned_txn_B = transaction.ApplicationNoOpTxn(
        sender,
        params,
        config.app_id,
        app_args,
        foreign_assets=[stablecoin_ASA],
    )

    gid = transaction.calculate_group_id([unsigned_txn_A, unsigned_txn_B])
    unsigned_txn_A.group = gid  # type: ignore
    unsigned_txn_B.group = gid  # type: ignore

    signed_txn_A = unsigned_txn_A.sign(sender_private_key)
    signed_txn_B = unsigned_txn_B.sign(sender_private_key)

    signed_group = [signed_txn_A, signed_txn_B]

    tx_id = Algod.getClient().send_transactions(signed_group)

    # wait for confirmation
    try:
        print("wait for confirmation...")
        confirmed_txn = transaction.wait_for_confirmation(Algod.getClient(), tx_id, 4)

        # print("Transaction information: {}".format(
        #     json.dumps(confirmed_txn, indent=4)))

        print("Successfully Opted-in Contract to ASA's")
        print("Result confirmed in round: {}".format(confirmed_txn["confirmed-round"]))
    except Exception as err:
        print("ERROR", err)
