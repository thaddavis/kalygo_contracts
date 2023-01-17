from pyteal import *
from contracts.escrow.constants import *


def seller_set_arbitration():
    return Seq(
        App.globalPut(
            GLOBAL_SELLER_ARBITRATION_FLAG,
            Int(1),
        ),
        Approve(),
    )
