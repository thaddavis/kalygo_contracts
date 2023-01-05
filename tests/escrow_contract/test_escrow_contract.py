import pytest
from scripts.deploy.escrow.deploy_new import main as deploy
from algosdk.v2client import algod
from algosdk import account, constants, logic
from algosdk.future import transaction
from helpers.time import get_current_timestamp, get_future_timestamp_in_secs
import config.config_escrow_localhost as config
from helpers.utils import (
    format_application_info_global_state,
    get_private_key_from_mnemonic,
    wait_for_confirmation,
)
import json

algod_client = algod.AlgodClient(config.algod_token, config.algod_url)


@pytest.fixture(scope="class")
def escrow_contract():
    print("deploy escrow_contract")

    app_id = deploy(
        config.account_a_address,
        config.account_a_mnemonic,
        config.account_b_address,
        config.account_c_address,
        config.escrow_payment_1,
        config.escrow_payment_2,
        config.total_price,
        int(get_current_timestamp()),
        int(get_future_timestamp_in_secs(60)),
        int(get_future_timestamp_in_secs(240)),
        int(get_future_timestamp_in_secs(360)),
    )
    yield app_id


deployer_private_key = get_private_key_from_mnemonic(config.account_a_mnemonic)


class Test_Escrow_Contract:
    def test_initial_state(self, escrow_contract):
        app_id = escrow_contract
        print("*** app_id ***", app_id)
        app_info = algod_client.application_info(app_id)
        # print("app_info", app_info)
        app_info_formatted = format_application_info_global_state(
            app_info["params"]["global-state"]
        )
        print("app_info_formatted", app_info_formatted)
        assert app_info_formatted["global_escrow_payment_1"] == 1000000
        assert app_info_formatted["global_escrow_payment_2"] == 2000000
        assert app_info_formatted["global_escrow_total"] == 3000000

        app_address = logic.get_application_address(config.app_id)
        res = algod_client.account_info(app_address)
        assert res["amount"] == 0

    # def test_call_increment(self, counter_contract):
    #     app_id = counter_contract

    #     print("*** app_id ***", app_id)

    #     sender = account.address_from_private_key(deployer_private_key)
    #     print("sender", sender)
    #     app_args = ["inc"]
    #     params = algod_client.suggested_params()
    #     params.flat_fee = True
    #     params.fee = 1000
    #     # # step 2 - create unsigned transaction
    #     txn = transaction.ApplicationNoOpTxn(sender, params, app_id, app_args)
    #     signed_txn = txn.sign(deployer_private_key)
    #     tx_id = signed_txn.transaction.get_txid()
    #     # step 3 - send the transaction
    #     algod_client.send_transactions([signed_txn])
    #     tx_info = wait_for_confirmation(algod_client, tx_id)
    #     print("Transaction information: {}".format(json.dumps(tx_info, indent=4)))

    #     app_info = algod_client.application_info(app_id)
    #     app_info_formatted = format_application_info_global_state(
    #         app_info["params"]["global-state"]
    #     )
    #     print("app_info_formatted", app_info_formatted)
    #     assert app_info_formatted["counter"] == 1
