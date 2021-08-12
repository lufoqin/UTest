<template>
  <div>
    <el-container class="container">
      <el-header style="height: 40px">
        <div class="tool-bar">
          <div class="toolbar-left">
            <title-text text="字符串内容"></title-text>
          </div>
          <div class="toolbar-right">
            <el-button class="ok-btn" type="primary" size="small" @click="creator" @keyup.enter="creator">确定</el-button>
            <el-button class="cancel-btn" type="primary" size="small" @click="clearInputValue">清空</el-button>
          </div>
        </div>
      </el-header>
      <el-main>
        <div>
          <el-input
            class="str-input"
            type="textarea"
            placeholder="请输入待解析的字符串"
            v-model="textarea"
            :rows="4"
            :autosize="textareaAutoSize"
            :clearable="clearable">
          </el-input>
        </div>
      </el-main>
    </el-container>
    <result-dialog :text-content="resultTextarea"
                   :from-dialog-visible="dialogVisible"
                   @changeDialogVisible="changeDialogVisible"></result-dialog>

  </div>
</template>

<script>
import TitleText from "@/views/editor/common/TitleText";
import ResultDialog from "@/views/editor/common/result/ResultDialog";

export default {
  name: "ParseString",
  components: {
    ResultDialog,
    TitleText
  },
  data() {
    return {
      textarea: '',
      clearable: true,
      textareaAutoSize: {"minRows": 5, "maxRows": 50},
      resultTextarea: '',
      dialogVisible: false
    }
  },
  methods: {
    creator() {
      const s = this.textarea
      let itemList
      let result = '{'
      if (s.substr(0, 1) === '{') {
        itemList = s.slice(1, s.length-1).split(',')
        // console.log(itemList);
      } else {
        itemList = s.split('\n')
      }
      let reg = /(\S+):\s*(.+)/
      for (let i=0; i<itemList.length; i++) {
        let res = reg.exec(itemList[i])
        // console.log(res);
        if (res) {
          if (res[1].substr(0, 1) === '"' || res[1].substr(0, 1) === "'"){
            result = result + res[1] +":"
          } else {
            result = result + "'" + res[1] + "'" + ':'
          }
          if (res[2].substr(0, 1) === '"' || res[2].substr(0, 1) === "'") {
            result =  result + res[2] + ","
          } else {
            result = result + "'" + res[2] + "'" + ","
          }
        }
      }
      result = result.slice(0, result.length-1)
      result = result + "}"
      if (result === '}') {
        result = "{'':''}"
      }
      this.resultTextarea = result
      this.dialogVisible = true
    },
    clearInputValue() {
      this.textarea = ''
      this.resultTextarea = ''
    },
    changeDialogVisible(val) {
      this.dialogVisible = val
    }
  },
}
</script>

<style scoped>
  .tool-bar {
    display: block;
    text-align: right;
    margin-top: 8px;
    margin-bottom: 8px;
  }
  .toolbar-left {
    float: left;
    margin-top: 8px;
    margin-bottom: 8px;
  }
  .toolbar-right {
    float: right;
    margin-top: 8px;
    margin-bottom: 8px;
    margin-right: 20px;
  }
  .container {
    height: 400px;
    border: 1px;
    solid-color: #eeeeee;
  }

  .str-input {
    width: 90%;
    margin-left: 5px;
    margin-top: 20px;
  }
</style>