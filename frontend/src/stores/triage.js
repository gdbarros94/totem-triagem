import { defineStore } from 'pinia'
import axios from 'axios'

// We proxy the API route through Nginx in prod, or Vite proxy in dev
const baseURL = import.meta.env.PROD ? '/api' : 'http://localhost:8000/api'

export const api = axios.create({
  baseURL
})

export const useTriageStore = defineStore('triage', {
  state: () => ({
    atendimentos: [],
    usouLibras: false,
    promptIA: ''
  }),
  actions: {
    async fetchAtendimentos() {
      try {
        const res = await api.get('/atendimentos')
        this.atendimentos = res.data
      } catch (e) {
        console.error("Error fetching", e)
      }
    },
    async fetchPrompt() {
      try {
        const res = await api.get('/configuracoes/prompt')
        this.promptIA = res.data.prompt_ia
        return this.promptIA
      } catch (e) {
         console.error(e)
         return ''
      }
    },
    async updatePrompt(prompt_ia) {
      await api.put('/configuracoes/prompt', { prompt_ia })
      this.promptIA = prompt_ia
    },
    async updateStatus(id, status) {
      await api.put(`/atendimentos/${id}`, { status })
      await this.fetchAtendimentos()
    },
    async createAtendimento(payload) {
      const res = await api.post('/atendimentos', payload)
      return res.data
    },
    setLibrasUsed() {
      this.usouLibras = true
    },
    resetLibras() {
      this.usouLibras = false
    }
  }
})
