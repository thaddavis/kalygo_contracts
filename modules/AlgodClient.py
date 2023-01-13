from algosdk.v2client import algod
import config.config_escrow as config


class Algod:
    # Declare the static variables
    client = None  # static variable

    # def __init__(self):

    @staticmethod
    def getClient():
        if Algod.client:
            return Algod.client
        else:
            headers = {
                "X-API-Key": config.algod_token,
            }
            Algod.client = algod.AlgodClient(
                config.algod_token, config.algod_url, headers
            )
            return Algod.client
