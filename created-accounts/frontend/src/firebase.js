import { initializeApp, firestore } from "firebase";

const app = initializeApp ({
    apiKey: "AIzaSyA4XcCSxF4NutBr0Q5IQC2vmfjK86J0MKo",
    authDomain: "created-accounts.firebaseapp.com",
    databaseURL: "https://created-accounts.firebaseio.com",
    projectId: "created-accounts",
    storageBucket: "created-accounts.appspot.com",
    messagingSenderId: "719280083462"
});

export const db = firestore();
export const account_creators = db.collection('account_creators').orderBy('claimed_accounts', "desc")

let limit = 15;
export const claim_account = db.collection('claim_account').orderBy('timestamp', "desc").limit(limit);
export const create_claimed_account = db.collection('create_claimed_account').orderBy('timestamp', "desc").limit(limit);
export const created_paid_accounts = db.collection('account_create').orderBy('timestamp', "desc").limit(limit);

export const global_preferences = db.collection('preferences').doc('global');
