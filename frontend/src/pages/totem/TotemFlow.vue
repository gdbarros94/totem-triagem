<template>
  <q-page class="column items-center justify-center q-pa-md" style="width: 100%; max-width: 1000px;">
    
    <!-- Step 1: Início -->
    <div v-if="step === 1" class="text-center full-width">
      <div class="text-h2 q-mb-xl text-weight-bolder" ref="librasWelcome">
        👋 Bem-vindo ao Autoatendimento
      </div>
      <div class="text-h5 q-mb-xl text-grey-8" ref="librasInstruction">
        Toque no botão abaixo para iniciar
      </div>
      <q-btn class="full-width" color="primary" size="3xl" label="COMEÇAR" @click="step = 2" rounded icon-right="arrow_forward" />
    </div>

    <!-- Step 2: Nome -->
    <div v-if="step === 2" class="text-center full-width">
      <div class="text-h3 q-mb-lg text-weight-bold" ref="librasNameTitle">Como você se chama?</div>
      <q-input v-model="form.nome_paciente" filled class="q-mb-md text-h4" input-class="text-h4 text-center" 
               placeholder="Toque aqui para digitar..." readonly />
      <VirtualKeyboard @keypress="onKeypressName" class="q-mb-xl" />
      <div class="row justify-between">
        <q-btn color="grey-6" size="xl" label="Voltar" @click="step = 1" rounded icon="arrow_back" />
        <q-btn color="primary" size="xl" label="Avançar" @click="startSymptoms" rounded icon-right="arrow_forward" :disable="!form.nome_paciente" />
      </div>
    </div>

    <!-- Step 3: Sintomas & Dor -->
    <div v-if="step === 3" class="text-center full-width">
      <div class="text-h3 q-mb-md text-weight-bold" ref="librasSymptomsTitle">Como você está se sentindo?</div>
      <q-input v-model="form.sintomas" filled type="textarea" class="q-mb-md text-h5" input-class="text-h5" 
               placeholder="Descreva o que está sentindo (pode usar o teclado)" />
      <!-- Small Keyboard for Symptoms -->
      <VirtualKeyboard @keypress="onKeypressSymptoms" class="q-mb-lg" />
      
      <div class="text-h4 q-mb-md text-weight-bold" ref="librasPainTitle">Nível de Dor <span class="text-primary">{{form.nivel_dor}}</span></div>
      <div class="row items-center justify-center q-mb-xl">
        <span class="text-h4 q-mr-md">😊 0</span>
        <q-slider v-model="form.nivel_dor" :min="0" :max="10" :step="1" color="negative" class="col-8" left-label track-size="10px" thumb-size="30px" />
        <span class="text-h4 q-ml-md">😭 10</span>
      </div>

      <div class="row justify-between">
        <q-btn color="grey-6" size="xl" label="Voltar" @click="step = 2" rounded icon="arrow_back" />
        <q-btn color="positive" size="xl" label="Finalizar" @click="submitTriage" rounded icon="check" :disable="!form.sintomas" />
      </div>
    </div>

    <!-- Step 4: Loading -->
    <div v-if="step === 4" class="text-center full-width">
      <q-spinner-hourglass color="primary" size="8em" />
      <div class="text-h4 q-mt-md text-weight-bold" ref="librasLoadingTitle">Aguarde, a Inteligência Artificial está classificando sua prioridade...</div>
    </div>

    <!-- Step 5: Resultado -->
    <div v-if="step === 5" class="text-center full-width">
      <q-card class="bg-white q-pa-xl shadow-up-4 rounded-borders">
        <div class="text-h3 q-mb-md text-weight-bold text-dark" ref="librasResultTitle">Seu atendimento foi registrado!</div>
        
        <div class="text-h5 q-mb-sm text-grey-8">Sua senha é:</div>
        <div class="text-h1 q-mb-lg text-weight-bolder" :class="colorMapText[result.prioridade]">
          {{ result.senha }}
        </div>
        
        <div class="row justify-center q-mb-xl">
          <q-banner rounded :class="colorMapBg[result.prioridade]" class="text-white text-h5 q-py-md q-px-xl text-center" style="max-width: 600px">
            Cor de Classificação: {{ result.prioridade }}
          </q-banner>
        </div>
        
        <div class="text-h5 q-mb-md text-grey-8" ref="librasWaitInstruction">Por favor, aguarde ser chamado no painel.</div>
        <q-btn color="primary" size="xl" label="Novo Atendimento" @click="resetFlow" rounded icon="refresh" class="q-mt-lg" />
      </q-card>
    </div>

  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useTriageStore } from '../../stores/triage'
import VirtualKeyboard from '../../components/VirtualKeyboard.vue'
import { applyLibrasLongPress } from '../../plugins/vlibras'

const store = useTriageStore()

const step = ref(1)
const form = ref({
  nome_paciente: '',
  sintomas: '',
  nivel_dor: 0
})
const result = ref(null)

// Element refs for VLibras detection setup
const librasWelcome = ref(null)
const librasInstruction = ref(null)
const librasNameTitle = ref(null)
const librasSymptomsTitle = ref(null)
const librasPainTitle = ref(null)
const librasLoadingTitle = ref(null)
const librasResultTitle = ref(null)
const librasWaitInstruction = ref(null)

onMounted(() => {
  store.resetLibras()
  
  // Attach VLibras long-press detection
  const markUsed = () => store.setLibrasUsed();
  
  // We use setTimeout to let elements render before attaching listeners
  setTimeout(() => {
    applyLibrasLongPress(librasWelcome.value, markUsed)
    applyLibrasLongPress(librasInstruction.value, markUsed)
    applyLibrasLongPress(librasNameTitle.value, markUsed)
    applyLibrasLongPress(librasSymptomsTitle.value, markUsed)
    applyLibrasLongPress(librasPainTitle.value, markUsed)
    applyLibrasLongPress(librasLoadingTitle.value, markUsed)
    applyLibrasLongPress(librasResultTitle.value, markUsed)
    applyLibrasLongPress(librasWaitInstruction.value, markUsed)
  }, 1000)
})

const onKeypressName = (key) => {
  if (key === 'BACK') {
    form.value.nome_paciente = form.value.nome_paciente.slice(0, -1)
  } else if (key === 'SPACE') {
    form.value.nome_paciente += ' '
  } else {
    form.value.nome_paciente += key
  }
}

const onKeypressSymptoms = (key) => {
  if (key === 'BACK') {
    form.value.sintomas = form.value.sintomas.slice(0, -1)
  } else if (key === 'SPACE') {
    form.value.sintomas += ' '
  } else {
    form.value.sintomas += key
  }
}

const startSymptoms = () => {
  step.value = 3;
}

const submitTriage = async () => {
  step.value = 4;
  try {
    const payload = {
      ...form.value,
      usou_libras: store.usouLibras
    }
    const data = await store.createAtendimento(payload)
    result.value = data;
    step.value = 5;
  } catch (error) {
    console.error("Erro ao criar atendimento:", error)
    step.value = 3;
    alert("Ocorreu um erro ao processar sua requisição. Verifique o servidor Backend e o N8N Workflow.");
  }
}

const resetFlow = () => {
  form.value = { nome_paciente: '', sintomas: '', nivel_dor: 0 }
  result.value = null;
  store.resetLibras();
  step.value = 1;
}

const colorMapBg = {
  'Vermelho': 'bg-negative',
  'Amarelo': 'bg-warning',
  'Verde': 'bg-positive',
  'Azul': 'bg-info'
}

const colorMapText = {
  'Vermelho': 'text-negative',
  'Amarelo': 'text-warning',
  'Verde': 'text-positive',
  'Azul': 'text-info'
}
</script>
