<template>
  <div class="title-text">
    {{text}}
  </div>
</template>

<script>
export default {
  name: "TitleBar",
  props: {
    text: String
  }
}
</script>

<style scoped>
  .title-text {
    display: inline-block;
    font-size: 14px;
    text-align: left;
    width: 120px;
  }
</style>