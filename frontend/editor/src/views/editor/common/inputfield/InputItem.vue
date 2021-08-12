<template>
  <el-col class="input-item" :span="span" :offset="offset">
    <el-tooltip
        class="tooltip"
        :effect="tooltipEffect"
        :content="tooltipContent"
        :placement="tooltipPlacement"
        :disabled="tooltipDisable">
      <span class="item-text">{{text}}</span>
    </el-tooltip>

    <el-input class="input-el" placeholder="请输入内容"
              v-model="input_val"
              @input="changeValue"
              clearable>
    </el-input>
  </el-col>
</template>

<script>
export default {
  name: "InputItem",
  props: {
    text: String,
    value: '',
    // tooltip相关的内容
    tooltipEffect: {
      type: String,
      default: "dark"
    },
    tooltipContent: {
      type: String,
      default: ''
    },
    tooltipPlacement: {
      type: String,
      default: "right-start"
    },
    tooltipDisable: {
      type: Boolean,
      default: true
    },
    span: {
      type: Number,
      default: 6
    },
    offset: {
      type: Number,
      default: 0
    },
    parentResetState: false
  },
  data() {
    return {
      inputValData: ''
    }
  },
  methods: {
    changeValue() {
      // console.log("changeValue");
      this.$emit('changeValue', this.input_val)
    },
  },
  computed: {
    input_val: {
      get() {
        return this.inputValData
      },
      set(val) {
        this.inputValData=val
      }
    }
  },
  watch: {
    "$store.state.singleJsonInputCleanState": {
      // deep: true,
      handler: function (newValue, oldValue) {
        console.log('----in watch')
        this.input_val = ''
      }
    },
    "parentResetState": {
      handler: function () {
        this.input_val = ''
      }
    }
  }
}
</script>

<style scoped>
  .input-item {
    /*width: 480px;*/
    display: flex;
    flex: 1;
  }
  .item-text {
    flex-shrink: 0;
    margin: 10px 10px;
    width: 100px;
  }

  /*屏幕小于1440px的宽带*/
  @media screen and (max-width: 1440px) {
    .input-el {
      width: 260px;
    }
  }

  /*屏幕等于1440px的宽度*/
  @media screen and (max-width: 1440px) and (min-width: 1440px){
    .input-el {
      width: 348px;
    }
  }

  /*屏幕大于1440px宽度*/
  @media screen and (min-width: 1441px) {
    .input-el {
      width: 348px;
    }
  }
</style>