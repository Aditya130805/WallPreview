<template>
  <main>
    <HomePage />
  </main>
</template>

<script>
import HomePage from './components/HomePage.vue';

export default {
  name: 'App',
  components: {
    HomePage
  }
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
}
main {
  width: auto;
  height: auto;
  margin: 0;
  padding: 0;
}
#app {
  font-family: Avenir, 'Helvetica', sans-serif;
  color: #2c3e50;
  margin: 0;
  padding: 0;
}
</style>