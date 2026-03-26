<template>
  <q-page class="q-pa-md bg-grey-3">
    <div class="row justify-center">
      <q-card class="col-12 col-md-8 shadow-2 q-pa-md">
        <q-card-section>
          <div class="text-h5 text-weight-bold">
            <q-icon name="smart_toy" class="q-mr-sm" color="primary" />
            Configuração do Prompt de Triagem (IA)
          </div>
          <div class="text-subtitle1 text-grey-8 q-mt-sm">
            Defina as regras de ouro para o modelo preditivo que roda no n8n.
          </div>
        </q-card-section>

        <q-separator inset />

        <q-card-section>
          <q-input
            v-model="store.promptIA"
            filled
            type="textarea"
            label="Prompt do Sistema"
            bottom-slots
            counter
            autogrow
            input-style="min-height: 200px; font-family: monospace;"
          >
            <template v-slot:hint>
              Lembre-se: O backend instrui o fluxo do n8n a formatar a resposta estruturada na Chave `prioridade` e `resumo`.
            </template>
          </q-input>
          
          <div class="row justify-end q-mt-md">
            <q-btn color="primary" icon="save" label="Salvar Prompt" @click="savePrompt" :loading="saving" />
          </div>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useTriageStore } from '../../stores/triage'

const store = useTriageStore()
const saving = ref(false)

onMounted(async () => {
  await store.fetchPrompt()
})

const savePrompt = async () => {
  saving.value = true;
  try {
    await store.updatePrompt(store.promptIA)
    alert("Prompt salvo com sucesso!")
  } catch (error) {
    console.error("Erro ao salvar o prompt", error)
    alert("Erro ao salvar prompt. Verifique o servidor Backend.")
  } finally {
    saving.value = false;
  }
}
</script>
