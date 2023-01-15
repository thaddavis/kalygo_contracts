from algosdk import logic
from algosdk.future import transaction
from algosdk.v2client.algod import AlgodClient


def withdraw_ASA(
    algod_client: AlgodClient,
    params,
    sender: str,
    sender_private_key: str,
    app_id: int,
    ASA_id: int,
    ASA_amount: int,
    foreign_assets: list[int],
):
    print("Withdraw ASA from contract")
    app_address = logic.get_application_address(app_id)
    print("app_id", app_id, "app_address", app_address)

    app_args = ["withdraw_ASA", ASA_id, ASA_amount]
    unsigned_txn = transaction.ApplicationNoOpTxn(
        sender, params, app_id, app_args, foreign_assets=foreign_assets
    )

    signed_txn = unsigned_txn.sign(sender_private_key)
    tx_id = algod_client.send_transactions([signed_txn])

    # wait for confirmation
    print("wait for confirmation...")
    transaction.wait_for_confirmation(algod_client, tx_id, 4)
    print("Successfully withdrew ASA from contract")
