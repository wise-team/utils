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

blockchain = Blockchain()

default_fields = {
    "claimed_accounts": 0,
    "pending_claimed_accounts": 0,
    "created_paid_accounts": 0,
    "created_discounted_accounts": 0,
    "created_accounts": 0,
}

for op in blockchain.stream(
    opNames=[
        'claim_account',
        'create_claimed_account',
        'account_create',
    ],
    start=26256743, # HF20
    # start=26265398, # create_claimed_account
    # start=26289186, # create_account
):

    print(op)
    op["timestamp"] = op["timestamp"].__str__()
    creator = op["creator"]
    trx_id = op["trx_id"]

    if op["type"] == "claim_account":
        claim_account.document(trx_id).set(op)
        ops.document(trx_id).set(op)

        creator_doc_ref = account_creators.document(creator)
        creator_doc_ref.collection('claims').document(trx_id).set(op)

        fields = creator_doc_ref.get().to_dict()
        if not fields:
            fields = default_fields.copy()
            creator_doc_ref.set(fields)

        fields["claimed_accounts"] += 1
        fields["pending_claimed_accounts"] += 1
        creator_doc_ref.update(fields)

    elif op['type'] == 'create_claimed_account':
        new_account_name = op["new_account_name"]

        del op['owner']
        del op['active']
        del op['posting']

        create_claimed_account.document(trx_id).set(op)
        ops.document(trx_id).set(op)

        creator_doc_ref = account_creators.document(creator)
        creator_doc_ref.collection('created_discounted_accounts').document(new_account_name).set(op)

        fields = creator_doc_ref.get().to_dict()
        if not fields:
            fields = default_fields.copy()
            creator_doc_ref.set(fields)

        fields["pending_claimed_accounts"] -= 1
        fields["created_discounted_accounts"] += 1
        fields["created_accounts"] += 1

        creator_doc_ref.update(fields)

    elif op['type'] == 'account_create':
        new_account_name = op["new_account_name"]

        del op['owner']
        del op['active']
        del op['posting']

        account_create.document(trx_id).set(op)
        ops.document(trx_id).set(op)

        creator_doc_ref = account_creators.document(creator)
        creator_doc_ref.collection('created_paid_accounts').document(new_account_name).set(op)

        fields = creator_doc_ref.get().to_dict()
        if not fields:
            fields = default_fields.copy()
            creator_doc_ref.set(fields)

        fields["created_paid_accounts"] += 1
        fields["created_accounts"] += 1

        creator_doc_ref.update(fields)
