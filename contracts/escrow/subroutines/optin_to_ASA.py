from pyteal import *

from contracts.escrow.constants import GLOBAL_ASA_ID


@Subroutine(TealType.none)
def optin_to_ASA():
    return Seq(
        [
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields(
                {
                    TxnField.type_enum: TxnType.AssetTransfer,
                    TxnField.xfer_asset: App.globalGet(GLOBAL_ASA_ID),
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
