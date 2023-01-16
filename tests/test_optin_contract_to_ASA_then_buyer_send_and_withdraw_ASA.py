import pytest
from algosdk import constants, logic
import config.config_escrow as config
from modules.helpers.utils import (
    get_private_key_from_mnemonic,
)
from modules.actions.deploy_new import deploy_new
from modules.actions.fund_minimum_balance import fund_minimum_balance
from modules.actions.optin_contract import optin_contract
from modules.actions.optout_contract import optout_contract
from modules.actions.delete_contract import delete_contract
import pytest
from modules.helpers.time import get_current_timestamp, get_future_timestamp_in_secs
from modules.AlgodClient import Algod
from modules.helpers.get_txn_params import get_txn_params
from modules.actions.withdraw_balance import withdraw_balance
from modules.actions.transfer_ASA_to_contract import transfer_ASA_to_contract
from modules.actions.withdraw_ASA import withdraw_ASA


@pytest.fixture(scope="module")
def escrow_contract():
    print()
    print()
    print("deploying escrow contract...")

    deployed_contract = deploy_new(
        config.account_a_address,  # deployer/creator of contract ie: likely will be buyer
        config.account_a_mnemonic,  # deployer/creator of contract mnemonic ie: likely will be buyer
        config.account_b_address,
        config.account_c_address,
        config.escrow_payment_1,
        config.escrow_payment_2,
        config.total_price,
        config.stablecoin_ASA,
        int(get_current_timestamp()),  # Inspection Period Start Date
        int(get_future_timestamp_in_secs(60)),  # Inspection Period End Date
        int(get_future_timestamp_in_secs(120)),  # Moving Date
        int(get_future_timestamp_in_secs(240)),  # Closing Date
        int(get_future_timestamp_in_secs(360)),  # Free Funds Date
        True,  # True, -> ENABLE_TIME_CHECKS
        foreign_apps=[],
        foreign_assets=[config.stablecoin_ASA],
    )
    yield deployed_contract["app_id"]
    print()
    print("tear down in fixture", deployed_contract["app_id"])
    delete_contract(
        deployed_contract["app_id"],
        config.account_a_mnemonic,
    )


def test_optin_contract_to_ASA_then_buyer_send_and_withdraw_ASA(escrow_contract):
    app_id = escrow_contract

    txn_params = get_txn_params(Algod.getClient(), constants.MIN_TXN_FEE, 1)
    opt_txn_params = get_txn_params(Algod.getClient(), constants.MIN_TXN_FEE, 2)

    buyer = config.account_b_address
    buyer_private_key = get_private_key_from_mnemonic(config.account_b_mnemonic)
    contract_address = logic.get_application_address(app_id)
    stablecoin_ASA = config.stablecoin_ASA

    res = Algod.getClient().account_info(contract_address)
    assert res["amount"] == 0

    fund_minimum_balance(
        Algod.getClient(),
        txn_params,
        buyer,
        buyer_private_key,
        contract_address,
        200000,  # 100,000 mAlgos min_balance for optin to ASA + 100,000 mAlgos for contract to be able to call other contracts
    )

    optin_contract(
        Algod.getClient(),
        opt_txn_params,
        buyer,
        buyer_private_key,
        contract_address,
        app_id,
        stablecoin_ASA,
    )

    res = Algod.getClient().account_info(contract_address)
    assert res["amount"] == 200000

    account_info = Algod.getClient().account_info(contract_address)
    # print("account_info", account_info)

    for asset in account_info["assets"]:
        if asset["asset-id"] == stablecoin_ASA:
            print("contract ASA holdings before transfer:", asset["amount"])
            assert asset["amount"] == 0

    # Transfer ASA to contract
    transfer_ASA_to_contract(
        Algod.getClient(),
        txn_params,
        buyer,
        buyer_private_key,
        contract_address,
        stablecoin_ASA,
        20,
    )

    account_info = Algod.getClient().account_info(contract_address)
    for asset in account_info["assets"]:
        if asset["asset-id"] == stablecoin_ASA:
            print("contract ASA holdings after transfer:", asset["amount"])
            assert asset["amount"] == 20

    """"
    Withdraw ASA from contract
    """
    withdraw_ASA(
        Algod.getClient(),
        opt_txn_params,
        buyer,
        buyer_private_key,
        app_id,
        stablecoin_ASA,
    )

    account_info = Algod.getClient().account_info(contract_address)
    for asset in account_info["assets"]:
        if asset["asset-id"] == stablecoin_ASA:
            print("contract ASA holdings after transfer:", asset["amount"])
            assert asset["amount"] == 0

    optout_contract(
        Algod.getClient(),
        opt_txn_params,
        buyer,
        buyer_private_key,
        app_id,
        stablecoin_ASA,
    )

    withdraw_balance(
        Algod.getClient(),
        txn_params,
        buyer,
        buyer_private_key,
        app_id,
    )

    res = Algod.getClient().account_info(contract_address)
    assert res["amount"] == 0
