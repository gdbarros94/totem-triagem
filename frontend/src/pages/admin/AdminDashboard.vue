<template>
  <q-page class="q-pa-md bg-grey-3">
    <div class="text-h4 q-mb-md text-weight-bold">Fila de Espera</div>
    
    <q-table
      :rows="store.atendimentos"
      :columns="columns"
      row-key="id"
      class="bg-white shadow-2"
      flat bordered
      :pagination="initialPagination"
    >
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="status" :props="props">
            <q-badge :color="statusColorMap[props.row.status]" rounded class="q-pa-sm text-weight-bold">
              {{ props.row.status.toUpperCase() }}
            </q-badge>
          </q-td>

          <q-td key="senha" :props="props">
            <div class="text-h6 text-weight-bold">{{ props.row.senha }}</div>
          </q-td>

          <q-td key="nome_paciente" :props="props">
            {{ props.row.nome_paciente }}
            <!-- ACCESSIBILITY ALERT -->
            <q-badge v-if="props.row.usou_libras" color="deep-purple" floating transparent>
              <q-icon name="sign_language" size="xs" class="q-mr-xs" />
              LIBRAS
            </q-badge>
          </q-td>

          <q-td key="prioridade" :props="props">
            <q-chip :color="priorityColorMap[props.row.prioridade]" text-color="white" icon="flag">
              {{ props.row.prioridade }}
            </q-chip>
          </q-td>

          <q-td key="sintomas" :props="props" class="ellipsis text-caption" style="max-width: 250px">
            {{ props.row.sintomas }}
          </q-td>
          
          <q-td key="nivel_dor" :props="props">
            {{ props.row.nivel_dor }} / 10
          </q-td>

          <q-td key="actions" :props="props">
            <q-btn v-if="props.row.status === 'aguardando'" color="primary" icon="campaign" label="Chamar" size="sm" dense @click="changeStatus(props.row.id, 'em_atendimento')" />
            <q-btn v-else-if="props.row.status === 'em_atendimento'" color="positive" icon="done" label="Finalizar" size="sm" dense class="q-ml-sm" @click="changeStatus(props.row.id, 'finalizado')" />
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </q-page>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useTriageStore } from '../../stores/triage'

const store = useTriageStore()

const initialPagination = {
  sortBy: 'senha',
  descending: false,
  page: 1,
  rowsPerPage: 20
}

const columns = [
  { name: 'status', label: 'Status', align: 'left', field: 'status', sortable: true },
  { name: 'senha', label: 'Senha', align: 'left', field: 'senha', sortable: true },
  { name: 'nome_paciente', label: 'Paciente', align: 'left', field: 'nome_paciente', sortable: true },
  { name: 'prioridade', label: 'Classificação (IA)', align: 'center', field: 'prioridade', sortable: true },
  { name: 'sintomas', label: 'Resumo / Sintomas', align: 'left', field: 'sintomas' },
  { name: 'nivel_dor', label: 'Dor', align: 'center', field: 'nivel_dor', sortable: true },
  { name: 'actions', label: 'Ações', align: 'right' }
]

const priorityColorMap = {
  'Vermelho': 'negative',
  'Amarelo': 'warning',
  'Verde': 'positive',
  'Azul': 'info'
}

const statusColorMap = {
  'aguardando': 'grey-6',
  'em_atendimento': 'primary',
  'finalizado': 'positive'
}

let pollInterval

onMounted(() => {
  store.fetchAtendimentos()
  pollInterval = setInterval(() => {
    store.fetchAtendimentos()
  }, 5000)
})

onUnmounted(() => {
  clearInterval(pollInterval)
})

const changeStatus = async (id, status) => {
  try {
    await store.updateStatus(id, status)
  } catch (error) {
    console.error("Erro ao alterar status", error)
    alert("Falha ao atualizar status do paciente.")
  }
}
</script>
