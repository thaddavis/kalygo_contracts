from pyteal import *
from contracts.escrow.constants import *


@Subroutine(TealType.none)
def buyer_set_pullout():
    return Seq(
        App.globalPut(
            GLOBAL_BUYER_PULLOUT_FLAG,
            Int(1),
        ),
        Approve(),
    )
