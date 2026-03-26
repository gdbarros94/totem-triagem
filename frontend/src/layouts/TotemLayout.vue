<template>
  <q-layout view="hHh lpR fFf" class="bg-grey-2">
    <q-header elevated class="bg-primary text-white custom-header">
      <q-toolbar class="q-py-md">
        <q-toolbar-title class="text-h3 text-weight-bold" style="text-align: center">
          🏥 Triagem Inteligente
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container class="flex flex-center" style="height: 100%;">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
</script>

<style scoped>
.custom-header {
  border-bottom: 5px solid #0d47a1;
}
</style>
