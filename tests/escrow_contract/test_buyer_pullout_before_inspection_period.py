import pytest
from modules.utils.deploy_new import deploy_new
from scripts.escrow.delete_contract import main as delete_contract
from algosdk import account
from algosdk.future import transaction
import config.config_escrow as config
from helpers.utils import (
    format_application_info_global_state,
    get_private_key_from_mnemonic,
)
from modules.AlgodClient import Algod
from modules.utils.get_txn_params import get_txn_params
from helpers.time import get_current_timestamp, get_future_timestamp_in_secs

buyer_private_key = get_private_key_from_mnemonic(config.account_b_mnemonic)


@pytest.fixture(scope="module")
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
        int(get_future_timestamp_in_secs(60)),  # Inspection Period End Date
        int(get_future_timestamp_in_secs(240)),  # Closing Date
        int(get_future_timestamp_in_secs(360)),  # Free Funds Date
        True,  # True, -> ENABLE_TIME_CHECKS
    )
    yield deployed_contract["app_id"]
    print()
    print("tear down in fixture", deployed_contract["app_id"])
    delete_contract(
        deployed_contract["app_id"],
        config.account_a_mnemonic,
    )


def test_buyer_pullout(escrow_contract):
    app_id = escrow_contract
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

    print("testing buyer pullout...")
    params = get_txn_params(Algod.getClient())
    sender = account.address_from_private_key(buyer_private_key)
    app_args = ["buyer_set_pullout"]
    unsigned_txn = transaction.ApplicationNoOpTxn(sender, params, app_id, app_args)
    signed_txn = unsigned_txn.sign(buyer_private_key)
    tx_id = Algod.getClient().send_transactions([signed_txn])

    # wait for confirmation
    print("wait for confirmation...")
    confirmed_txn = transaction.wait_for_confirmation(Algod.getClient(), tx_id, 4)
    print("BUYER SUCCESSFULLY PULLED OUT")
    print("Result confirmed in round: {}".format(confirmed_txn["confirmed-round"]))

    app_info = Algod.getClient().application_info(app_id)
    app_info_formatted = format_application_info_global_state(
        app_info["params"]["global-state"]
    )
    print()
    print(
        '"global_buyer_pullout_flag"',
        app_info_formatted["global_buyer_pullout_flag"],
    )
    assert app_info_formatted["global_buyer_pullout_flag"] == 1


def teardown_module(module):
    """teardown any state that was previously setup with a setup_module method."""
