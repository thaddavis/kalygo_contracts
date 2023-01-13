from pyteal import *
from contracts.escrow.guards import (
    guard_creator_close_out,
    guard_buyer_close_out,
    guard_seller_close_out,
    guard_optin_to_ASA,
    guard_optout_from_ASA,
    guard_send_ASA_to_buyer,
    guard_send_ASA_to_seller,
    guard_buyer_set_pullout,
)
from helpers import program
from contracts.escrow.constants import *
from .initialization.initialize_contract import initialize_contract

from .subroutines import (
    close_out,
    optin_to_ASA,
    optout_from_ASA,
    send_ASA_to_buyer,
    send_ASA_to_seller,
    buyer_set_pullout,
)


def approval():
    return program.event(
        init=Seq(initialize_contract(), Approve()),
        close_out=Seq(Approve()),
        update=Cond(
            [App.globalGet(GLOBAL_CREATOR) == Txn.sender(), Approve()]
        ),  # update=Reject(), # for production tho : )
        delete=Seq(
            If(Balance(Global.current_application_address()) == Int(0))
            .Then(Approve())
            .Else(Reject())
        ),
        no_op=Seq(
            Cond(
                [guard_creator_close_out(), close_out()],
                [guard_buyer_close_out(), close_out()],
                [guard_seller_close_out(), close_out()],
                [guard_optout_from_ASA(), optout_from_ASA()],
                [guard_buyer_set_pullout(), buyer_set_pullout()],
                # Gtxn's come after solo Txn's
                [guard_optin_to_ASA(), optin_to_ASA()],
                [guard_send_ASA_to_buyer(), send_ASA_to_buyer()],
                [guard_send_ASA_to_seller(), send_ASA_to_seller()],
                # [guard_seller_accept_pull_out(), seller_accept_pull_out()],
                # [guard_buyer_raise_arbitration(), buyer_raise_arbitration()],
                # [guard_seller_raise_arbitration(), seller_raise_arbitration()],
            ),
            Reject(),
        ),
    )


def clear():
    return Approve()
