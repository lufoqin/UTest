<template>
  <div>
    <el-card shadow="always" class="tools-card" :body-style="{ padding: '3px 0' }">

      <el-row>
        <el-col :span="2">
          <el-tooltip effect="dark" content="新增步骤" placement="top-end">
            <el-button
              type="primary"
              size="small"
              @click="addItemList">
              <i class="el-icon-document-add"></i> 新增
            </el-button>
          </el-tooltip>

        </el-col>

        <el-col :span="2">
          <el-tooltip effect="dark" content="生成所有步骤的结果" placement="top-end">
            <el-button
              type="primary"
              size="small"
              @click="notifyComponentTransmit">
              <i class="el-icon-thumb"></i> 确定
            </el-button>
          </el-tooltip>
        </el-col>

        <el-col :span="3">
          <el-tooltip effect="dark" content="全局配置" placement="top-start">
            <el-dropdown @command="handleDropdownCommand">
              <el-button type="info" size="small">
                <i class="el-icon-setting"></i> 全局配置<i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="header">请求头管理</el-dropdown-item>
                <el-dropdown-item command="verifyFields">校验字段管理</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </el-tooltip>
        </el-col>

        <el-col :span="2">
          <el-tooltip effect="dark" content="清空所有步骤的内容" placement="top-start">
            <el-button
              type="danger"
              size="small"
              @click="reset">
              <i class="el-icon-delete"></i> 清空
            </el-button>
          </el-tooltip>
        </el-col>

      </el-row>

    </el-card>
      <el-main style="padding: 0 5px">
      <el-tabs v-model="editableTabsValue" type="border-card">
        <el-tab-pane
          v-for="(item, index) in itemList"
          :key="item.index"
          :label="item.title"
          :name="item.name">
          <prepare-edit-item
              :step-index="item.index"
              :key="item.index"
              :submit-flag="submitFlag"
              @receiveData="handleData"
              :parent-reset-state="resetState">

          </prepare-edit-item>
        </el-tab-pane>
      </el-tabs>
    </el-main>

    <dialog-edit-with-table :show-symbol="globalSettings.showHeaderManager"
                            title="请求头管理"
                            :exist-data="headerManagerData"
                            @handleResult="handleHeaderManagerData"
                            @changeDialogShow="changeHeaderManagerShow">

    </dialog-edit-with-table>

    <dialog-edit-with-table :show-symbol="globalSettings.showVerifyFields"
                            title="校验字段管理"
                            :exist-data="verifyFieldsData"
                            @handleResult="handleVerifyFieldsData"
                            @changeDialogShow="changeVerifyFieldsShow">

    </dialog-edit-with-table>

    <result-dialog :text-content="resultTextarea"
                   :from-dialog-visible="dialogVisible"
                   @changeDialogVisible="changeDialogVisible">
    </result-dialog>
  </div>
</template>

<script>
import TitleText from "@/views/editor/common/TitleText";
import PrepareEditItem from "@/views/editor/prepareedit/PrepareEditItem";
import ResultDialog from "@/views/editor/common/result/ResultDialog";
import ContenToolBar from "@/views/editor/common/toolbar/ContenToolBar";
import NarMenu from "@/views/editor/common/narmenu/NarMenu";
import NarMenuItem from "@/views/editor/common/narmenu/NarMenuItem";
import { preReset } from "@/assets/js/utils";
import DialogEditWithTable from "@/views/editor/prepareedit/parts/DialogEditWithTable";

export default {
  name: "PrepareEdit",
  components: {DialogEditWithTable, NarMenuItem, NarMenu, ContenToolBar, TitleText, ResultDialog, PrepareEditItem},
  data() {
    return {
      editableTabsValue: '0',
      itemList: [{title: '步骤 1', name: '0', index: 0}],
      currentItemIndex: 0, // 当前步骤下标
      submitFlag: false, // 确定按钮的标识，用于给子组件传递信号是否点击了确定按钮
      dialogVisible: false, // 展示结果页的标识

      resetState: false, // 清空按钮的标识
      receivedNum:0, //生成结果时，临时记录已接收子组件结果的数量
      resultTextarea: '',
      results: {},

      // 全局变量相关的内容
      globalSettings: {
        showHeaderManager: false,
        showVerifyFields: false,
        showOthers: false,
      }
    }
  },

  computed: {
    headerManagerData: {
      get() {
        return this.$store.state.globalSettings.headerManager
      }
    },
    verifyFieldsData: {
      get() {
        return this.$store.state.globalSettings.verifyFields
      }
    },
    resTextData: {
      get() {
        return this.$store.state.globalSettings.resText
      }
    },
    statusCodeData: {
      get() {
        return this.$store.state.globalSettings.statusCode
      }
    },
    resTimeData: {
      get() {
        return this.$store.state.globalSettings.resTime
      }
    },
    waitTimeData: {
      get() {
        return this.$store.state.globalSettings.waitTime
      }
    }
  },

  methods: {
    changeDialogVisible(val) {
      this.dialogVisible = val
      if (val === false) {
        this.resultTextarea = ''
      }
    },
    addItemList() {
      this.currentItemIndex++
      this.editableTabsValue = this.currentItemIndex+''
      this.itemList.push({
        title: '步骤 '+ (this.currentItemIndex+1),
        index: this.currentItemIndex,
        name: this.currentItemIndex + ''
      })
    },

    reset() {
      let title = "是否清空所有步骤的内容"
      console.log('----');
      preReset(this, () => {
        Object.assign(this.$data, this.$options.data())
        this.resetState = Object.assign(this.resetState, !this.resetState)
      }, title)
    },

    //处理子组件传送的数据
    handleData(args) {
      console.log('handleData');
      console.log(args);

      this.results[args[1]] = args[0]
      this.receivedNum ++
      if (this.receivedNum === this.itemList.length) {
        this.createRes()
        this.resumeState()
      }
    },

    //通知子组件传送数据过来
    notifyComponentTransmit() {
      this.submitFlag = true
      // this.submitFlag = false
    },

    //将各子组件传送过来的数据拼接为类数组格式
    convert2array() {
      let newData = {}
      let arrayData = "["
      Object.keys(this.results).sort().map(key => {
        newData[key] = this.results[key]
      })

      for (let key in newData) {
        if (newData[key]) {
          arrayData += newData[key] + ","
        }
      }

      if (arrayData === "[") {
        arrayData += "]"
      } else {
        arrayData = arrayData.slice(0, -1) + "]"
      }

      this.resultTextarea = arrayData
    },

    //所有子组件的数据传送过来后，触发将数据转换为类数据格式
    createRes() {
      this.convert2array()
      this.changeDialogVisible(true)
    },

    //恢复各信号量
    resumeState() {
      this.receivedNum = 0
      this.submitFlag = false
    },

    addTab(targetName) {
      this.currentItemIndex ++
      let newTabName = this.currentItemIndex + '';
      this.itemList.push({
        title: '步骤 '+this.currentItemIndex + 1,
        name: newTabName,
        index: this.currentItemIndex
      });
      this.editableTabsValue = newTabName;
    },

    handleDropdownCommand(command) {
      if (command === "header") {
        this.globalSettings.showHeaderManager = true
      } else if (command === "verifyFields") {
        this.globalSettings.showVerifyFields = true
      } else if (command === "others") {
        this.globalSettings.showOthers = true
      }

    },

    // globalSettings 方法汇总
    changeHeaderManagerShow(val) {
    this.globalSettings.showHeaderManager = val
  },
    handleHeaderManagerData(data) {
    this.$store.state.globalSettings.headerManager = data
  },
    changeVerifyFieldsShow(val) {
      this.globalSettings.showVerifyFields = val
    },
    handleVerifyFieldsData(data) {
      this.$store.state.globalSettings.verifyFields = data
    },
    changeOthersShow(val) {},
    handleOthersData(val) {},



  }

}
</script>

<style scoped>
  .el-header {
    /*background-color: #eeeeee;*/
    color: #333;
    line-height: 50px;
  }
  .tools-card {
    margin: 0 5px;
  }
  .el-card {
    padding: 8px;
  }
</style>