from pyteal import *
from contracts.escrow.constants import *

# TODO
@Subroutine(TealType.uint64)
def guard_send_ASA_to_buyer():
    return Seq(Approve())
