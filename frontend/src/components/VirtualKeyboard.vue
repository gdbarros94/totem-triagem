<template>
  <div class="virtual-keyboard q-pa-md bg-grey-3 rounded-borders shadow-2" style="max-width: 800px; width: 100%; margin: 0 auto;">
    <div v-for="(row, rIndex) in layout" :key="rIndex" class="row justify-center q-gutter-sm q-mb-sm">
      <q-btn v-for="key in row" :key="key" 
             :label="key === 'SPACE' ? '' : (key === 'BACK' ? '' : key)" 
             :icon="key === 'BACK' ? 'backspace' : (key === 'SPACE' ? 'space_bar' : '')"
             :class="key === 'SPACE' ? 'col-6' : (key === 'BACK' ? 'col-2' : 'col-1')"
             color="white" text-color="dark" size="xl" unelevated
             @click="handleKeyPress(key)" />
    </div>
  </div>
</template>
<script setup>
const emit = defineEmits(['keypress']);
const layout = [
  ['Q','W','E','R','T','Y','U','I','O','P'],
  ['A','S','D','F','G','H','J','K','L'],
  ['Z','X','C','V','B','N','M', 'BACK'],
  ['SPACE']
]
const handleKeyPress = (key) => {
  emit('keypress', key);
};
</script>
