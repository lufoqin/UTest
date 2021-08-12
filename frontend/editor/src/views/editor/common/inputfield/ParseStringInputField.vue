<template>
  <div>
    <el-input
      class="str-input"
      type="textarea"
      placeholder="请输入待解析的字符串"
      v-model="textarea"
      :rows="4"
      :autosize="textareaAutoSize"
      :clearable="clearable"
      @input="creator">
    </el-input>
  </div>

</template>

<script>
import TitleText from "@/views/editor/common/TitleText";

export default {
  name: "ParseStringInputField",
  components: {
    TitleText
  },
  data() {
    return {
      textarea: '',
      clearable: true,
      textareaAutoSize: {"minRows": 5, "maxRows": 50}
    }
  },
  props:{
    parentResetState: false
  },
  methods: {
    creator() {
      console.log('input change');
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
      this.$emit("stringRes", result)
    }
  },
  watch: {
    "parentResetState": {
      handler: function () {
        this.textarea = ''
      }
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