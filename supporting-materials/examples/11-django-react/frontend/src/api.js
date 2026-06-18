import axios from 'axios'

const base = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export const api = axios.create({
  baseURL: `${base}/api`,
})

export const listTodos = () => api.get('/todos/')
export const createTodo = (payload) => api.post('/todos/', payload)
export const toggleTodo = (id) => api.post(`/todos/${id}/toggle/`)
export const deleteTodo = (id) => api.delete(`/todos/${id}/`)
