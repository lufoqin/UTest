<template>
  <el-col-custom :span="1">
    <span class="name">
    {{text}}
    </span>
  </el-col-custom>

</template>

<script>
import ElColCustom from "@/views/editor/common/elrowcustom/ElColCustom";

export default {
  name: "PartNameText",
  components: {ElColCustom},
  props: {
    text: ''
  }
}
</script>

<style scoped>
  .name {
    font-size: 15px;
    margin-left: 17px;
  }
</style>