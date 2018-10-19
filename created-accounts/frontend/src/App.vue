<template>
  <div id="app">
    <div class="main-section">
      <h1>Created Accounts by user</h1>
      <table>
        <thead>
          <tr>
            <td>#</td>
            <td>Creator</td>
            <td>Claimed Accounts</td>
            <td>Created Discounted Accounts</td>
            <td>Created Paid Accounts</td>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(creator, index) of creators" v-bind:key="creator['.key']">
            <td>{{ index + 1 }}</td>
            <td>{{creator.id}}</td>
            <td>{{creator.claimed_accounts}}</td>
            <td>{{creator.created_discounted_accounts}}</td>
            <td>{{creator.created_paid_accounts}}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="subsection">
      <h2>Last claims</h2>
      <table>
        <thead>
          <tr>
            <td>#</td>
            <td>Date</td>
            <td>Creator</td>
          </tr>
        </thead>
        <tbody>
          <tr v-for="claim of claims" v-bind:key="claim['.key']">
            <td>&nbsp;</td>
            <td>{{claim.timestamp}}</td>
            <td>{{claim.creator}}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="subsection">
      <h2>Last created accounts with claims</h2>
      <table>
        <thead>
          <tr>
            <td>#</td>
            <td>Date</td>
            <td>Creator</td>
            <td>Account Created</td>
          </tr>
        </thead>
        <tbody>
          <tr v-for="account of create_claimed" v-bind:key="account['.key']">
            <td>&nbsp;</td>
            <td>{{account.timestamp}}</td>
            <td>{{account.creator}}</td>
            <td>{{account.new_account_name}}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="subsection">
      <h2>Last created paid accounts</h2>
      <table>
        <thead>
          <tr>
            <td>#</td>
            <td>Date</td>
            <td>Creator</td>
            <td>Account Created</td>
          </tr>
        </thead>
        <tbody>
          <tr v-for="account of created_paid" v-bind:key="account['.key']">
            <td>&nbsp;</td>
            <td>{{account.timestamp}}</td>
            <td>{{account.creator}}</td>
            <td>{{account.new_account_name}}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <footer>
      Current Steem irreversible block number: {{ prefs.current_block_num }}<br>
      Last block synced: {{ prefs.last_block_num_synced }}<br>
      Blocks behind: {{ prefs.blocks_behind }}<br>
      Last synced block timestamp: {{ prefs.last_timestamp_synced }}<br>
    </footer>
  </div>
</template>

<script>
import {
  account_creators,
  claim_account,
  global_preferences,
  create_claimed_account,
  created_paid_accounts
} from './firebase';

export default {
  name: 'app',
  data () {
    return {
      creators: [],
      claims: [],
      create_claimed: [],
      created_paid: [],
      msg: 'Welcome to Your Vue.js App',
      prefs: {
        blocks_behind: '?',
        current_block_num: '?',
        last_block_num_synced: '?',
        last_timestamp_synced: '?',
        last_trx_id_synced: '?',
      }
    }
  },
  firestore () {
    return {
      creators: account_creators,
      claims: claim_account,
      create_claimed: create_claimed_account,
      created_paid: created_paid_accounts,
      prefs: global_preferences,
    }
  }
}
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}

.main-section{
  margin: 0 calc(50% - 400px);
}

.subsection {
  float: left;
  width: 33%;
  padding: 0 50px;
  box-sizing: border-box;
}

footer {
  padding-top: 50px;
  clear: both;
}
</style>
