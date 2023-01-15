from pyteal import *
from contracts.escrow.constants import *


@Subroutine(TealType.uint64)
def guard_buyer_withdraw_balance():
    return Seq(
        And(
            # TODO will need to add time related checks
            Global.group_size() == Int(1),
            App.globalGet(GLOBAL_BUYER) == Txn.sender(),
            Txn.application_args[0] == WITHDRAW_BALANCE,
        )
    )
