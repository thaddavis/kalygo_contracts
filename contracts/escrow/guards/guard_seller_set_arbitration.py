from pyteal import *
from contracts.escrow.constants import *


@Subroutine(TealType.uint64)
def guard_seller_set_arbitration():
    return Seq(
        Or(
            And(
                Global.group_size() == Int(1),
                App.globalGet(GLOBAL_SELLER) == Txn.sender(),
                Txn.application_args[0] == SELLER_SET_ARBITRATION,
                App.globalGet(GLOBAL_ENABLE_TIME_CHECKS) == Int(1),
                Global.latest_timestamp() < App.globalGet(GLOBAL_CLOSING_DATE),
            ),
            And(
                Int(0)
            ),  # CHECK IF OTHER PARTY HAS RAISED ARBITRATION IN WHICH CASE ALLOW EXTENSION TO RAISE ARB FLAG
        )
    )
