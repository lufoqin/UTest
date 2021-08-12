<template>
  <div>
    <el-row ref="tableEdit">
      <el-col :span="2">
        <el-tooltip effect="dark" content="新增一行" placement="top-end">
          <el-button
            type="primary"
            size="small"
            plain
            @click="addRow">
            <i class="el-icon-plus"></i> 新增
          </el-button>
        </el-tooltip>

      </el-col>

      <el-col :span="2">
        <el-tooltip effect="dark" content="预览当前参数的内容" placement="top-end">
          <el-button
            type="primary"
            size="small"
            plain
            @click="preview">
            <i class="el-icon-document"></i> 预览
          </el-button>
        </el-tooltip>

      </el-col>

      <el-col :span="4">
        <el-tooltip effect="dark" content="转换文本内容" placement="top-end">
          <el-button
            type="primary"
            size="small"
            plain
            @click="switchShow">
           <i class="el-icon-edit"></i> {{editModel}}
          </el-button>
        </el-tooltip>

      </el-col>

      <el-col :span="5">
        <el-tooltip effect="dark" content="是否和文本编辑器的内容拼接" placement="top-end">
          <el-switch v-model="isExtend" active-text="拼接" inactive-text="不拼接" style="margin-top: 3px">
          </el-switch>
        </el-tooltip>

      </el-col>
    </el-row>

    <el-row>
      <el-col :span="24" >
        <div ref="tablePage">
          <el-table
              v-if="showComponent === 1"
              :data="tableData"
              style="width: 100%"
              :height="tableHeight+'px'">
            <el-table-column label="参数名" min-width="120px">
              <editable-cell slot-scope="{row}"
                             :can-edit="editModeEnabled"
                             v-model="row.name">
                <el-input
                    slot="content"
                    v-model="row.name"
                    placeholder="请输入参数名">
                </el-input>
              </editable-cell>
            </el-table-column>

            <el-table-column label="参数值" min-width="120px">
              <editable-cell slot-scope="{row}"
                             :can-edit="editModeEnabled"
                             v-model="row.value">
                <el-input
                    slot="content"
                    v-model="row.value"
                    placeholder="请输入参数值">
                </el-input>
              </editable-cell>
            </el-table-column>

            <el-table-column label="操作" min-width="120px" align="center">
              <template slot-scope="scope">
                <el-button size="mini" type="danger" @click="deleteRow(scope.$index, scope.row)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <el-row v-if="showComponent === 2">
            <el-row class="textarea-row">
              <el-col :span="24" style="padding: 15px 0" class="textarea-col">
                <el-input
                    type="textarea"
                    v-model="textarea"
                    :rows="textareaRows"
                    :style="{minHeight: textareaMinHeight+'px'}">

                </el-input>
              </el-col>
            </el-row>

          </el-row>
        </div>
      </el-col>
    </el-row>

    <result-dialog :text-content="result.result"
                   :from-dialog-visible="result.dialogVisible"
                   @changeDialogVisible="changeDialogVisible">
    </result-dialog>
  </div>

</template>

<script>
import EditableCell from "@/views/editor/common/table/EditableCell";
import { table2jsonStr, str2jsonFormat, arrayCopy } from "@/assets/js/utils";
import ResultDialog from "@/views/editor/common/result/ResultDialog";

export default {
  name: "TableItem",
  components: {ResultDialog, EditableCell},
  props: {
    itemHeight: 0,
    isActive: false,
    isSubmit: false,
    cancelClose: false,
    resetFlag: false,
    initData: '',
    clearAfterSubmit: false
  },

  data() {
    let self = this
    return {
      editModeEnabled:  true,
      tableHeight: 0,
      showComponent: 1, //要显示的内容，1：表格，2：文本编辑器
      switchedTextarea: false,
      isExtend: true, //文本框的内容是否在表格的基础上拼接
      textarea: '', // 文本编辑器的内容
      textareaRows: 5, // 文本编辑器默认行数
      textareaMinHeight: 0, // 文本编辑器默认最低行高度
      editModel: '文本编辑模式', // 文本编辑器按钮显示的文字
      result: {
        result: '',
        dialogVisible: false
      },
      defaultValue: [{
       name: "",
       value: ""
      }, {
       name: "",
       value: ""
      }, {
       name: "",
       value: ""
      }],
    }
  },

  computed: {
    tableData: {
      get() {
        let data = []
        if (this.initData) { // 如果父组件传递了初始化数据，则将初始化数据展示在table上
          let obj = JSON.parse(this.initData)
          for (let key in obj) {
            data.push({name: key, value: obj[key]})
          }
        }
        // 在初始化数据的基础上，增加3行空白行
        data = data.concat(this.defaultValue)
        return data
      },
      set(val) {
        this.defaultValue = val
      },
    }
  },

  methods: {
    addRow() {
      this.tableData.push({name: "", value: ""})
    },

    deleteRow(index, row) {
      this.tableData.splice(index, 1)
    },
    resetHeight() {
      return new Promise((resolve, reject) => {
        this.tableHeight = 0
        resolve()
      })
    },
    // 设置table高度
    setTableHeight() {
      this.resetHeight().then(res => {
        let tableEditBtnClientHeight = this.$refs.tableEdit.$el.clientHeight
        this.tableHeight = this.itemHeight - tableEditBtnClientHeight
        // console.log('tableHeight');
        // console.log(this.tableHeight);
      })
    },

    setTextareaHeight() {
      let tableEditBtnClientHeight = this.$refs.tableEdit.$el.clientHeight
      console.log('tableEditBtnClientHeight');
      console.log(tableEditBtnClientHeight);

      this.textareaMinHeight = this.itemHeight - tableEditBtnClientHeight - 30
      console.log(this.textareaMinHeight);
      this.textareaRows = this.tableHeight / 30
    },

    createResult() {
      return new Promise((resolve, reject) => {
        let tableText = table2jsonStr(this.tableData)
        let textareaContent = str2jsonFormat(this.textarea) // 文本编辑器的转换后的内容
        if (this.isExtend) { // 判断是否打开了拼接开关
          // 拼接开关打开了，将两边的内容拼接一起
          if (tableText && textareaContent) { //如果两边的内容都不为空，则进行内容拼接
            this.result.result = tableText.slice(0, -1) + "," + textareaContent.slice(1, -1) + "}"
          } else if (!tableText && !textareaContent){ //如果都为空，默认返回"{}"
            this.result.result = "{}"
          } else if (tableText){ // 表格的内容不为空，返回表格的内容
            this.result.result = tableText || "{}"
          } else {
            this.result.result = textareaContent || "{}"
          }
        } else { //如果没有打开拼接开关，则只显示正在编辑页的内容
          if (this.showComponent === 1) { //显示键值对编辑器的内容
            this.result.result = tableText || "{}"
          } else { // 显示文本编辑器的内容
            this.result.result = textareaContent || "{}"
          }

        }

        resolve()
      })

    },

    preview() {
      this.createResult().then(res => {
        this.result.dialogVisible = true
      })
    },

    changeDialogVisible(val) {
      this.result.dialogVisible = val
      if (val === false) {
        this.result.result = ''
      }
    },

    switchShow() {
      if (this.showComponent === 1) {
        new Promise(resolve => {
          this.showComponent = 2
          this.editModel = '键值对编辑模式'
          resolve()
        }).then(res => {
          if (!this.switchedTextarea) {
          this.switchedTextarea = true
          this.setTextareaHeight()
        }
        })

      } else {
        this.showComponent = 1
        this.editModel = '文本编辑模式'
      }
    },

    genDefaultValue() {
      let data = []
      for (let i=0; i<3; i++) {
        data.push({name: "", value: ""})
      }
      return data
    }

  },

  watch: {
    "isActive": {
      handler: function() {
        this.setTableHeight()
      }
    },

    "isSubmit": {
      handler: function () {
        if (this.isSubmit === true) {
          this.createResult().then(res => {
            this.$emit("receiveTableData", this.result.result)
            if (this.clearAfterSubmit) {
              this.defaultValue = this.genDefaultValue()
            }
          })
        }
      }
    },
    "resetFlag": {
      handler: function () {
        this.tableData = this.genDefaultValue()
        this.textarea = ''
      }
    },
    "cancelClose": {
      handler: function () {
        if (this.clearAfterSubmit) {
          this.defaultValue = this.genDefaultValue()
        }
      }
    }
  }

}
</script>

<style scoped>

</style>