<template>
  <div id="editor">
    <el-container ref="layoutPage">
      <el-header style="background: #0086b3">
        <el-row>
          <el-col :span="4">
            <div style="margin-top: 14px">
              <span
                  style="color: #eee;
                  font-size: 20px;
                  margin-top: 8px;
                  font-weight: bolder"><i class="el-icon-menu"></i> 用例编辑</span>
            </div>
          </el-col>
        </el-row>
      </el-header>

      <el-container ref="layoutMain">
        <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
          <el-menu :defalut-active="$route.path" router>

            <el-menu-item index="/prepare">
              <div>
                <i class="el-icon-s-platform"></i>
                <span class="item-menu">
                  用例编辑
                </span>
              </div>

            </el-menu-item>

            <el-menu-item index="/db">
              <div>
                <i class="el-icon-s-data"></i>
                <span class="item-menu">
                  数据库验证
                </span>
              </div>
            </el-menu-item>

            <el-menu-item index="/dyparam">
              <div>
                <i class="el-icon-s-promotion"></i>
                <span class="item-menu">
                  动态参数
                </span>
              </div>
            </el-menu-item>

          </el-menu>

        </el-aside>

        <el-main style="padding: 3px 0">
          <keep-alive>
            <router-view></router-view>
          </keep-alive>

        </el-main>

      </el-container>

    </el-container>

  </div>
</template>

<script>
import NarMenu from "@/views/editor/common/narmenu/NarMenu";
import NarMenuItem from "@/views/editor/common/narmenu/NarMenuItem";
import TabBar from "@/components/tabbar/TabBar";
import TabBarItem from "@/components/tabbar/TabBarItem";
import Input from "@/views/editor/common/inputfield/Input";
import TitleText from "@/views/editor/common/TitleText";
import BaseEdit from "@/views/editor/baseedit/BaseEdit";
import PrepareEdit from "@/views/editor/prepareedit/PrepareEdit";
import DyParamEdit from "@/views/editor/dyparamedit/DyParamEdit";

export default {
  name: "Editor",
  components: {
    NarMenu,
    NarMenuItem,
    PrepareEdit,
    TabBar,
    TabBarItem,
    TitleText,
    Input,
    BaseEdit
  },
  data() {
    return {
      clientHeight: '',
      activeName: 'first',
      base: '/base'
    }
  },
  mounted() {
    // 获取浏览器可视区域高度
    this.clientHeight = document.documentElement.clientHeight
    // console.log(this.clientHeight);
    //document.body.clientWidth;
    //console.log(self.clientHeight);
    window.onresize = function temp() {
      this.clientHeight = document.documentElement.clientHeight;
    };
  },

  methods: {
    handleClick(tab, event) {
        console.log(tab, event);
      },
    changeItem(event, index) {
      // console.log(index);
      this.$router.push(index)
    },
    changeFixed(clientHeight){ //动态修改样式
      // console.log(clientHeight);
      // console.log(this.$refs.homePage.$el.style.height);

      this.$refs.layoutPage.$el.style.height = clientHeight+'px';
      this.$refs.layoutMain.$el.style.height = clientHeight-60+'px'
      // console.log(this.$refs.layoutPage.$elment.style);
    },
  },

  watch: {
    // 如果 `clientHeight` 发生改变，这个函数就会运行
    clientHeight: function () {
      // console.log('watch');
      // console.log(this.clientHeight);
      this.changeFixed(this.clientHeight)
    }
  }
}
</script>

<style scoped>
  .capital {
    font-size: 22px;
  }
  .el-container {
    padding: 0;
    margin: 0;
    width: 100%;
  }
  .item-menu {
    font-weight: bolder;
    font-size: 15px;
    font-family: "Microsoft YaHei UI";
    margin-top: 3px;
  }

</style>