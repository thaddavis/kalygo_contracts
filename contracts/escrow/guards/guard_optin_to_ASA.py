from pyteal import *
from contracts.escrow.constants import *


@Subroutine(TealType.uint64)
def guard_optin_to_ASA():
    return Seq(
        And(
            Global.group_size() == Int(1),
            Txn.sender() == App.globalGet(GLOBAL_BUYER),
            Txn.type_enum() == TxnType.ApplicationCall,
            Txn.application_args[0] == OPTIN_CONTRACT,
        )
    )
