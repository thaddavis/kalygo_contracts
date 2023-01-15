from pyteal import *


@Subroutine(TealType.none)
def withdraw_balance():
    return Seq(
        [
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields(
                {
                    TxnField.type_enum: TxnType.Payment,
                    TxnField.amount: Balance(Global.current_application_address())
                    - Global.min_txn_fee(),
                    TxnField.sender: Global.current_application_address(),
                    TxnField.receiver: Txn.sender(),
                    TxnField.fee: Global.min_txn_fee(),
                    TxnField.close_remainder_to: Txn.sender(),
                }
            ),
            InnerTxnBuilder.Submit(),
            Approve(),
        ]
    )
