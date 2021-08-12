<template>
  <div>
    <el-form
      ref="form"
      :model="form"
      label-width="1px"
      style="width: 100%">

      <el-row class="form-el-row">
        <el-col :span="2">
          <div class="form-item-title">
            <span>请求地址：</span>
          </div>
        </el-col>

        <el-col :span="6">
          <el-form-item label="">
            <el-select
                v-model="form.methodValue"
                placeholder="请选择请求方法">
              <el-option
                  v-for="item in form.methodsOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>

        <el-col :span="16">
          <el-form-item label="" >
            <el-input
                v-model="form.url"
                placeholder="请输入去除hostname后的api地址或者完整api地址"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row class="form-el-row">
        <el-col :span="2">
          <div class="form-item-title">
            <span>接口描述：</span>
          </div>
        </el-col>

        <el-col :span="22">
          <el-form-item label="">
            <el-input v-model="form.desc"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row class="form-el-row">
        <el-col :span="2">
          <div class="form-item-title">
            <span>等待时间：</span>
          </div>
        </el-col>

        <el-col :span="3">
          <el-form-item label="">
            <el-input
                v-model="form.waitTime"
                placeholder="接口等待时间"></el-input>
          </el-form-item>
        </el-col>

        <el-col :span="2">
          <div class="form-item-title">
            <span>状态码：</span>
          </div>
        </el-col>

        <el-col :span="3">
          <el-form-item label="">
            <el-input v-model="form.resStatus"></el-input>
          </el-form-item>
        </el-col>

        <el-col :span="2">
          <div class="form-item-title">
            <span>响应时间：</span>
          </div>
        </el-col>

        <el-col :span="3">
          <el-form-item label="">
            <el-input v-model="form.resTime"></el-input>
          </el-form-item>
        </el-col>

        <el-col :span="2">
          <div class="form-item-title">
            <span>响应字段：</span>
          </div>
        </el-col>

        <el-col :span="7">
          <el-form-item label="">
            <el-input v-model="form.resText"></el-input>
          </el-form-item>
        </el-col>

      </el-row>

      <el-row class="form-el-row">
        <el-col :span="2">
          <div class="form-item-title">
            <span>py表达式：</span>
          </div>
        </el-col>

        <el-col :span="22">
          <el-form-item label="">
            <el-input v-model="form.py"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="2">
          <div class="form-item-title">
            <span>其他信息：</span>
          </div>
        </el-col>

        <el-col :span="22">
          <el-tabs type="border-card" @tab-click="handleTabClick" v-model="formTabsName">
            <el-tab-pane
                label="请求参数"
                name="reqParam"
                ref="tablePage">
              <table-item
                  :item-height="tableHeight"
                  :is-active="tabActive.reqParam"
                  :is-submit="isPreview"
                  :reset-flag="resetState"
                  @receiveTableData="handleTableData($event, 'reqParam')"
                  >
              </table-item>
            </el-tab-pane>

            <el-tab-pane label="请求头" name="reqHeader">
              <table-item
                  :item-height="tableHeight"
                  :is-active="tabActive.reqHeader"
                  :is-submit="isPreview"
                  :reset-flag="resetState"
                  @receiveTableData="handleTableData($event, 'reqHeader')">
              </table-item>
            </el-tab-pane>

            <el-tab-pane label="用例变量" name="caseVar">
              <table-item
                  :item-height="tableHeight"
                  :is-active="tabActive.caseVar"
                  :is-submit="isPreview"
                  :reset-flag="resetState"
                  @receiveTableData="handleTableData($event, 'caseVar')">
              </table-item>
            </el-tab-pane>

            <el-tab-pane label="接口变量" name="IfVar">
              <table-item
                  :item-height="tableHeight"
                  :is-active="tabActive.IfVar"
                  :is-submit="isPreview"
                  :reset-flag="resetState"
                  @receiveTableData="handleTableData($event, 'IfVar')">
              </table-item>
            </el-tab-pane>
            <el-tab-pane label="校验字段" name="vf">
              <table-item
                  :item-height="tableHeight"
                  :is-active="tabActive.vf"
                  :is-submit="isPreview"
                  :reset-flag="resetState"
                  @receiveTableData="handleTableData($event, 'vf')">
              </table-item>
            </el-tab-pane>
            <el-tab-pane label="响应头校验" name="resHeader">
              <table-item
                  :item-height="tableHeight"
                  :is-active="tabActive.resHeader"
                  :is-submit="isPreview"
                  :reset-flag="resetState"
                  @receiveTableData="handleTableData($event, 'resHeader')">
              </table-item>
            </el-tab-pane>
            <el-tab-pane label="数据库验证" name="db">
              <table-item
                  :item-height="tableHeight"
                  :is-active="tabActive.db"
                  :is-submit="isPreview"
                  :reset-flag="resetState"
                  @receiveTableData="handleTableData($event, 'db')">
              </table-item>
            </el-tab-pane>
            <el-tab-pane label="动态参数" name="dyParam">
              <table-item
                  :item-height="tableHeight"
                  :is-active="tabActive.dyParam"
                  :is-submit="isPreview"
                  :reset-flag="resetState"
                  @receiveTableData="handleTableData($event, 'dyParam')">
              </table-item>
            </el-tab-pane>
          </el-tabs>
        </el-col>
      </el-row>
    </el-form>

    <el-row style="margin-top: 10px">
      <el-col :span="2">
        <el-tooltip effect="dark" content="预览当前步骤的内容" placement="top-end">
          <el-button
              type="primary"
              size="small"
              @click="preview"><i class="el-icon-document"></i> 预览</el-button>
        </el-tooltip>
      </el-col>

      <el-col :span="2">
        <el-tooltip effect="dark" content="清空当前步骤的内容" placement="top-start">
          <el-button
              type="danger"
              size="small"
              @click="reset">
            <i class="el-icon-delete"></i> 清空</el-button>
        </el-tooltip>
      </el-col>
    </el-row>

    <result-dialog :text-content="results.result"
                   :from-dialog-visible="results.dialogVisible"
                   @changeDialogVisible="changeDialogVisible">
    </result-dialog>

  </div>
</template>

<script>
import InputItem from "@/views/editor/common/inputfield/InputItem";
import PartNameText from "@/views/editor/prepareedit/parts/PartNameText";
import ContenToolBar from "@/views/editor/common/toolbar/ContenToolBar";
import ElRowCustom from "@/views/editor/common/elrowcustom/ElRowCustom";
import JsonEditByDialog from "@/views/editor/common/jsoneditor/JsonEditByDialog";
import ElColCustom from "@/views/editor/common/elrowcustom/ElColCustom";
import SubJsonItem from "@/views/editor/prepareedit/parts/SubJsonItem";
import DisplayInput from "@/views/editor/common/result/DisplayInput";
import OpenPlate from "@/views/editor/common/expansion/OpenPlate";
import ClosePlate from "@/views/editor/common/expansion/ClosePlate";
import EditableCell from "@/views/editor/common/table/EditableCell";
import TableItem from "@/views/editor/common/table/TableItem";
import ResultDialog from "@/views/editor/common/result/ResultDialog";
import {preReset, table2jsonStr} from "@/assets/js/utils";

export default {
  name: "PrepareEditItem",
  components: {
    ResultDialog,
    TableItem,
    EditableCell,
    ClosePlate,
    OpenPlate,
    SubJsonItem,
    DisplayInput, ElColCustom, JsonEditByDialog, ElRowCustom, PartNameText, InputItem, ContenToolBar},

  data() {
    return {
      tableHeight: 0,
      windowHeight: 0,
      formTabsName: 'reqParam',

      tabActive: {
        reqParam: false,
        reqHeader: false,
        caseVar: false,
        IfVar: false,
        vf: false,
        resHeader: false,
        db: false,
        dyParam: false,
      },

      // 表单信息
      form: {
        methodValue: 'POST',
        methodsOptions: [{
          value: 'POST',
          label: 'POST'
        }, {
          value: 'GET',
          label: 'GET'
        }, {
          value: 'PUT',
          label: 'PUT'
        }, {
          value: 'DELETE',
          label: 'DELETE'
        },  {
          value: 'PATCH',
          label: 'PATCH'
        }],
        url: '',
        desc: '',
        waitTime: '',
        resText: '',
        resStatus: '200',
        resTime: '2',
        py: ''
      },

      isPreview: false,

      resetState: false,

      activeNames: ['1'],

      createCompleteSymbol: false, // 是否生成结果标志位

      results: {
        desc: '',
        url: '',
        method: '',
        header: '',
        param: '',
        caseVar: '',
        ifVar: '',
        resTime: '',
        vf: '',
        resText: '',
        resHeader: '',
        statusCode: '',
        dbVf: '',
        pyExp: '',
        waitTime: '',
        dyParam: '',
        result: '',
        dialogVisible: false, // 用于控制预览结果展示的显示
        receiveCount: 0, // 已发送table数据的子组件个数，用于判断是否所有的请求参数都已将数据传送完成

      },
    }
  },

  props: {
    stepIndex: '',
    text: '',
    parentResetState: false,
    submitFlag: false
  },
  watch: {
    "parentResetState": {
      handler: function () {
        this.handleReset()
      }
    },
    "submitFlag": {
      handler: function () {
        if (this.submitFlag === true) {
          // console.log('-----------');
          this.notifyTransmit()
        }
      }
    },
    "createCompleteSymbol": {
      handler: function () {
        if (this.createCompleteSymbol && this.submitFlag === true) {
          this.$emit("receiveData", [this.results.result, this.stepIndex])
        } else if (this.createCompleteSymbol === true) {
          this.results.dialogVisible = true
        }
        this.createCompleteSymbol = false
      }
    }
  },

  mounted() {
    this.windowHeight = document.documentElement.clientHeight
    // console.log(this.windowHeight);
    this.fetTableHeight();
  },

  methods: {
    resetHeight() {
      return new Promise((resolve, reject) => {
        this.tableH = 0
        resolve()
      })
    },
    // 设置table高度
    fetTableHeight() {
      this.resetHeight().then(res => {
        let heightObj = this.$refs.tablePage.$el.getBoundingClientRect()
        let tableTop = heightObj.top
        this.tableHeight = this.windowHeight - tableTop - 100
        this.tabActive.reqParam =  true
        // console.log(this.tableHeight);
        return document.documentElement.clientHeight - tableTop - 100
      })
    },

    getClientHeight() {
       document.documentElement.clientHeight
    },
    handleTabClick (tab, event) {
      // console.log(tab.name);
      // console.log(event);
      this.tabActive[tab.name] = true
    },

    handleChange(val) {
      console.log(val);
    },

    //预览
    preview() {
      this.notifyTransmit()
    },

    //通知table传送数值，并生成类json格式字符串
    notifyTransmit() {
      // 对isPreview进行取反，子组件监听该值的变化，发生变化后，会将各自的table数据通过触发handleTableData函数进行处理
      // handleTableData函数统计已发送的表格子组件个数，当满足条件后，会再触发convert2json函数，生成结果，存储到this.results.result中
      // convert2json函数处理完数据后，会设置this.createCompleteSymbol=true，监听该变量的函数会再将结果发送出去
      this.isPreview = true

    },

    // 恢复各状态
    resumeSymbol() {
      this.results.receiveCount = 0
      this.isPreview = false
    },

    changeDialogVisible(val) {
      this.results.dialogVisible = val
      if (val === false) {
        this.results.result = ''
      }
    },

    //重置当前步骤
    reset() {
      let tips = "是否清空当前步骤的内容"
      preReset(this, () => {
        this.handleReset()
      },tips)
    },

    handleReset() {
      let tableH = this.tableHeight
      let windowH = this.windowHeight
      Object.assign(this.$data, this.$options.data.call(this))
      this.tableHeight = tableH
      this.windowHeight = windowH
      this.fetTableHeight()
      this.resetState = Object.assign(this.resetState, !this.resetState)
    },

    //生成当前步骤的结果
    createResult() {
      let rest = "{"

      this.handleStrFields()

      if (this.form.desc) {
        rest += this.results.desc + ","
      }
      if (this.form.methodValue) {
        rest += this.results.method + ","
      }
      if (this.form.url) {
        rest += this.results.url + ","
      } else {
        this.createCompleteSymbol = true
        this.results.result = ""
        return
      }
      if (this.results.param) {
        rest += this.results.param + ","
      }
      if (this.results.header) {
        rest += this.results.header + ","
      } else if (this.$store.state.globalSettings.headerManager) {
        rest += '"header":' + this.$store.state.globalSettings.headerManager + ","
      }
      if (this.results.caseVar) {
        rest += this.results.caseVar + ","
      }
      if (this.results.ifVar) {
        rest += this.results.ifVar + ","
      }
      if (this.results.vf) {
        rest += this.results.vf + ","
      } else if (this.$store.state.globalSettings.verifyFields) {
        rest += '"verify_fields":' + this.$store.state.globalSettings.verifyFields + ","
      }

      if (this.form.waitTime) {
        rest += this.results.waitTime + ","
      } else if (this.$store.state.globalSettings.waitTime) {
        rest += '"wait_time":' + '"' + this.$store.state.globalSettings.waitTime + '"' + ","
      }
      if (this.form.resStatus) {
        rest += this.results.statusCode + ","
      }
      if (this.form.resTime) {
        rest += this.results.resTime + ","
      }
      if (this.form.resText) {
        rest += this.results.resText + ","
      }
      if (this.form.py) {
        rest += this.results.pyExp + ","
      }
      if (this.results.resHeader) {
        rest += this.results.resHeader + ","
      }
      if (this.results.dbVf) {
        rest += this.results.dbVf + ","
      }
      if (this.results.dyParam) {
        rest += this.results.dyParam + ","
      }
      this.results.result = rest.slice(0, -1) + "}"
      this.createCompleteSymbol = true
      console.log('set this.createCompleteSymbol');

    },

    handleStrFields() {
      this.results.desc = '"description":' + '"' + this.form.desc + '"'
      this.results.url = '"url":' + '"' + this.form.url + '"'
      this.results.method = '"method":' + '"' + this.form.methodValue + '"'
      this.results.waitTime = '"wait_time":' + '"' + this.form.waitTime + '"'
      this.results.statusCode = '"status_code":' + '"' + this.form.resStatus + '"'
      this.results.resText = '"res_text":' + '"' + this.form.resText + '"'
      this.results.resTime = '"res_time":' + '"' + this.form.resTime + '"'
      this.results.pyExp = '"expression":' + '"' + this.form.py + '"'
    },

    handleTableData(data, type) {

      this.results.receiveCount ++
      if (type === "reqParam") {
        this.handleParams(data)
      } else if (type === "reqHeader") {
        this.handleReqHeader(data)
      } else if (type === "caseVar") {
        this.handleCaseVar(data)
      } else if (type === "IfVar") {
        this.handleIfVar(data)
      } else if (type === "vf") {
        this.handleVf(data)
      } else if (type === "resHeader") {
        this.handleResHeader(data)
      } else if (type === "db") {
        this.handleDb(data)
      } else if (type === "dyParam") {
        this.handleDyParam(data)
      }
      console.log(this.results.receiveCount);
      if (this.results.receiveCount === 8) {
        this.createResult()
        this.resumeSymbol()
      }
    },

    //请求参数
    handleParams(arg) {
      let res = arg
      if (res === "{}") {
        this.results.param = ''
      } else {
        this.results.param = '"params":'+ res
      }
    },
    //请求头
    handleReqHeader(arg) {
      let res = arg
      if (res === "{}") {
        this.results.header = ''
      } else {
        this.results.header = '"header":'+ res
      }
    },
    //用例变量
    handleCaseVar(arg) {
      let res = arg
      if (res === "{}") {
        this.results.caseVar = ''
      } else {
        this.results.caseVar = '"case_vars":' + res
      }
    },
    //接口变量
    handleIfVar(arg) {
      let res = arg
      if (res === "{}") {
        this.results.ifVar = ''
      } else {
        this.results.ifVar = '"interface_var":' + res
      }
    },
    //校验字段
    handleVf(arg) {
      let res = arg
      if (res === "{}") {
        this.results.vf = ''
      } else {
        this.results.vf = '"verify_fields":' + res
      }
    },
    //响应头
    handleResHeader(arg) {
      let res = arg
      if (res === "{}") {
        this.results.resHeader = ''
      } else {
        this.results.resHeader = '"res_header":' + res
      }
    },
    //数据库验证
    handleDb(arg) {
      let res = arg
      if (res === "{}") {
        this.results.dbVf = ''
      } else {
        this.results.dbVf = '"db_verify":' + res
      }
    },
    //动态参数
    handleDyParam(arg) {
      let res = arg
      if (res === "{}") {
        this.results.dyParam = ''
      } else {
        this.results.dyParam = '"dyparam":' + res
      }
    }
  }
}
</script>

<style scoped>
  .container {
    height: 350px;
    border: 1px;
    solid-color: #fcf8f8;
  }
  .more-options {
    background: #fafafa;
  }

  .more-lyric-enter,
  .more-lyric-leave-to {
    opacity: 0;
    transform: translateX(10px);
  }
  /*.more-lyric-enter-to,*/
  /*.more-lyric-leave {*/
  /*  opacity: 1;*/
  /*}*/
  .more-lyric-enter-active {
    transition: all .2s ease;
  }
  .more-lyric-leave-active {
    /*transition: all 0.2s cubic-bezier(1.0, 0.5, 0.8, 1.0);*/
  }
  .form-item-title {
    margin-top: 8px;
    text-align: right;
  }
  .form-el-row {
    height: 100%;
  }
</style>