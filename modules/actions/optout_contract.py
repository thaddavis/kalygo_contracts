from algosdk import logic
from algosdk.future import transaction
from algosdk.v2client.algod import AlgodClient


def optout_contract(
    algod_client: AlgodClient,
    params,
    sender: str,
    sender_private_key: str,
    app_id: int,
    ASA_id: int,
):
    print("Opting-out Contract from ASA")
    app_address = logic.get_application_address(app_id)
    print("app_id", app_id, "app_address", app_address)

    app_args = ["optout_contract"]
    unsigned_txn = transaction.ApplicationNoOpTxn(
        sender, params, app_id, app_args, foreign_assets=[ASA_id]
    )

    signed_txn = unsigned_txn.sign(sender_private_key)
    tx_id = algod_client.send_transactions([signed_txn])

    # wait for confirmation
    print("wait for confirmation...")
    transaction.wait_for_confirmation(algod_client, tx_id, 4)
    print("Successfully Opted-out Contract from ASA")
