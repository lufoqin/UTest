<template>
  <div>
    <el-button type="text" @click="dialogVisible = true">点击打开编辑器</el-button>
    <el-dialog width="70%" :title="title + '编辑'" :visible.sync="dialogVisible" :before-close="handleClose">
      <el-container class="container">
        <el-header height="60px">
          <tool-bar>
            <tool-bar-item :span="2">
              参数信息
            </tool-bar-item>
            <tool-bar-item :span="2">
              <el-button type="primary" size="medium" @click="addInputList">添加</el-button>
            </tool-bar-item>
            <tool-bar-item :span="2" :offset="10">
              <el-button class="ok-btn" type="primary" size="medium" @click="creator">确定</el-button>
            </tool-bar-item>
            <tool-bar-item :span="2">
              <el-button class="cancel-btn" type="primary" size="medium" @click="clearInputValue">清空</el-button>
            </tool-bar-item>
          </tool-bar>
        </el-header>

        <el-main>
          <el-row-custom class="input" type="flex" v-for="index in inputList" :key="index">
            <input-dialog @inputChange="inputChange" :index="index" :parent-reset-state="resetState"></input-dialog>
            <el-col-custom class="delete-btn" :span="2">
              <el-button size="medium" @click="deleteCurrentInput(index)">删除</el-button>
            </el-col-custom>
          </el-row-custom>

          <parse-string-input-field @stringRes="parseStringRes" :parent-reset-state="resetState"></parse-string-input-field>
        </el-main>
      </el-container>
    </el-dialog>
  </div>
</template>

<script>
import ElRowCustom from "@/views/editor/common/elrowcustom/ElRowCustom";
import ElColCustom from "@/views/editor/common/elrowcustom/ElColCustom";
import ToolBar from "@/views/editor/common/toolbar/ToolBar";
import ToolBarItem from "@/views/editor/common/toolbar/ToolBarItem";
import InputDialog from "@/views/editor/common/inputfield/InputDialog";
import ParseStringInputField from "@/views/editor/common/inputfield/ParseStringInputField";

export default {
name: "JsonEditByDialog",
  components: {ParseStringInputField, ElRowCustom, ElColCustom, ToolBarItem, ToolBar, InputDialog},
  props: {
    title: '',
    parentResetState: false
  },
  data() {
    return {
      currentInputIndex: 2,
      showFlag: true,
      inputList: [
        0, 1, 2
      ],
      paramDict: {},
      isAutofocus: true,
      dialogVisible: false,

      stringRes: '',

      resetState: false
    }
  },
  methods: {
    inputChange(arg) {
      // console.log(arg);
      let ky=arg[0]
      let val = arg[1]
      let id = arg[2]
      this.paramDict[id] = {}
      this.paramDict[id][ky] = val
    },
    addInputList() {
      this.currentInputIndex ++
      this.inputList.push(this.currentInputIndex)
    },
    deleteCurrentInput(index) {
      if (this.inputList.length > 1){
              this.inputList.splice(index-1, 1)
      delete this.paramDict[index]
      }
    },
    clearInputValue() {
      // console.log('-----reload');
      this.paramDict = {}
      this.resetState = !this.resetState
    },
    parseStringRes(arg) {
      // 解析由输入框返回的字符
      console.log('====arg');
      console.log(arg);
      if (arg != "{'':''}") {
        this.stringRes = arg.slice(1, arg.length-1)
      } else {
        this.stringRes = ''
      }
    },
    creator() {
      console.log('in creator');
      let allParam = this.paramDict
      let toDict = {}
      let desStr = "{"
      // 拼接由文本输入框输入的内容
      if (this.stringRes != '') {
        desStr = desStr + this.stringRes + ","
      }
      for (let item of Object.keys(allParam)) {
        const itemV = allParam[item]

        let key = Object.keys(itemV)[0]
        if (!key) {
          continue
        }
        toDict[key] = itemV[key]
        // 如果输入框的字符是以' 或者 " 开头的，则不添加'符号
        if (key.substr(0,1) === '"' || key.substr(0,1) === "'") {
          desStr = desStr + key + ":"
        }else {
          desStr = desStr + "'" + key + "'" + ":"
        }
        if (itemV[key].substr(0,1) === '"' || itemV[key].substr(0,1) === "'") {
          desStr = desStr + itemV[key] + ","
        }else {
          desStr = desStr + "'" + itemV[key] + "'" + ","
        }
      }
      desStr = desStr.slice(0, desStr.length-1) // 去掉最后一组多余的,号
      desStr = desStr + "}"
      if (desStr === '}') {
        desStr = ''
      }
      this.$emit("getResultStr", desStr)
      this.changeDialogVisible(false)
    },
    changeDialogVisible(val) {
      this.dialogVisible = val
    },
    handleClose() {
      this.$confirm("是否保存已编辑的内容？")
      .then(_ => {
        this.creator()
        this.changeDialogVisible(false)
      })
      .catch(_ => {
        this.clearInputValue()
        this.changeDialogVisible(false)
      })
    }
  },
  watch: {
    "parentResetState": {
      handler: function () {
        this.resetState = !this.resetState
        this.paramDict = {}
      }
    }
  }
}
</script>

<style scoped>
  .container {
    height: 400px;
    border: 1px;
    solid-color: #eeeeee;
  }
  .input {
    margin-top: 4px;
    margin-bottom: 4px;
    flex: 1;
    justify-content: space-between;
  }
</style>