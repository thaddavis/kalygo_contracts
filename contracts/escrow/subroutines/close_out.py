from pyteal import *

@Subroutine(TealType.none)
def close_out():
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
                    TxnField.fee: Int(0),
                    TxnField.close_remainder_to: Txn.sender(),
                }
            ),
            InnerTxnBuilder.Submit(),
            Approve(),
        ]
    )
