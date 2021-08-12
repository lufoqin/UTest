<template>
  <div>
    <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
<!--    <slot></slot>-->
    </el-tabs>
  </div>

</template>
<script>
  export default {
    name: "TabBar",
    data() {
      return {
        activeName: ''
      };
    },
    methods: {
      handleClick(tab, event) {
        console.log(tab, event);
      }
    }
  };
</script>

<style scoped>

</style>