import os 
import algokit_utils as au
from algokit_utils.transactions import transaction_composer as att
from algosdk import account, mnemonic
from algosdk.v2client.algod import AlgodClient

from algokit_utils.models.account import SigningAccount
from algosdk.transaction import PaymentTxn
import client as cl
from utils import (
    account_creation,
    # display_info,
    box_abi,
    get_min_balance_required,

)

os.system("algokit compile py --out-dir ./app app.py")
os.system("algokit generate client app/Eval.arc32.json --output client.py")

algorand = au.AlgorandClient.testnet()
algod_client = algorand.client.algod
indexer_client = algorand.client.indexer

print(algod_client.block_info(0))
print(indexer_client.health())





Sarra = algorand.account.from_mnemonic(mnemonic="brain drive switch ritual example top race garage repair corn voice thank give grant coral village act zone ketchup congress police purpose viable abstract similar")

factory = algorand.client.get_typed_app_factory(
        cl.EvalFactory
    )



app_id = 736038676

ac = factory.get_app_client_by_id(app_id)
sp = algorand.get_suggested_params()
send_params=au.SendParams(populate_app_call_resources=True)


# ac.send.claim_algo(
#     params=au.CommonAppCallParams(
    
#     sender=Sarra.address,
#     signer=Sarra.signer
#          ),
#          send_params=send_params,
#      )



# result = algorand.send.asset_create(
#         au.AssetCreateParams(
#             sender=account.address,
#             signer=account.signer,
#             total=150,
#             decimals=10,
 
#         )
#     )
# asset_id = result.confirmation["asset-index"]
asset_id=736068347
# print(f"Asset ID: {asset_id}")




  


# res_asset = algorand.send.asset_create(
#         au.AssetCreateParams(
#             sender=Sarra.address,
#             signer=Sarra.signer,
#             total=15,
#             decimals=0,
#             default_frozen=False,
#         )
#     )

# asset_id = res_asset.confirmation["asset-index"]

# mbr_pay_txn = algorand.create_transaction.payment(
#         au.PaymentParams(
#             sender=Sarra.address,
#             receiver=ac.app_address,
#             amount=au.AlgoAmount(algo=0.2),
#             extra_fee=au.AlgoAmount(micro_algo=sp.min_fee),
#         )
#     )

# result = ac.send.opt_in_to_asset(
#         cl.OptInToAssetArgs(
#             mbr_pay=att.TransactionWithSigner(
#                 mbr_pay_txn,
#                 Sarra.signer
#             ),
#             asset=asset_id
#         ),
#         params=au.CommonAppCallParams(
#             box_references=[Sarra.address],
#             sender=Sarra.address,
#             signer=Sarra.signer,
#         ),
#         send_params=send_params
#     )

# result = ac.send.sum(
#         cl.SumArgs(
#             array=bytes([1, 2])
#         ),
#         params=au.CommonAppCallParams(
#             box_references=[Sarra.address],
#             sender=Sarra.address,
#             signer=Sarra.signer,
#         ),
#         send_params=send_params
#     )

result = ac.send.update_box(
        cl.UpdateBoxArgs(
            value="test"
        ),
        params=au.CommonAppCallParams(
            box_references=[Sarra.address],
            sender=Sarra.address,
            signer=Sarra.signer,
        ),
        send_params=send_params
    )



   

