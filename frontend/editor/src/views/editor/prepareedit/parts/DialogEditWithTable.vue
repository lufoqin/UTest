<template>
  <div>
    <el-dialog :title="title" :visible.sync="isShow" width="65%">
      <table-item :item-height="tableHeight"
                  :is-active="isActive"
                  :is-submit="isOk"
                  :cancel-close="cancelClose"
                  :reset-flag="resetState"
                  :init-data="existData"
                  :clear-after-submit="true"
                  @receiveTableData="handleTableData">

      </table-item>

      <span slot="footer">
        <el-button @click="cancel">取 消</el-button>
        <el-button type="primary" @click="save">保 存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import TableItem from "@/views/editor/common/table/TableItem";
export default {
  name: "DialogEditWithTable",
  components: {TableItem},
  props: {
    title: '',
    resetState: false,
    showSymbol: false,
    existData: ''
  },
  data() {
    return {
      isOk: false,
      cancelClose: false,
      tableHeight: 0,
      isActive: false,
      result: ''
    }
  },

  computed: {
    isShow: {
      get() {
        return this.showSymbol
      },
      set(val) {
        this.$emit("changeDialogShow", val)
      }
    }
  },
  methods: {
    save() {
      this.isOk = true
    },

    cancel() {
      this.isShow = false
      this.cancelClose = !this.cancelClose
    },

    handleTableData(data) {
      if (data === "{}") {
        this.result = ''
      } else {
        this.result = data
      }
      this.$emit("handleResult", this.result)
      this.resumeSymbol()
    },

    resumeSymbol() {
      this.isShow = false
      this.isOk = false
    },

    // 设置table高度
    fetTableHeight() {
      this.tableHeight = this.windowHeight / 2

    },

    getScreenHeight() {
       return window.screen.availHeight
    },
  },

  watch: {
    "showSymbol": {
      handler: function () {
        if (this.showSymbol) {
          new Promise(resolve => {
            this.fetTableHeight()
            resolve()
          }).then(res => {
            this.isActive = !this.isActive
          })
        }
      }
    }
  },
  mounted() {
    this.windowHeight = this.getScreenHeight()
    // console.log(this.windowHeight);
  },

}


</script>

<style scoped>

</style>