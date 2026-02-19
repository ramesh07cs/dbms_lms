import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  const token = window.__LMS_TOKEN__
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      window.__LMS_TOKEN__ = null
      window.__LMS_LOGOUT__?.()
      window.location.href = '/login'
    } else if (err.response?.status === 403) {
      window.__LMS_403__?.(err)
    }
    return Promise.reject(err)
  }
)

export default api
