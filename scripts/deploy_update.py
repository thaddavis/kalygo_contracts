from algosdk import account
from algosdk.future import transaction
from contracts.escrow.contract import approval, clear
from pyteal import compileTeal, Mode
from helpers.utils import (
    compile_program,
    wait_for_confirmation,
    get_private_key_from_mnemonic,
)
import config.config_escrow as config
from modules.AlgodClient import Algod


def main():
    creator_private_key = get_private_key_from_mnemonic(config.account_a_mnemonic)

    approval_program_ast = approval()
    approval_program_teal = compileTeal(
        approval_program_ast, mode=Mode.Application, version=6
    )

    with open("./build/approval.teal", "w") as h:
        h.write(approval_program_teal)

    approval_program_compiled = compile_program(
        Algod.getClient(), approval_program_teal
    )

    clear_state_program_ast = clear()
    clear_state_program_teal = compileTeal(
        clear_state_program_ast, mode=Mode.Application, version=6
    )

    with open("./build/clear.teal", "w") as h:
        h.write(clear_state_program_teal)

    clear_state_program_compiled = compile_program(
        Algod.getClient(), clear_state_program_teal
    )

    app_args = []

    sender = account.address_from_private_key(creator_private_key)

    params = Algod.getClient().suggested_params()
    params.flat_fee = True
    params.fee = 1000

    txn = transaction.ApplicationUpdateTxn(
        sender,
        params,
        config.app_id,
        approval_program_compiled,
        clear_state_program_compiled,
        app_args,
        foreign_apps=[],
        # foreign_assets=[config.stablecoin_ASA],
    )
    print("Updating...")

    # sign transaction
    signed_txn = txn.sign(creator_private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    Algod.getClient().send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(Algod.getClient(), tx_id)

    # display results
    transaction_response = Algod.getClient().pending_transaction_info(tx_id)

    print(transaction_response)
