<template>
  <div>
    <el-container class="container">
      <el-header style="height: 40px">
        <div>
          <conten-tool-bar>
            <template #text>参数信息</template>
            <template #addClick>
              <el-button type="primary" size="medium" @click="addInputList">添加</el-button>
            </template>
            <template #okClick>
              <el-button class="ok-btn" type="primary" size="medium" @click="creator">确定</el-button>
            </template>
            <template #clearClick>
              <el-button class="cancel-btn" type="primary" size="medium" @click="clearInputValue">清空</el-button>
            </template>
          </conten-tool-bar>
        </div>
      </el-header>
      <el-main>
        <el-row class="input" type="flex" v-for="index in inputList" :key="index">
          <Input @inputChange="inputChange" :index="index" :parent-reset-state="resetState"></Input>
          <el-col class="delete-btn" :span="2">
            <el-button size="medium" @click="deleteCurrentInput(index)">删除</el-button>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
    <result-dialog :text-content="resultTextarea"
                   :from-dialog-visible="dialogVisible"
                   @changeDialogVisible="changeDialogVisible">

    </result-dialog>
  </div>
</template>

<script>
import TitleText from "@/views/editor/common/TitleText";
import Input from "@/views/editor/common/inputfield/Input";
import ResultTextarea from "@/views/editor/common/result/ResultDialog";
import ResultDialog from "@/views/editor/common/result/ResultDialog";
import ContenToolBar from "@/views/editor/common/toolbar/ContenToolBar";

export default {
  name: "NewEdit",
  components: {
    ContenToolBar,
    ResultDialog,
    TitleText,
    Input,
    ResultTextarea,
  },
    data() {
      return {
        currentInputIndex: 2,
        showFlag: true,
        inputList: [
          0, 1, 2
        ],
        paramDict: {},
        resultTextarea: '',
        isAutofocus: true,
        dialogVisible: false,

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
      this.resultTextarea = ''
    },
    creator() {
      // console.log('in creator');
      let allParam = this.paramDict
      let toDict = {}
      let desStr = "{"
      for (let item of Object.keys(allParam)) {
        const itemV = allParam[item]
        let key = Object.keys(itemV)[0]
        toDict[key] = itemV[key]
        if (key.substr(0,1) === '"' || key.substr(0,1) === "'") {
          desStr = desStr + key + ":"
        }else {
          desStr = desStr + '"' + key + '"' + ":"
        }
        if (itemV[key].substr(0,1) === '"' || itemV[key].substr(0,1) === "'") {
          desStr = desStr + itemV[key] + ","
        }else {
          desStr = desStr + '"' + itemV[key] + '"' + ","
        }
      }
      desStr = desStr.slice(0, desStr.length-1)
      desStr = desStr + "}"
      if (desStr === '}') {
        desStr = '{}'
      }
      this.resultTextarea = desStr
      this.dialogVisible = true
    },
    changeDialogVisible(val) {
      this.dialogVisible = val
    }
  }
}
</script>

<style scoped>
  .tool-bar {
    display: block;
    text-align: right;
    margin-top: 8px;
    margin-bottom: 8px;
    /*width: 100%;*/
  }
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
  .delete-btn {
    /*margin-top: 4px;*/
    /*margin-bottom: 4px;*/
    /*margin-right: 10px;*/
  }
  .ok-btn {
    margin-right: auto;
  }
  .cancel-btn {
    /*margin-right: 1px;*/
  }


</style>