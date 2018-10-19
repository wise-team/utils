from beem.blockchain import Blockchain
import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


account_creators = db.collection("account_creators")
ops = db.collection("ops")
claim_account = db.collection("claim_account")
create_claimed_account = db.collection("create_claimed_account")
account_create = db.collection("account_create")
global_preferences = db.collection("preferences").document("global")

blockchain = Blockchain()

default_fields = {
    "claimed_accounts": 0,
    "pending_claimed_accounts": 0,
    "created_paid_accounts": 0,
    "created_discounted_accounts": 0,
    "created_accounts": 0,
}


@firestore.transactional
def new_claim_account(transaction, op):
    creator_doc_ref = account_creators.document(op["creator"])
    fields = creator_doc_ref.get(transaction=transaction).to_dict()

    transaction.set(document_data=op, reference=claim_account.document(op["trx_id"]))
    transaction.set(document_data=op, reference=ops.document(op["trx_id"]))
    transaction.set(document_data=op, reference=creator_doc_ref.collection('claims').document(op["trx_id"]))

    if not fields:
        fields = default_fields.copy()
        transaction.set(document_data=fields, reference=creator_doc_ref)

    fields["claimed_accounts"] += 1
    fields["pending_claimed_accounts"] += 1
    transaction.update(field_updates=fields, reference=creator_doc_ref)


@firestore.transactional
def new_create_claimed_account(transaction, op):
    new_account_name = op["new_account_name"]
    creator_doc_ref = account_creators.document(op["creator"])
    created_discounted_accounts = creator_doc_ref.collection('created_discounted_accounts').document(new_account_name)
    fields = creator_doc_ref.get(transaction=transaction).to_dict()

    del op['owner']
    del op['active']
    del op['posting']

    transaction.set(document_data=op, reference=create_claimed_account.document(op["trx_id"]))
    transaction.set(document_data=op, reference=ops.document(op["trx_id"]))
    transaction.set(document_data=op, reference=created_discounted_accounts)

    if not fields:
        fields = default_fields.copy()
        transaction.set(document_data=fields, reference=creator_doc_ref)

    fields["pending_claimed_accounts"] -= 1
    fields["created_discounted_accounts"] += 1
    fields["created_accounts"] += 1

    transaction.update(field_updates=fields, reference=creator_doc_ref)


@firestore.transactional
def new_account_create(transaction, op):
    new_account_name = op["new_account_name"]
    creator_doc_ref = account_creators.document(op["creator"])
    fields = creator_doc_ref.get(transaction=transaction).to_dict()
    created_paid_accounts = creator_doc_ref.collection('created_paid_accounts').document(new_account_name)

    del op['owner']
    del op['active']
    del op['posting']

    transaction.set(document_data=op, reference=account_create.document(op["trx_id"]))
    transaction.set(document_data=op, reference=ops.document(op["trx_id"]))
    transaction.set(document_data=op, reference=created_paid_accounts)

    if not fields:
        fields = default_fields.copy()
        transaction.set(document_data=fields, reference=creator_doc_ref)

    fields["created_paid_accounts"] += 1
    fields["created_accounts"] += 1

    transaction.update(field_updates=fields, reference=creator_doc_ref)


transaction = db.transaction()
pref = global_preferences.get().to_dict()
last_block_num_synced = pref['last_block_num_synced'] if pref else 26256743 - 1  # HF20 -1
last_block_num = last_block_num_synced + 1

for op in blockchain.stream(
    opNames=[
        'claim_account',
        'create_claimed_account',
        'account_create',
    ],
    # start=26256743, # first block of HF20
    # start=26265398, # first block after HF20 with `create_claimed_account` op
    # start=26289186, # first block after HF20 with `create_account` op
    start=last_block_num_synced + 1,
    max_batch_size=50,
):

    print(op)
    op["timestamp"] = op["timestamp"].__str__()

    if last_block_num < op['block_num']:  # that means that all ops from last_block are already synced
        last_block_num_synced = op['block_num'] - 1
        current_block_num = blockchain.get_current_block_num()
        transaction.set(global_preferences, {
            "last_block_num_synced": last_block_num_synced,
            "current_block_num": current_block_num,
            "blocks_behind": current_block_num - op['block_num'],
            "last_trx_id_synced": op["trx_id"],
            "last_timestamp_synced": op["timestamp"],
        })

        transaction.commit()
        transaction = db.transaction()

    last_block_num = op['block_num']

    if op["type"] == "claim_account":
        new_claim_account(transaction, op)

    elif op['type'] == 'create_claimed_account':
        new_create_claimed_account(transaction, op)

    elif op['type'] == 'account_create':
        new_account_create(transaction, op)
