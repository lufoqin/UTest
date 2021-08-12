<template>
  <div>
    <tool-bar>
      <tool-bar-item :span='2'>
        <template>
          <slot name="text"></slot>
        </template>
      </tool-bar-item>
      <tool-bar-item :span='2'>
        <template>
          <slot name="addClick"></slot>
        </template>
      </tool-bar-item>

      <tool-bar-item :span='2' :offset="15">
        <template>
          <slot name="okClick"></slot>
        </template>
      </tool-bar-item>
      <tool-bar-item :span='2' :offset="1">
        <template>
          <slot name="clearClick"></slot>
        </template>
      </tool-bar-item>
    </tool-bar>
  </div>
</template>

<script>
import ToolBar from "@/views/editor/common/toolbar/ToolBar";
import ToolBarItem from "@/views/editor/common/toolbar/ToolBarItem";
export default {
  name: "ContenToolBar",
  components: {ToolBar, ToolBarItem}
}
</script>

<style scoped>

</style>