from typing import TypeAlias
# Doc https://algorandfoundation.github.io/puya/index.html
# Doc https://algorandfoundation.github.io/algokit-utils-py/index.html
from algopy import (
    Account,
    ARC4Contract,
    BoxMap,
    Bytes,
    Asset,
    Global,
    Txn,
    itxn,
    UInt64,
    arc4,
    gtxn,
    op,
)


class Eval(ARC4Contract):
    def __init__(self) -> None:
        self.q1 = BoxMap(Account, arc4.Bool, key_prefix="q1")
        self.q2 = BoxMap(Account, arc4.Bool, key_prefix="q2")
        self.q3 = BoxMap(Account, arc4.Bool, key_prefix="q3")
        self.q4 = BoxMap(Account, arc4.Bool, key_prefix="q4")
        self.q4_string = BoxMap(Account, arc4.String, key_prefix="")

    @arc4.abimethod()
    def add_students(self, account: Account) -> None:
        assert Txn.sender == Global.creator_address
        self.q4_string[account] = arc4.String(" ")

    @arc4.abimethod
    def claim_algo(self) -> None:
        assert Txn.sender in self.q4_string
        assert Txn.sender not in self.q1
        self.q1[Txn.sender] = arc4.Bool(True)
        itxn.Payment(
            receiver=Txn.sender,
            amount=500_000,
            fee=2*op.Global.min_txn_fee
        ).submit()

    @arc4.abimethod
    def opt_in_to_asset(self, mbr_pay: gtxn.PaymentTransaction, asset: Asset) -> None:
        assert Txn.sender in self.q4_string
        assert Txn.sender not in self.q2
        self.q2[Txn.sender] = arc4.Bool(True)
        assert not Global.current_application_address.is_opted_in(asset)
        assert mbr_pay.receiver == Global.current_application_address
        assert mbr_pay.amount == Global.min_balance + Global.asset_opt_in_min_balance
        itxn.AssetTransfer(
            xfer_asset=asset.id,
            asset_receiver=Global.current_application_address,
            asset_amount=0,
        ).submit()

    @arc4.abimethod
    def sum(self, array: Bytes) -> UInt64:
        assert Txn.sender in self.q4_string
        assert Txn.sender not in self.q3
        self.q3[Txn.sender] = arc4.Bool(True)
        assert array.length == 2

        total = UInt64(0)
        for n in array:
            total += op.btoi(n)
        return total

    @arc4.abimethod()
    def update_box(self, value: arc4.String) -> arc4.String:
        assert Txn.sender in self.q4_string
        assert Txn.sender not in self.q4
        self.q4[Txn.sender] = arc4.Bool(True)
        self.q4_string[Txn.sender] = value
        return self.q4_string[Txn.sender]
