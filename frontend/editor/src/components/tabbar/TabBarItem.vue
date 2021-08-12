<template>
  <div>
      <el-tab-pane label="配置管理" name="second">
<!--    <slot name="item"></slot>-->
        tabbar name
      </el-tab-pane>
  </div>

</template>

<script>
export default {
  name: "TabBarItem",
  props: {
    tabName: ''
  }
}
</script>

<style scoped>

</style>