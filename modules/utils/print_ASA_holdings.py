def print_ASA_holdings(algod_client, indexer_client, ASA_id: int):
    # params = algod_client.suggested_params()
    # params.flat_fee = True
    # # "* 2" is how to pool fees for optin inner group txn
    # params.fee = fee * fee_multiple
    # return params

    print("")
    asset_info = algod_client.asset_info(ASA_id)
    results = indexer_client.accounts(asset_id=ASA_id)
    # print("assets account info: {}".format(
    #     json.dumps(results, indent=4)))
    print("asset name:", asset_info["params"]["name"])
    print("creator account:", asset_info["params"]["creator"])
    print("")
    print("HOLDERS")
    print("")

    for account in results["accounts"]:
        if "assets" in account:
            print("address:", account["address"])
            for asset in account["assets"]:
                if asset["asset-id"] == ASA_id:
                    print("holdings are: ", asset["amount"])
                    continue
            print("")

    print("")
