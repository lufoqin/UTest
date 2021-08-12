import Vue from 'vue'
import VueRouter from 'vue-router'

// const Home = () => import('../views/editor/baseedit/BaseEdit.vue')
const BaseEdit = () => import('../views/editor/baseedit/BaseEdit')
const PrepareEdit = () => import('../views/editor/prepareedit/PrepareEdit')
const DbEidt = () => import('../views/editor/dbedit/DbEdit')
const DyParam = () => import('../views/editor/dyparamedit/DyParamEdit')

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/prepare'
  },
  {
    path: '/home',
    redirect: '/prepare'
  },
  {
    path: '/base',
    redirect: '/prepare'
  },
  {
    path: '/prepare',
    name: 'Prepare',
    component: PrepareEdit
  },
  {
    path: '/db',
    name: 'Db',
    component: DbEidt
  },
  {
    path: '/dyparam',
    name: 'Dyparam',
    component: DyParam
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
