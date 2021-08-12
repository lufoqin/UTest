<template>
  <div id="app">
    <editor></editor>

  </div>
</template>

<script>
  import editor from "./views/editor/Editor";

  export default {
    name: 'App',
    components: {
      editor
    }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /*text-align: center;*/
  color: #2c3e50;
  /*margin-top: 10px;*/
}
</style>
