from algosdk.v2client import algod
from algosdk import account
from algosdk.future import transaction
from algosdk.encoding import decode_address
from pyteal import compileTeal, Mode
from modules.helpers.time import get_current_timestamp, get_future_timestamp_in_secs
from modules.helpers.utils import (
    compile_program,
    wait_for_confirmation,
    read_created_app_state,
    get_private_key_from_mnemonic,
)

import config.config_escrow as config
from contracts.escrow.contract import approval, clear
from modules.AlgodClient import Algod

local_ints = 0
local_bytes = 0
global_ints = 9
global_bytes = 3


def main(
    deployer_address: str = config.account_a_address,
    deployer_mnemonic: str = config.account_a_mnemonic,
    buyer_address: str = config.account_b_address,
    seller_address: str = config.account_c_address,
    escrow_payment_1: int = config.escrow_payment_1,
    escrow_payment_2: int = config.escrow_payment_2,
    total_price: int = config.total_price,
    inspection_start: int = int(get_current_timestamp()),
    inspection_end: int = int(get_future_timestamp_in_secs(60)),
    closing_date=int(get_future_timestamp_in_secs(240)),
    free_funds_date=int(get_future_timestamp_in_secs(360)),
    enable_time_checks=True,
    foreign_apps=[],
    foreign_assets=[],
):
    deployer_private_key = get_private_key_from_mnemonic(deployer_mnemonic)

    # declare application state storage (immutable)
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)

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

    app_args = [
        decode_address(buyer_address),  # 0 buyer
        decode_address(seller_address),  # 1 seller
        escrow_payment_1,  # 2 1st_escrow_payment
        escrow_payment_2,  # 3 2nd_escrow_payment
        total_price,  # 4 total escrow
        inspection_start,  # 5 GLOBAL_INSPECTION_START_DATE, Btoi(Txn.application_args[5]) # uint64
        inspection_end,  # 6 GLOBAL_INSPECTION_END_DATE, Btoi(Txn.application_args[6]) # uint64
        closing_date,  # 7 GLOBAL_CLOSING_DATE, Btoi(Txn.application_args[7]) # uint64
        free_funds_date,  # 8 GLOBAL_FREE_FUNDS_DATE, Btoi(Txn.application_args[8]) # uint64,
        enable_time_checks,  # 9 GLOBAL_TIME_CHECK_ENABLED
    ]

    on_complete = transaction.OnComplete.NoOpOC.real
    params = Algod.getClient().suggested_params()
    params.flat_fee = True
    params.fee = 1000

    txn = transaction.ApplicationCreateTxn(
        deployer_address,
        params,
        on_complete,
        approval_program_compiled,
        clear_state_program_compiled,
        global_schema,
        local_schema,
        app_args,
        foreign_apps=[],
        # foreign_assets=[config.stablecoin_ASA],
        foreign_assets=foreign_assets,
    )
    print("sending ApplicationCreateTxn...")
    # sign transaction
    signed_txn = txn.sign(deployer_private_key)
    tx_id = signed_txn.transaction.get_txid()
    # send transaction
    Algod.getClient().send_transactions([signed_txn])
    # await confirmation
    wait_for_confirmation(Algod.getClient(), tx_id)
    # display results
    transaction_response = Algod.getClient().pending_transaction_info(tx_id)
    # print("transaction_response", transaction_response)
    app_id = transaction_response["application-index"]
    confirmed_round = transaction_response["confirmed-round"]
    print("Created new app-id:", app_id)
    # created_app_state = read_created_app_state(
    #     Algod.getClient(), deployer_address, app_id
    # )
    # print("Global state: {}".format(json.dumps(created_app_state, indent=4)))
    return {
        "app_id": app_id,
        "confirmed_round": confirmed_round,
        "inspection_start": inspection_start,
        "inspection_end": inspection_end,
    }
