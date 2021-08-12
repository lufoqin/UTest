<template>
  <div>
    <el-row class="row" type="flex" :gutter="gutter">
      <slot></slot>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "ElRowCustom",
  props: {
    gutter: {
      type: Number,
      default: 0
    }
  }

}
</script>

<style scoped>
  .row {
    justify-content: space-between;

  }
</style>