from beem.blockchain import Blockchain
import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


claim_account = db.collection("claim_account")
claimed_accounts_per_user = db.collection("claimed_accounts_per_user")
create_claimed_account = db.collection("create_claimed_account")

blockchain = Blockchain()
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

    if op["type"] == "claim_account":
        creator = op["creator"]
        trx_id = op["trx_id"]

        claim_account.document(trx_id).set(op)


        creator_doc_ref = claimed_accounts_per_user.document(creator)
        creator_doc_ref.collection('claims').document(trx_id).set(op)

        fields = creator_doc_ref.get().to_dict()
        if not fields:
            fields = {
                "claimed_accounts": 0,
                "pending_claimed_accounts": 0,
                "created_paid_accounts": 0,
                "created_discounted_accounts": 0,
                "created_accounts": 0,
            }
            creator_doc_ref.set(fields)

        fields["claimed_accounts"] += 1
        fields["pending_claimed_accounts"] += 1
        creator_doc_ref.update(fields)

    elif op['type'] == 'create_claimed_account':
        print('create_claimed_account')

        creator = op["creator"]
        trx_id = op["trx_id"]
        new_account_name = op["new_account_name"]

        del op['owner']
        del op['active']
        del op['posting']

        create_claimed_account.document(trx_id).set(op)

        creator_doc_ref = claimed_accounts_per_user.document(creator)
        creator_doc_ref.collection('created_discounted_accounts').document(new_account_name).set(op)

        fields = creator_doc_ref.get().to_dict()
        if not fields:
            fields = {
                "claimed_accounts": 0,
                "pending_claimed_accounts": 0,
                "created_paid_accounts": 0,
                "created_discounted_accounts": 0,
                "created_accounts": 0,
            }
            creator_doc_ref.set(fields)

        fields["pending_claimed_accounts"] -= 1
        fields["created_discounted_accounts"] += 1
        fields["created_accounts"] += 1

        creator_doc_ref.update(fields)

    elif op['type'] == 'account_create':
        print('account_create')
