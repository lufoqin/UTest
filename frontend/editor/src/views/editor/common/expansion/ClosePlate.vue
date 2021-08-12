<template>
  <div class="hidden-more">
    <el-divider></el-divider>
    <div><i class="el-icon-caret-top"></i>{{text}}</div>
<!--    <el-divider></el-divider>-->
  </div>
</template>

<script>
export default {
  name: "ClosePlate",
  props: {
    text: {
      type: String,
      default: '点击隐藏'
    }
  }
}
</script>

<style scoped>
  .hidden-more {
    height: auto;
  }
  .hidden-more:hover {
    /*background: #eeeeee;*/
    color: #51a7e8;
    cursor: pointer;
  }
</style>