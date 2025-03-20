import re
from typing import List
import algosdk as sdk
from algokit_utils import AlgorandClient, AlgoAmount, ABIType
from hashlib import sha256


def account_creation(algorand: AlgorandClient, name: str, funds=AlgoAmount(algo=0)):
    account = algorand.account.from_environment(name, fund_with=funds)
    info = algorand.client.algod.account_info(account.address)
    print(
        f"Name\t\t: %s \n"
        f"Address\t\t: %s\n"
        f"Created Asset\t: %s\n"
        f"Assets\t\t: %s\n"
        f"Algo\t\t: %.6f"
        % (
            name,
            account.address,
            info["created-assets"],
            info["assets"],
            info["amount"] / 1_000_000,
        )
    )
    if len(info["created-apps"]) > 0:
        print(f"Created-Apps\t: %s \n" % info["created-apps"][0]["id"])
    print("")
    return account


def get_asa_id(ptx):
    if (
        isinstance(ptx, dict)
        and "asset-index" in ptx
        and isinstance(ptx["asset-index"], int)
    ):
        return ptx["asset-index"]
    else:
        raise ValueError("Unexpected response from pending_transaction_info")


def display_info(algorand: AlgorandClient, names: List[str]):
    for name in names:
        account_creation(algorand, name)


def box_abi(cl, struct_name: str) -> ABIType:
    """Generate an ABIType from a struct name in cl.APP_SPEC.structs."""
    struct_fields = cl.APP_SPEC.structs[struct_name]  # Retrieve struct fields
    abi_type_string = f"({','.join(field.type for field in struct_fields)})"
    return ABIType.from_string(abi_type_string)


def sha256_encode(value):
    return sha256(sdk.abi.StringType().encode(value)).digest()


def sha256_digest(value):
    return sha256(value).digest()


def get_min_balance_required(ac, method) -> int | None:
    """
    Simulates a transaction and extracts the minimum balance required if the transaction fails due to insufficient funds.

    :param ac: The application client instance.
    :param method: The method for the application call.
    :return: The minimum balance required if an insufficient balance error occurs, otherwise None.
    """
    try:
        ac.algorand.new_group().add_app_call_method_call(
            method
        ).simulate()
        return 0  # If no error occurs, return None (no min balance issue)

    except Exception as e:
        error_message = str(e)
        # Extract the current balance and required minimum balance
        match = re.search(r"balance (\d+) below min (\d+)", error_message)
        if match:
            balance = int(match.group(1))
            min_balance_required = int(match.group(2))
            return min_balance_required - balance  # Return the extracted min balance required

        return None
