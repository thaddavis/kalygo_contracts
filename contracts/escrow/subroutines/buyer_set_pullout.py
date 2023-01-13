from pyteal import *
from contracts.escrow.constants import *


@Subroutine(TealType.none)
def buyer_set_pullout():
    return Seq(
        If(
            And(
                Txn.sender() == App.globalGet(GLOBAL_BUYER),
                And(
                    App.globalGet(GLOBAL_ENABLE_TIME_CHECKS) == Int(1),
                    Global.latest_timestamp() < App.globalGet(GLOBAL_INSPECTION_END),
                ),
            )
        )
        .Then(
            Seq(
                App.globalPut(
                    GLOBAL_BUYER_PULLOUT_FLAG,
                    App.globalGet(GLOBAL_BUYER_PULLOUT_FLAG) + Int(1),
                )
            )
        )
        .Else(Reject()),
        Approve(),
    )
