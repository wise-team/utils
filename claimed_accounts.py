from beem.blockchain import Blockchain
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


claim_account = db.collection("claim_account")
claimed_accounts_per_user = db.collection("claimed_accounts_per_user")

blockchain = Blockchain()
for op in blockchain.stream(opNames=['claim_account'], start=26256743):
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
