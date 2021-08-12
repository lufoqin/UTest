import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import store from './store/index'
import router from "./router";
import VueClipboard from 'vue-clipboard2'
import '@/assets/css/global.css'

Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.use(VueClipboard)
Vue.prototype.$store = store

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
