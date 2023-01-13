from pyteal import *


@Subroutine(TealType.none)
def optin_to_ASA():
    return Seq(
        [
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields(
                {
                    TxnField.type_enum: TxnType.AssetTransfer,
                    TxnField.xfer_asset: Btoi(
                        Gtxn[1].application_args[1]
                    ),  # Stablecoin ASA
                    TxnField.asset_amount: Int(0),
                    TxnField.sender: Global.current_application_address(),
                    TxnField.asset_receiver: Global.current_application_address(),
                    TxnField.fee: Int(0),
                }
            ),
            InnerTxnBuilder.Submit(),
            Approve(),
        ]
    )
