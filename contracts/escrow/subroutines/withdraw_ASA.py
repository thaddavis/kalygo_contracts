from pyteal import *
from contracts.escrow.constants import GLOBAL_ASA_ID


@Subroutine(TealType.none)
def withdraw_ASA():
    contract_ASA_balance = AssetHolding.balance(
        Global.current_application_address(), App.globalGet(GLOBAL_ASA_ID)
    )
    return Seq(
        [
            contract_ASA_balance,
            # ASA back to sender
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields(
                {
                    TxnField.type_enum: TxnType.AssetTransfer,
                    TxnField.xfer_asset: App.globalGet(GLOBAL_ASA_ID),
                    # vvv simulate amount of ASA to return to sender vvv
                    # TxnField.asset_amount: Btoi(Txn.application_args[2]),
                    TxnField.asset_amount: contract_ASA_balance.value(),
                    TxnField.sender: Global.current_application_address(),
                    TxnField.asset_receiver: Txn.sender(),
                    TxnField.fee: Int(0),
                }
            ),
            InnerTxnBuilder.Submit(),
            Approve(),
        ]
    )
