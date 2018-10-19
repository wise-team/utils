import Vue from 'vue'
import App from './App.vue'
import VueFire from 'vuefire'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'


Vue.use(VueFire);
Vue.use(BootstrapVue);
Vue.use(require('vue-moment'));

new Vue({
  el: '#app',
  render: h => h(App),
});
