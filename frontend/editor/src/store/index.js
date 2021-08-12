import Vue from "vue";
import Vuex from 'vuex'
// 挂载vuex

Vue.use(Vuex)

// 创建vuex对象并向外暴露
export default new Vuex.Store({
  //全局性变量
  state: {
    // 所有input框的 v-model值
    singleJsonInputCleanState: false,
    prepareState: false,
    globalSettings: {
      headerManager: '',
      verifyFields: '',
      statusCode: '',
      resText: '',
      waitTime: '',
      resTime: ''
    }
  },

  // 全局同步方法，调用方法：this.$store.commit('funcName')
  mutations: {
    resetSingleJsonInputCleanState(state) {
      state.singleJsonInputCleanState = !state.singleJsonInputCleanState
    },

    resetPrepare(state) {
      state.prepareState = !state.prepareState
    }
  },

  // 异步方法 ，调用方法：this.$store.dispatch('funcName')
  actions: {

  },

  // Vuex 属性计算，在视图里面当变量使用
  getters: {

  },

  // 模块化注册
  modules: {

  },
})