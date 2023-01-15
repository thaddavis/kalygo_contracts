from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction


def transfer_ASA_to_contract(
    algod_client: AlgodClient,
    params,
    sender: str,
    sender_private_key: str,
    app_address: str,
    ASA_id: int,
    ASA_amount: int,
):
    print(
        "Transferring ASA from sender to contract",
        "ASA_id",
        ASA_id,
        "sender",
        sender,
        "app_address",
        app_address,
    )

    asset_info = algod_client.asset_info(ASA_id)
    print("")
    print("sender_address", sender)
    print("receiver_address (contract)", app_address)
    print("ASA creator", asset_info["params"]["creator"])
    print("")

    unsigned_txn_A = transaction.AssetTransferTxn(
        sender,  # sender (str): address of the sender
        params,  # sp (SuggestedParams): suggested params from algod
        app_address,  # receiver (str): address of the receiver
        ASA_amount,  # amt (int): amount of asset base units to send
        ASA_id,  # index (int): index of the asset
    )

    print("signing AssetTransferTxn")
    signed_txn_A = unsigned_txn_A.sign(sender_private_key)
    # submit transaction
    print("sending txn")
    tx_id = algod_client.send_transactions([signed_txn_A])
    # wait for confirmation
    print("wait for confirmation...")
    transaction.wait_for_confirmation(algod_client, tx_id, 4)
    print("Asset amount transferred successfully")
