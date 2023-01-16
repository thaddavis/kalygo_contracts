from pyteal import *
from contracts.escrow.constants import *


@Subroutine(TealType.none)
def initialize_contract():
    return Seq(
        App.globalPut(
            GLOBAL_ENABLE_TIME_CHECKS, Btoi(Txn.application_args[10])
        ),  # uint64
        App.globalPut(GLOBAL_ASA_ID, Btoi(Txn.application_args[11])),  # uint64
        App.globalPut(GLOBAL_BUYER_PULLOUT_FLAG, Int(0)),  # uint64
        App.globalPut(GLOBAL_CREATOR, Txn.sender()),  # byteslice
        App.globalPut(GLOBAL_BUYER, Txn.application_args[0]),  # byteslice
        App.globalPut(GLOBAL_SELLER, Txn.application_args[1]),  # byteslice
        If(
            And(
                Btoi(Txn.application_args[2]) >= Int(100000),  # escrow 1 uint64
                Btoi(Txn.application_args[3]) >= Int(100000),  # escrow 2 uint64
                (Btoi(Txn.application_args[2]) + Btoi(Txn.application_args[3]))
                == Btoi(Txn.application_args[4]),  # make sure escrow 1 & 2 == total
            )
        )
        .Then(
            Seq(
                App.globalPut(
                    GLOBAL_ESCROW_PAYMENT_1, Btoi(Txn.application_args[2])
                ),  # uint64
                App.globalPut(
                    GLOBAL_ESCROW_PAYMENT_2, Btoi(Txn.application_args[3])
                ),  # uint64
                App.globalPut(
                    GLOBAL_ESCROW_TOTAL, Btoi(Txn.application_args[4])
                ),  # uint64
            )
        )
        .Else(Reject()),
        If(
            And(
                Btoi(Txn.application_args[5]) <= Btoi(Txn.application_args[6]),
                Btoi(Txn.application_args[6]) <= Btoi(Txn.application_args[7]),
                Btoi(Txn.application_args[7]) <= Btoi(Txn.application_args[8]),
            )
        )
        .Then(
            Seq(
                App.globalPut(
                    GLOBAL_INSPECTION_START_DATE, Btoi(Txn.application_args[5])
                ),  # uint64
                App.globalPut(
                    GLOBAL_INSPECTION_END_DATE, Btoi(Txn.application_args[6])
                ),  # uint64
                App.globalPut(
                    GLOBAL_MOVING_DATE, Btoi(Txn.application_args[7])
                ),  # uint64
                App.globalPut(
                    GLOBAL_CLOSING_DATE, Btoi(Txn.application_args[8])
                ),  # uint64
                App.globalPut(
                    GLOBAL_FREE_FUNDS_DATE, Btoi(Txn.application_args[9])
                ),  # uint64
            )
        )
        .Else(Reject()),
    )
