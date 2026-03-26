<template>
  <q-layout view="lHh lpR fFf" class="bg-grey-10 text-white">
    <q-header elevated class="bg-dark text-white border-bottom-primary">
      <q-toolbar class="q-py-sm">
        <q-avatar icon="medical_services" color="primary" text-color="white" size="md" />
        <q-toolbar-title class="text-h5 text-weight-bold q-ml-sm">
          Painel de Enfermagem
        </q-toolbar-title>

        <q-space />

        <q-tabs v-model="tab" shrink stretch class="text-primary bg-dark">
          <q-route-tab to="/admin" exact icon="dashboard" label="Fila de Espera" />
          <q-route-tab to="/admin/prompt" exact icon="smart_toy" label="Ajuste de IA" />
        </q-tabs>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
const tab = ref('')
</script>

<style scoped>
.border-bottom-primary {
  border-bottom: 2px solid var(--q-primary);
}
</style>
