from pyteal import *


@Subroutine(TealType.none)
def withdraw_ASA():
    return Seq(
        [
            # ASA back to sender
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields(
                {
                    TxnField.type_enum: TxnType.AssetTransfer,
                    TxnField.xfer_asset: Btoi(Txn.application_args[1]),
                    # vvv simulate amount of ASA to return to sender vvv
                    TxnField.asset_amount: Btoi(Txn.application_args[2]),
                    TxnField.sender: Global.current_application_address(),
                    TxnField.asset_receiver: Txn.sender(),
                    TxnField.fee: Int(0),
                }
            ),
            InnerTxnBuilder.Submit(),
            Approve(),
        ]
    )
