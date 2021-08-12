<template>
  <el-col :span="span" :offset="offset">
    <slot></slot>
  </el-col>
</template>

<script>
export default {
  name: "ElColCustom",
  props: {
    span: {
      type: Number,
      default: 8
    },
    offset: {
      type: Number,
      default: 0
    }
  }
}
</script>

<style scoped>
  .el-col {
    border-radius: 4px;
  }
</style>