from pyteal import *
from contracts.escrow.constants import *

# TODO
@Subroutine(TealType.uint64)
def guard_seller_withdraw_ASA():
    return Seq(
        And(
            # TODO will need to add time related checks
            Global.group_size() == Int(1),
            App.globalGet(GLOBAL_SELLER) == Txn.sender(),
            Txn.application_args[0] == WITHDRAW_ASA,
        )
    )
