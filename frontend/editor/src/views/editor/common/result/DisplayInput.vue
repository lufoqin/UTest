<template>
  <div>
    <el-input class="textarea" type="textarea" placeholder="placeholder" v-model="textarea" :autosize="autosize">

    </el-input>
  </div>
</template>

<script>
export default {
  name: "DisplayInput",
  props: {
    content: '',
    parentResetState: false
  },
  data() {
    return {
      autosize: {"minRows": 1, "maxRows": 6}
    }
  },
  computed: {
    textarea: {
      get() {
        return this.content
      },
      set(val) {
        this.$emit("resetTextarea", val)
      }
    }
  },
  watch: {
    "parentResetState": {
      handler: function () {
        this.textarea = ''
      }
    },
    "content": {
      handler: function () {
        this.textarea = this.content
      }
    }
  }
}
</script>

<style scoped>
  /*屏幕小于1440px的宽带*/
  @media screen and (max-width: 1440px) {
    .textarea {
      width: 700px;
    }
  }

  /*屏幕等于1440px的宽度*/
  @media screen and (max-width: 1440px) and (min-width: 1440px){
    .textarea {
      width: 700px;
    }
  }

  /*屏幕大于1440px宽度*/
  @media screen and (min-width: 1441px) {
    .textarea {
      width: 900px;
    }
  }
</style>