from textwrap import indent
import time
from datetime import datetime
import pytest
from modules.utils.deploy_new import deploy_new
from scripts.escrow.delete_contract import main as delete_contract
from algosdk import account, error
from algosdk.future import transaction
import config.config_escrow as config
from helpers.utils import (
    format_application_info_global_state,
    get_private_key_from_mnemonic,
)
from modules.AlgodClient import Algod
from modules.utils.get_txn_params import get_txn_params
from helpers.time import get_current_timestamp, get_future_timestamp_in_secs
from modules.AlgodClient import Algod

buyer_private_key = get_private_key_from_mnemonic(config.account_b_mnemonic)


@pytest.fixture(scope="function")
def escrow_contract():
    print()
    print()
    print("deploying escrow contract...")

    deployed_contract = deploy_new(
        config.account_a_address,
        config.account_a_mnemonic,
        config.account_b_address,
        config.account_c_address,
        config.escrow_payment_1,
        config.escrow_payment_2,
        config.total_price,
        int(get_current_timestamp()),  # Inspection Period Start Date
        int(get_future_timestamp_in_secs(8)),  # Inspection Period End Date
        int(get_future_timestamp_in_secs(60)),  # Closing Date
        int(get_future_timestamp_in_secs(120)),  # Free Funds Date
        True,  # True, -> ENABLE_TIME_CHECKS
    )
    yield deployed_contract["app_id"], deployed_contract[
        "confirmed_round"
    ], deployed_contract["inspection_start"], deployed_contract["inspection_end"]
    print()
    print("teardown phase of fixture", "deleting app_id:", deployed_contract["app_id"])
    delete_contract(
        deployed_contract["app_id"],
        config.account_a_mnemonic,
    )


def test_buyer_pullout(escrow_contract):
    app_id, confirmed_round, inspection_start, inspection_end = escrow_contract

    app_info = Algod.getClient().application_info(app_id)
    # print("app_info", app_info)
    app_info_formatted = format_application_info_global_state(
        app_info["params"]["global-state"]
    )
    print()
    print(
        '"global_buyer_pullout_flag"',
        app_info_formatted["global_buyer_pullout_flag"],
    )
    assert app_info_formatted["global_buyer_pullout_flag"] == 0

    onchain_timestamp = Algod.getClient().block_info(confirmed_round)["block"]["ts"]
    last_round = confirmed_round
    while onchain_timestamp < inspection_end:
        status = Algod.getClient().status()
        print(
            "confirmed_round",
            confirmed_round,
            'status["last-round"]',
            status["last-round"],
        )
        if last_round != status["last-round"]:
            last_round = status["last-round"]
            onchain_timestamp = Algod.getClient().block_info(status["last-round"])[
                "block"
            ]["ts"]

        print(datetime.fromtimestamp(onchain_timestamp), ":On-chain time:")
        print(datetime.fromtimestamp(inspection_end), ":Inspection period end date:")

        time.sleep(2)

    print("inspection period has elapsed...")

    with pytest.raises(error.AlgodHTTPError):
        print("testing buyer pullout...")
        params = get_txn_params(Algod.getClient())
        sender = account.address_from_private_key(buyer_private_key)
        app_args = ["buyer_set_pullout"]
        unsigned_txn = transaction.ApplicationNoOpTxn(sender, params, app_id, app_args)
        signed_txn = unsigned_txn.sign(buyer_private_key)

        tx_id = Algod.getClient().send_transactions([signed_txn])

        print("tx_id", tx_id)
        # wait for confirmation
        print("wait for confirmation . > . > . >")

        # confirmed_txn = transaction.wait_for_confirmation(Algod.getClient(), tx_id, 4)

        transaction.wait_for_confirmation(Algod.getClient(), tx_id, 4)

    app_info = Algod.getClient().application_info(app_id)
    app_info_formatted = format_application_info_global_state(
        app_info["params"]["global-state"]
    )
    print()
    print(
        '"global_buyer_pullout_flag"',
        app_info_formatted["global_buyer_pullout_flag"],
    )
    assert app_info_formatted["global_buyer_pullout_flag"] == 0
    print("`buyer_set_pullout` failed as expected")


# def teardown_module(module):
#     """teardown any state that was previously setup with a setup_module method."""
