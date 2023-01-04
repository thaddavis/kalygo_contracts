from algosdk.v2client import algod
from algosdk import account
from algosdk.future import transaction
from contracts.escrow.contract import approval, clear
from pyteal import compileTeal, Mode
from helpers.utils import compile_program, wait_for_confirmation, get_private_key_from_mnemonic
import json

import config.config_localhost as config

headers = {
    "X-API-Key": config.algod_token,
}


def main():
    algod_client = algod.AlgodClient(
        config.algod_token, config.algod_url, headers)
    creator_private_key = get_private_key_from_mnemonic(
        config.account_a_mnemonic
    )

    # declare application state storage (immutable)
    local_ints = 0
    local_bytes = 0
    global_ints = 0
    global_bytes = 0
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)

    approval_program_ast = approval()
    approval_program_teal = compileTeal(
        approval_program_ast, mode=Mode.Application, version=6
    )

    with open('./build/approval.teal', "w") as h:
        h.write(approval_program_teal)

    approval_program_compiled = compile_program(
        algod_client, approval_program_teal)

    clear_state_program_ast = clear()
    clear_state_program_teal = compileTeal(
        clear_state_program_ast, mode=Mode.Application, version=6
    )

    with open('./build/clear.teal', "w") as h:
        h.write(clear_state_program_teal)

    clear_state_program_compiled = compile_program(
        algod_client, clear_state_program_teal
    )

    app_args = []

    sender = account.address_from_private_key(creator_private_key)

    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = 1000

    txn = transaction.ApplicationUpdateTxn(
        sender,
        params,
        config.app_id,
        approval_program_compiled,
        clear_state_program_compiled,
        app_args,
        foreign_apps=[config.ASA_1, config.ASA_2,
                      config.pool_1_app_id, config.pool_2_app_id]
    )
    print("Updating...")

    # sign transaction
    signed_txn = txn.sign(creator_private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    algod_client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(algod_client, tx_id)

    # display results
    transaction_response = algod_client.pending_transaction_info(tx_id)

    print(transaction_response)