<template>
  <router-view />
</template>

<script setup>
</script>

<style>
/* Reset and accessibility enhancements */
body {
  margin: 0;
  font-family: 'Roboto', '-apple-system', 'Helvetica Neue', sans-serif;
  background-color: #f5f5f5;
  -webkit-font-smoothing: antialiased;
}
/* Optional higher contrast selection */
::selection {
  background: #ffeb3b; 
  color: #000;
}
</style>
