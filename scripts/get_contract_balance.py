from algosdk import logic
import config.config_escrow as config
import json
from modules.AlgodClient import Algod


def main():
    print("app_id:", config.app_id)
    application_address = logic.get_application_address(config.app_id)
    print("application address for app_id", application_address)
    print("")

    account_info = Algod.getClient().account_info(application_address)
    print("Account Info: {}".format(json.dumps(account_info, indent=4)))
