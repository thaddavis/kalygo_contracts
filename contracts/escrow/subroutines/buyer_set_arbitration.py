from pyteal import *
from contracts.escrow.constants import *


def buyer_set_arbitration():
    return Seq(
        App.globalPut(
            GLOBAL_BUYER_ARBITRATION_FLAG,
            Int(1),
        ),
        Approve(),
    )
