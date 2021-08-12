<template>
  <div class="case-header">
    <el-row-custom class="re-row">
      <el-col-custom class="sub-title-text" :span="2">
        <span>{{titleText}}</span>
      </el-col-custom>
      <el-col-custom :span="5">
        <json-edit-by-dialog :title="titleText" @getResultStr="handleSubResult" :parent-reset-state="resetState"></json-edit-by-dialog>
      </el-col-custom>
      <el-col-custom class="display-input" v-show="isShow">
        <display-input :content="cResultContent" :parent-reset-state="resetState" @resetTextarea="subResetTextarea"></display-input>
      </el-col-custom>
    </el-row-custom>
  </div>
</template>

<script>
import ElRowCustom from "@/views/editor/common/elrowcustom/ElRowCustom";
import ElColCustom from "@/views/editor/common/elrowcustom/ElColCustom";
import JsonEditByDialog from "@/views/editor/common/jsoneditor/JsonEditByDialog";
import DisplayInput from "@/views/editor/common/result/DisplayInput";
import ParseString from "@/views/editor/baseedit/ParseString";
export default {
  name: "SubJsonItem",
  components: {ElRowCustom, ElColCustom, JsonEditByDialog, DisplayInput},
  props: {
    titleText:'',
    showResult: false,
    resultContent: '',
    parentResetState: false
  },
  data() {
    return {
      resetState: this.parentResetState,
      isShow: this.showResult,
      cResultContent: this.resultContent
    }
  },
  computed: {

  },
  methods: {
    handleSubResult(arg) {
      this.$emit("handleSubItemResult", arg)
    },
    subResetTextarea(val) {
      this.cResultContent = val
    }
  },
  watch: {
    "parentResetState": {
      handler: function () {
        this.resetState = !this.resetState
        this.cResultContent = ""
      }
    },
    showResult() {
      this.isShow = this.showResult
    },
    resultContent() {
      this.cResultContent = this.resultContent
    }
  }
}
</script>

<style scoped>
  .case-header /deep/ .row {
    justify-content: flex-start;
    flex: 1;
  }
  .re-row {
    margin-top: 8px;
    margin-bottom: 8px;
  }
  .sub-title-text {
    margin-left: 20px;
    margin-top: 8px;
    margin-bottom: 8px;
    text-align: left;

  }
  .display-input {
    margin-top: 8px;
    margin-bottom: 8px;
  }
</style>