<template>
  <el-menu-item :index="index">
    <slot></slot>
  </el-menu-item>
</template>

<script>
export default {
  name: "NarMenuItem",
  props: {
    index: ''
  }
}
</script>

<style scoped>

</style>