import time
import config.config_escrow as config
from modules.AlgodClient import Algod
from modules.IndexerClient import Indexer
from algosdk.future import transaction
from modules.helpers.print_account_ASA_holdings import print_account_ASA_holdings
from modules.helpers.utils import get_private_key_from_mnemonic
from modules.helpers.get_txn_params import get_txn_params

# import json


def main():
    # REVOKE ASSET
    # The clawback address `sender` revokes asset units from `revocation_target` and places them with `receiver`

    params = get_txn_params(Algod.getClient())
    sender = "24EAOWVXMSZ7LAXDYLHPIQ7PXDIO4OMPSJTZXP47YAJ4MTQASCJXPCQ2DI"  # use the `print_ASA_info.py` script to find the clawback address for the asset
    receiver = "LRRN5NIUW5FM6CGWXBK4LP37TJL232HV5KQ4C45WK373MKVUEYS5EHQN5Y"
    revocation_target = "MTCUJRCVBADQ2W4HDJBKZOMEP4XBAM7WFDWNC7IYZ3HOG4XUIZWYVAUI6U"

    sender_private_key = get_private_key_from_mnemonic(
        "oak diagram room element planet output satoshi scrap appear brass core crunch charge drink husband festival fan toy ancient surprise cart cave inquiry absent fee"
    )

    print("PRE-revoke holdings for revocation_target")
    print_account_ASA_holdings(
        Algod.getClient(), Indexer.getClient(), config.stablecoin_ASA, revocation_target
    )

    # Must be signed by the account that is the Asset's clawback address
    txn = transaction.AssetTransferTxn(
        sender=sender,
        sp=params,
        receiver=receiver,
        amt=199995,
        index=config.stablecoin_ASA,
        revocation_target=revocation_target,
    )
    stxn = txn.sign(sender_private_key)

    try:
        txid = Algod.getClient().send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = transaction.wait_for_confirmation(Algod.getClient(), txid, 4)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn["confirmed-round"]))
    except Exception as err:
        print(err)

    print("")
    print("waiting to allow indexer to update new balance amount...")
    time.sleep(3)
    print("")
    print(
        "POST-revoke holdings for revocation_target"
    )  # The balance of revocation target should be reduced by `amount``
    print_account_ASA_holdings(
        Algod.getClient(), Indexer.getClient(), config.stablecoin_ASA, revocation_target
    )
