<template>
  <div id="app">

    <h1>Created Accounts per user</h1>
    <h6>since hardfork 20</h6>

    <b-container>
      <b-row>
        <b-col md="12">
          <b-table class="created-accounts-per-user" responsive small hover
                   :items="creators"
                   :fields="t1_fields"
                   :per-page="creators__per_page"
                   :current-page="currentPage"
          >
            <!-- A virtual column -->
            <template slot="index" slot-scope="data">
              {{ (creators__per_page * ((currentPage?currentPage:1)-1)) + data.index + 1}}
            </template>
          </b-table>
        </b-col>
      </b-row>

      <b-row>
        <b-col offset-md="4" md="4" align-h="end">
          <b-pagination align="center" :total-rows="creators.length" :per-page="creators__per_page" v-model="currentPage" class="my-0" />
        </b-col>
        <b-col md="4" >
          <b-form-group horizontal label="Per page">
            <b-form-row style="width: 100px; justify-content: flex-end;">
              <b-form-select :options="[10, 25, 50, 100, 500]" v-model="creators__per_page"/>
            </b-form-row>
          </b-form-group>
        </b-col>
      </b-row>
    </b-container>

    <b-container class="wide">
      <b-row>
        <b-col sm="12" xl="6" class="last-table col-xxl">
          <h2>Last claims</h2>
          <b-table style="max-width: 75%; margin: auto;" small :items="claims" :fields="[{key: 'timestamp', label:'When'}, 'creator']">
            <template slot="timestamp" slot-scope="data">
              <span :title="data.item.timestamp | moment('YYYY-MM-DD hh:mm:ss') + ' UTC'">{{data.item.timestamp | moment("from")}}</span>
            </template>
          </b-table>
        </b-col>

        <b-col sm="12" xl="6" class="last-table col-xxl">
          <h2>Last created accounts with claims</h2>
          <b-table small :items="create_claimed" :fields="[{key: 'timestamp', label:'When'}, 'creator', {key: 'new_account_name', label:'Account Created'}]">
            <template slot="timestamp" slot-scope="data">
              <span :title="data.item.timestamp | moment('YYYY-MM-DD hh:mm:ss') + ' UTC'">{{data.item.timestamp | moment("from")}}</span>
            </template>
          </b-table>
        </b-col>

        <b-col sm="12" xl="6" class="last-table col-xxl">
          <h2>Last created accounts with claims</h2>
          <b-table small :items="created_paid" :fields="[{key: 'timestamp', label:'When'}, 'creator', {key: 'new_account_name', label:'Account Created'}]">
            <template slot="timestamp" slot-scope="data">
              <span :title="data.item.timestamp | moment('YYYY-MM-DD hh:mm:ss') + ' UTC'">{{data.item.timestamp | moment("from")}}</span>
            </template>
          </b-table>
        </b-col>

      </b-row>
    </b-container>

    <footer>
      Current Steem irreversible block number: {{ prefs.current_block_num }}<br>
      Last block synced: {{ prefs.last_block_num_synced }}<br>
      Blocks behind: {{ prefs.blocks_behind }}<br>
      Last synced block timestamp: {{prefs.last_timestamp_synced | moment('YYYY-MM-DD hh:mm:ss') + ' UTC'}} ({{ prefs.last_timestamp_synced | moment("from") }})<br>
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
      t1_fields: [
        {
          key: 'index',
          label: '#',
        },
        {
          key: 'id',
          label: 'Account',
          sortable: true,
        },
        {
          key: 'claimed_accounts',
          sortable: true,
        },
        {
          key: 'created_discounted_accounts',
          sortable: true,
        },
        {
          key: 'created_paid_accounts',
          sortable: true,
        }
      ],
      creators: [],
      creators__per_page: 10,
      currentPage: 1,
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

a {
  color: #42b983;
}
h6 {
  margin-bottom: 30px;
}

.last-table {
  margin: 30px auto;
}

footer {
  padding: 50px 0;
  clear: both;
}

.col-xxl {
  @media (min-width: 1600px) {
  flex: 0 0 33%;
  max-width: 33%;
  }
}

@media (min-width: 1600px) {
  .wide {
    max-width: 1600px;
  }
}
</style>
