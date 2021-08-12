<template>
  <div>
    <el-dialog title="结果"
               :visible.sync="dialogVisible"
               append-to-body
                width="50%">
      <el-input
          type="textarea"
          placeholder="placeholder"
          v-model="resultTextarea"
          :autosize="autoSize">

      </el-input>

      <span slot="footer" class="dialog-footer">
        <el-button type="primary" size="small" v-clipboard:copy="resultTextarea"
                   v-clipboard:success="copySuccess"
                   v-clipboard:error="copyFail">
          <i class="el-icon-document-copy">
          </i> 点击复制</el-button>
        <el-button type="primary" size="small" @click="dialogVisible = false">确 定</el-button>
        <el-button size="small" @click="dialogVisible = false">取 消</el-button>
      </span>
    </el-dialog>


  </div>
</template>

<script>
export default {
  name: "ResultDialog",
  props: {
    textContent: '',
    fromDialogVisible: false
  },
  data() {
    return {
      autoSize: {"minRows": 5, "maxRows": 20},
      prettyText: '',
      resultTextarea: ''
    }
  },
  computed: {
    dialogVisible: {
      get() {
        if (!this.fromDialogVisible) {
          return this.fromDialogVisible
        } else {
          let prettyResult = this.pretty(this.textContent)
          if (prettyResult === false) {
            return false
          } else {
            this.resultTextarea = prettyResult
            return true
          }
        }

      },
      set() {
        this.$emit("changeDialogVisible", false)
      }
    }
  },
  methods:{
    pretty(text) {
      console.log(text);
      try {
        if (text) {
          let escapeStr = text.replaceAll('\\', '\\\\')  // 处理转义符 \
          return JSON.stringify(JSON.parse(escapeStr), null, 2).replaceAll('\\\\', '\\')
        } else {
          return "{}"
        }

      } catch (e) {
        console.log(e);
        this.showFormatErrorMsg()
        return false
      }
    },
    showFormatErrorMsg() {
      this.$message.error("生成结果失败，请检查各字段是否使用了单引号''或者是否存在json格式错误")
      this.$emit("changeDialogVisible", false)
    },
    copySuccess(e) {
      // console.log(e);
      this.$message.success("复制成功！")
    },
    copyFail(e) {
      // console.log(e);
      this.$message.error("复制失败！")
    }
  },
  watch: {
    // textContent: {
    //   deep: true,
    //   handler: function (val, oldVal) {
    //     console.log(val);
    //     if (val) {
    //       this.resultTextarea = this.pretty(val)
    //     } else {
    //       this.resultTextarea = ""
    //     }
    //
    //   }
    // },
  }
}
</script>

<style scoped>

</style>