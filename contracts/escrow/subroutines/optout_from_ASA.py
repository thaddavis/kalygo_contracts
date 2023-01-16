from pyteal import *
from contracts.escrow.constants import GLOBAL_ASA_ID


@Subroutine(TealType.none)
def optout_from_ASA():
    return Seq(
        [
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields(
                {
                    TxnField.type_enum: TxnType.AssetTransfer,
                    TxnField.xfer_asset: App.globalGet(GLOBAL_ASA_ID),  # stablecoin ASA
                    TxnField.asset_close_to: Global.current_application_address(),
                    TxnField.sender: Global.current_application_address(),
                    TxnField.asset_receiver: Global.current_application_address(),
                    TxnField.fee: Int(0),
                }
            ),
            InnerTxnBuilder.Submit(),
            Approve(),
        ]
    )
