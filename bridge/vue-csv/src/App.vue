<template>
  <div id="app">
    <CsvUploader />
  </div>
</template>




<script>
import CsvUploader from './components/CsvUploader.vue';

export default {
  name: 'App',
  components: {
    CsvUploader
  }
}

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
