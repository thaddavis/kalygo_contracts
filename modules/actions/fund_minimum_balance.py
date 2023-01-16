from multiprocessing.dummy import Array
from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction


def fund_minimum_balance(
    algod_client: AlgodClient,
    params,
    sender: str,
    sender_private_key: str,
    receiver: str,
    amount: int,  # need to send 100,000 mAlgos for each ASA the contract opts into
):
    print(
        "Fund Minimum Balance...",
        "sender",
        sender,
        "receiver",
        receiver,
    )
    note = "for optin to stablecoin ASA".encode()
    unsigned_txn_A = transaction.PaymentTxn(
        sender, params, receiver, amount, None, note
    )

    signed_txn_A = unsigned_txn_A.sign(sender_private_key)

    signed_group = [signed_txn_A]

    tx_id = algod_client.send_transactions(signed_group)

    # wait for confirmation
    try:
        print("wait for confirmation...")
        confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 4)
        print("Successfully Funded Minimum Contract Balance")
    except Exception as err:
        print("ERROR", err)
