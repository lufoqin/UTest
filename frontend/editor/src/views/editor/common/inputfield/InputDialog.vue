<template>
  <div>
    <el-row class="input" type="flex" :gutter="gutter">
      <input-dialog-item text="key" :span="span" @changeValue="changeKeyValue" :parent-reset-state="resetState"></input-dialog-item>
      <input-dialog-item text="value" :span="span" :offset="2" @changeValue="changeValueValue" :parent-reset-state="resetState"></input-dialog-item>
    </el-row>
  </div>
</template>

<script>
import InputItem from "@/views/editor/common/inputfield/InputDialogItem";
import InputDialogItem from "@/views/editor/common/inputfield/InputDialogItem";

export default {
  name: "InputDialog",
  components: {
    InputDialogItem
  },
  props: {
    index: Number,
    span: {
      type: Number,
      default: 6
    },
    parentResetState: false
  },
  data() {
    return {
      gutter: 0,
      inputValue: '',
      kvValue: ['', '', ''],
      resetState: this.parentResetState
    }
  },

  methods: {
    changeKeyValue(value) {
      // console.log(value);
      this.kvValue[0]=value
      this.kvValue[2] = this.index
      this.$emit('inputChange', this.kvValue)
    },
    changeValueValue(value) {
      // console.log(value);
      // console.log('index=',this.index);
      this.kvValue[1]=value
      this.kvValue[2] = this.index
      this.$emit('inputChange', this.kvValue)
    }
  },
  watch: {
    "parentResetState": {
      handler: function () {
        this.resetState = this.parentResetState
      }
    }
  }
}
</script>

<style scoped>
  /*.input {*/
  /*  !*display: flex;*!*/
  /*  margin-top: 4px;*/
  /*  margin-bottom: 4px;*/
  /*  flex: 1;*/
  /*}*/

</style>