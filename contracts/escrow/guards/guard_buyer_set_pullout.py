from pyteal import *
from contracts.escrow.constants import *


@Subroutine(TealType.uint64)
def guard_buyer_set_pullout():
    return Seq(
        And(
            Global.group_size() == Int(1),
            App.globalGet(GLOBAL_BUYER) == Txn.sender(),
            Txn.application_args[0] == BUYER_SET_PULLOUT,
            App.globalGet(GLOBAL_ENABLE_TIME_CHECKS) == Int(1),
            Global.latest_timestamp() < App.globalGet(GLOBAL_INSPECTION_END_DATE),
        )
    )
