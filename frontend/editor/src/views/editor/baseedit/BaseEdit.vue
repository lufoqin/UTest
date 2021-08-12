<template>
  <div>
    <el-header>
      <span style="font-size: 16px">常规编辑</span>
    </el-header>
    <el-collapse v-model="activeNames" @change="handleChange">
      <el-collapse-item name="1">
        <template slot="title">
          <h3>常规编辑 <i class="el-icon-edit"></i> </h3>
        </template>
        <new-edit></new-edit>
      </el-collapse-item>
      <el-collapse-item name="2">
        <template slot="title">
          <h3>字符串转换 <i class="el-icon-brush"></i></h3>
        </template>
        <parse-string></parse-string>
      </el-collapse-item>
    </el-collapse>

  </div>
</template>

<script>
import NewEdit from "@/views/editor/baseedit/NewEdit";
import ParseString from "@/views/editor/baseedit/ParseString";

export default {
  name: "BaseEdit",
  components: {
    ParseString,
    NewEdit
  },
  data() {
    return {
      activeNames: ['1']
    }
  },
  methods: {
    handleChange(val) {
      console.log(val);
    }
  }
}
</script>

<style scoped>
  .el-header {
    line-height: 30px;
  }
</style>