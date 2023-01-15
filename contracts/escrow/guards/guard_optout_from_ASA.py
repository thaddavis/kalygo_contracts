from pyteal import *
from contracts.escrow.constants import *


@Subroutine(TealType.uint64)
def guard_optout_from_ASA():
    return Seq(
        And(
            Global.group_size() == Int(1),
            Txn.application_args[0] == OPTOUT_CONTRACT,
        )
    )
