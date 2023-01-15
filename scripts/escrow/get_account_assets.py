import json
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk import constants
import config.config_escrow as config
from helpers.utils import get_private_key_from_mnemonic

from modules.AlgodClient import Algod


def main():
    account = config.account_b_address
    # account = "W5SNJIZZXSLML7G4MAYPTORTI54LOCHIBTA2IV7NSHJ3MP2JVUJNWQAWXI"
    params = Algod.getClient().suggested_params()
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE

    account_info = Algod.getClient().account_info(account)

    print("Account Information: {}".format(json.dumps(account_info, indent=4)))
