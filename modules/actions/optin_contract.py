from multiprocessing.dummy import Array
from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction


def optin_contract(
    algod_client: AlgodClient,
    params,
    sender: str,
    sender_private_key: str,
    receiver: str,
    app_id: int,
    ASA_id: int,
):
    print(
        "Opting-in Contract to ASA...",
        "ASA id:",
        ASA_id,
        "app_id",
        app_id,
        "sender",
        sender,
        "receiver",
        receiver,
    )

    app_args = ["optin_contract"]
    unsigned_txn_B = transaction.ApplicationNoOpTxn(
        sender, params, app_id, app_args, foreign_assets=[ASA_id]
    )

    signed_txn_B = unsigned_txn_B.sign(sender_private_key)

    signed_group = [signed_txn_B]

    tx_id = algod_client.send_transactions(signed_group)

    # wait for confirmation
    try:
        print("wait for confirmation...")
        confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 4)
        print("Successfully Opted-in Contract to ASA")
    except Exception as err:
        print("ERROR", err)
