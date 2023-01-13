from pyteal import *
from contracts.escrow.constants import *


@Subroutine(TealType.none)
def send_ASA_to_buyer():
    return Seq(Approve())
