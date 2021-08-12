<template>
  <div class="load-more">
    <el-divider></el-divider>
    <div><i class="el-icon-caret-bottom"></i>{{text}}</div>
<!--    <el-divider></el-divider>-->
  </div>
</template>

<script>
export default {
  name: "OpenPlate",
  props: {
    text: {
      type: String,
      default: '点击加载更多'
    }
  }
}
</script>

<style scoped>
  .load-more {
    height: auto;
  }
  .more-options {
    background: #fafafa;
  }
  .load-more:hover {
    /*background: #eeeeee;*/
    color: #51a7e8;
    cursor: pointer;
  }
</style>