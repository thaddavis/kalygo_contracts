from pyteal import *
from contracts.escrow.constants import *


@Subroutine(TealType.uint64)
def guard_creator_close_out():
    return Seq(
        And(
            App.globalGet(GLOBAL_CREATOR) == Txn.sender(),
            Txn.application_args[0] == CLOSE_OUT,
        )
    )
