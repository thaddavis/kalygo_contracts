from pyteal import *
from contracts.escrow.guards import (
    guard_creator_withdraw_balance,
    guard_buyer_withdraw_balance,
    guard_seller_set_arbitration,
    guard_seller_withdraw_balance,
    guard_optin_to_ASA,
    guard_optout_from_ASA,
    guard_buyer_withdraw_ASA,
    guard_seller_withdraw_ASA,
    guard_buyer_set_pullout,
    guard_buyer_set_arbitration,
)
from contracts.escrow.program import event
from contracts.escrow.constants import *
from .initialization.initialize_contract import initialize_contract

from .subroutines import (
    withdraw_balance,
    withdraw_ASA,
    optin_to_ASA,
    optout_from_ASA,
    buyer_set_pullout,
    buyer_set_arbitration,
    seller_set_arbitration,
)


def approval():
    return event(
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
                [guard_creator_withdraw_balance(), withdraw_balance()],
                [guard_buyer_withdraw_balance(), withdraw_balance()],
                [guard_seller_withdraw_balance(), withdraw_balance()],
                [guard_seller_set_arbitration(), seller_set_arbitration()],
                [guard_optout_from_ASA(), optout_from_ASA()],
                [guard_buyer_withdraw_ASA(), withdraw_ASA()],
                [guard_buyer_set_pullout(), buyer_set_pullout()],
                [guard_buyer_set_arbitration(), buyer_set_arbitration()],
                [guard_optin_to_ASA(), optin_to_ASA()],
                # [guard_buyer_withdraw_ASA(), withdraw_ASA()],
                # [guard_seller_withdraw_ASA(), withdraw_ASA()],
                # [guard_seller_accept_pull_out(), seller_accept_pull_out()],
                # [guard_buyer_set_arbitration(), buyer_raise_arbitration()],
                # [guard_seller_raise_arbitration(), seller_raise_arbitration()],
            ),
            Reject(),
        ),
    )


def clear():
    return Approve()
