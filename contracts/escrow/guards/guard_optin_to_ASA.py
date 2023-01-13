from pyteal import *
from contracts.escrow.constants import *


@Subroutine(TealType.uint64)
def guard_optin_to_ASA():
    return Seq(
        And(
            Global.group_size() == Int(2),
            Gtxn[0].type_enum() == TxnType.Payment,
            Gtxn[1].type_enum() == TxnType.ApplicationCall,
            Gtxn[1].application_args[0] == OPTIN_CONTRACT,
        )
    )
