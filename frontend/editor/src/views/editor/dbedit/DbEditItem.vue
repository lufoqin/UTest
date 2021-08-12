<template>
  <div>
    <el-form
      ref="form"
      :model="form"
      label-width="1px"
      style="width: 100%">

      <el-row class="form-el-row">
        <el-col :span="2">
          <el-tooltip effect="dark" content="请输入在基础配置中配置的数据库名" placement="top-end">
            <div class="form-item-title">
              <span>数据库db：</span>
            </div>
          </el-tooltip>

        </el-col>

        <el-col :span="2">
          <el-form-item label="" >
            <el-input
                v-model="form.dbName"
                placeholder="数据库名"></el-input>
          </el-form-item>
        </el-col>

        <el-col :span="2">
          <el-tooltip effect="dark" content="验证类型" placement="top-start">
            <div class="form-item-title">
              <span>验证类型</span>
              <el-popover
                  placement="top-start"
                  trigger="click"
                  title="说明："
                  content='"=": 相等; "!=": 不相等;"~": 包含; "!~": 不包含'>
                <i slot="reference" class="el-icon-chat-dot-square"></i>
              </el-popover>

            </div>
          </el-tooltip>

        </el-col>

        <el-col :span="2">
          <el-form-item label="">
            <el-select
                v-model="form.vfTypeValue"
                placeholder="请选择验证类型">
              <el-option
                  v-for="item in form.vfTypeOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>

        <el-col :span="2">
          <div class="form-item-title">
            <span>SQL语句：</span>
          </div>
        </el-col>

        <el-col :span="14">
          <el-form-item label="">
            <el-input v-model="form.sql" placeholder="请输入SQL语句"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="2">
          <div class="form-item-title">
            <span>验证内容：</span>
          </div>
        </el-col>

        <el-col :span="22">
          <el-tabs type="border-card" @tab-click="handleTabClick" v-model="formTabsName">
            <el-tab-pane
                label="验证内容"
                name="vfContent"
                ref="tablePage">
              <table-item
                  :item-height="tableHeight"
                  :is-active="tabActive.vfContent"
                  :is-submit="isPreview"
                  :reset-flag="resetState"
                  @receiveTableData="handleTableData">
              </table-item>
            </el-tab-pane>
          </el-tabs>
        </el-col>
      </el-row>
    </el-form>

    <el-row style="margin-top: 10px">
      <el-col :span="2">
        <el-tooltip effect="dark" content="预览当前的内容" placement="top-end">
          <el-button
              type="primary"
              size="small"
              @click="preview"><i class="el-icon-document"></i> 预览</el-button>
        </el-tooltip>
      </el-col>

      <el-col :span="2">
        <el-tooltip effect="dark" content="清空当前的内容" placement="top-start">
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
  name: "DbEditItem",
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
      formTabsName: 'vfContent',

      tabActive: {
        vfContent: false
      },

      // 表单信息
      form: {

        vfTypeOptions: [{
          value: '=',
          label: '相等'
        }, {
          value: '!=',
          label: '不相等'
        }, {
          value: '~',
          label: '包含'
        }, {
          value: '!~',
          label: '不包含'
        }],
        dbName: '', // 数据库名
        vfTypeValue: '=', // 验证类型
        sql: '', // SQL语句

      },

      isPreview: false,

      resetState: false,

      activeNames: ['1'],

      createCompleteSymbol: false, // 是否生成结果标志位

      results: {
        dbName: '',
        vfType: '',
        sql: '',
        vfContent: '',

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
          console.log('-----------');
          this.notifyTransmit()
        }
      }
    },
    "createCompleteSymbol": {
      handler: function () {
        if (this.createCompleteSymbol && this.submitFlag === true) {
          this.$emit("receiveData", [this.results.result, this.stepIndex])
          console.log('==============');
        } else if (this.createCompleteSymbol === true) {
          console.log('============');
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
        this.tabActive.vfContent =  true
        console.log(this.tableHeight);
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

      this.handleStrFields()

      if (this.form.sql && this.form.dbName) {
        let rest = '{"sql' + (this.stepIndex+1) + '"' + ':' + '{'
        rest += this.results.sql + ','
        rest += this.results.dbName + ','
        rest += this.results.vfType + ','
        if (this.results.vfContent) {
          rest += this.results.vfContent
        } else {
          rest = rest.slice(0, -1)
        }

        rest += '}}'
        console.log(rest);
        this.results.result = rest
      } else {
        this.results.result = ""
      }

      this.createCompleteSymbol = true
      console.log('set this.createCompleteSymbol');

    },

    handleStrFields() {
      this.results.sql = '"sql":' + '"' + this.form.sql + '"'
      this.results.dbName = '"db":' + '"' + this.form.dbName + '"'
      this.results.vfType = '"type":' + '"' + this.form.vfTypeValue + '"'
    },

    handleTableData(data) {
      if (data === "{}") {
        this.results.vfContent = ''
      } else {
        this.results.vfContent = '"check":'+ data
      }

      this.createResult()
      this.resumeSymbol()

    },

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