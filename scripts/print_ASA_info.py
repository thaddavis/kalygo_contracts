from algosdk.v2client import indexer
import config.config_escrow as config
from modules.AlgodClient import Algod
from modules.IndexerClient import Indexer
import json


def main():
    stablecoin_ASA: int = config.stablecoin_ASA
    response = Indexer.getClient().search_assets(asset_id=stablecoin_ASA)
    print("asset info: {}".format(json.dumps(response, indent=4)))
