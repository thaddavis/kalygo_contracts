import pytest
from scripts.deploy.escrow.deploy_new import main as deploy
from algosdk.v2client import algod
from algosdk import account, constants, logic
from algosdk.future import transaction
import config.config_escrow as config
from helpers.utils import (
    format_application_info_global_state,
    get_private_key_from_mnemonic,
    wait_for_confirmation,
)

from modules.AlgodClient import Algod

deployer_private_key = get_private_key_from_mnemonic(config.account_a_mnemonic)


def test_initial_state(escrow_contract):
    app_id = escrow_contract
    print("*** app_id ***", app_id)
    app_info = Algod.getClient().application_info(app_id)
    # print("app_info", app_info)
    app_info_formatted = format_application_info_global_state(
        app_info["params"]["global-state"]
    )
    print("app_info_formatted", app_info_formatted)
    assert app_info_formatted["global_escrow_payment_1"] == 1000000
    assert app_info_formatted["global_escrow_payment_2"] == 2000000
    assert app_info_formatted["global_escrow_total"] == 3000000

    app_address = logic.get_application_address(config.app_id)
    res = Algod.getClient().account_info(app_address)
    assert res["amount"] == 0
