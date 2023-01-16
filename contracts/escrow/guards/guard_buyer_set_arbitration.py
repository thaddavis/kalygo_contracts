from pyteal import *
from contracts.escrow.constants import *


@Subroutine(TealType.uint64)
def guard_buyer_set_arbitration():
    return Seq(
        Or(
            And(
                Global.group_size() == Int(1),
                App.globalGet(GLOBAL_BUYER) == Txn.sender(),
                Txn.application_args[0] == BUYER_SET_ARBITRATION,
                App.globalGet(GLOBAL_ENABLE_TIME_CHECKS) == Int(1),
                Global.latest_timestamp() < App.globalGet(GLOBAL_CLOSING_DATE),
            ),
            And(Int(0)),
        )
    )
