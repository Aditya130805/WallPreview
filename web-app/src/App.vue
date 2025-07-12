<template>
  <main>
    <router-view :isInRatio="isInRatio"></router-view>
  </main>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      isInRatio: true
    }
  },
  methods: {
    switch_version () {
      const width = window.innerWidth;
      if (width > 1500) {
        console.log("In!")
        this.isInRatio = true;
      }
      else {
        this.isInRatio = false;
      }
    }
  },
  created() {
    this.switch_version()
    window.addEventListener('resize', this.switch_version);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.switch_version);
  }
};
</script>

<style>
* {
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