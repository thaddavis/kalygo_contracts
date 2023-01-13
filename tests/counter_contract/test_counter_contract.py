import pytest
from scripts.deploy.counter.deploy_new import main as deploy
from algosdk.v2client import algod
from algosdk import account
from algosdk.future import transaction
import config.config_counter as config
from helpers.utils import (
    format_application_info_global_state,
    get_private_key_from_mnemonic,
    wait_for_confirmation,
)
import json

algod_client = algod.AlgodClient(config.algod_token, config.algod_url)


@pytest.fixture(scope="class")
def counter_contract():
    print("deploy counter_contract")
    app_id = deploy()
    yield app_id


deployer_private_key = get_private_key_from_mnemonic(config.account_a_mnemonic)


class Test_Counter_Contract:
    def test_initial_state(self, counter_contract):
        app_id = counter_contract
        print("*** app_id ***", app_id)
        app_info = algod_client.application_info(app_id)
        app_info_formatted = format_application_info_global_state(
            app_info["params"]["global-state"]
        )
        print("app_info_formatted", app_info_formatted)
        assert app_info_formatted["counter"] == 0

    def test_call_increment(self, counter_contract):
        app_id = counter_contract

        print("*** app_id ***", app_id)

        sender = account.address_from_private_key(deployer_private_key)
        print("sender", sender)
        app_args = ["inc"]
        params = algod_client.suggested_params()
        params.flat_fee = True
        params.fee = 1000
        # # step 2 - create unsigned transaction
        txn = transaction.ApplicationNoOpTxn(sender, params, app_id, app_args)
        signed_txn = txn.sign(deployer_private_key)
        tx_id = signed_txn.transaction.get_txid()
        # step 3 - send the transaction
        algod_client.send_transactions([signed_txn])
        tx_info = wait_for_confirmation(algod_client, tx_id)
        print("Transaction information: {}".format(json.dumps(tx_info, indent=4)))

        app_info = algod_client.application_info(app_id)
        app_info_formatted = format_application_info_global_state(
            app_info["params"]["global-state"]
        )
        print("app_info_formatted", app_info_formatted)
        assert app_info_formatted["counter"] == 1
