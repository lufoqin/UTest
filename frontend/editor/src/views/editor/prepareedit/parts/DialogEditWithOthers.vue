<template>
  <div>
    <el-dialog :title="title" :visible.sync="isShow" width="65%">


      <span slot="footer">
        <el-button @click="isShow=false">取 消</el-button>
        <el-button type="primary" @click="save">保 存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "DialogEditWithOthers",


}
</script>

<style scoped>

</style>