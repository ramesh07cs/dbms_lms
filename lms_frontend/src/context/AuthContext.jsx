import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import api from '../api/axios'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setTokenState] = useState(null)
  const [loading, setLoading] = useState(true)

  const setToken = useCallback((t) => {
    setTokenState(t)
    window.__LMS_TOKEN__ = t
    if (!t) setUser(null)
  }, [])

  const logout = useCallback(() => {
    if (token) {
      api.post('/users/logout').catch(() => { })
    }
    setToken(null)
    setUser(null)
    window.__LMS_LOGOUT__ = null
  }, [token, setToken])

  useEffect(() => {
    window.__LMS_LOGOUT__ = logout
  }, [logout])

  useEffect(() => {
    const t = window.__LMS_TOKEN__
    if (t) {
      setTokenState(t)
      api.get('/users/profile')
        .then(({ data }) => setUser(data.user))
        .catch(() => setToken(null))
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [setToken])

  const login = async (email, password) => {
    const { data } = await api.post('/users/login', { email, password })
    const accessToken = data.access_token
    setToken(accessToken)
    const { data: profileData } = await api.get('/users/profile')
    if (profileData?.user) setUser(profileData.user)
    else {
      const payload = JSON.parse(atob(accessToken.split('.')[1]))
      const sub = payload.sub || payload.identity || {}
      setUser({ user_id: sub.id, email: sub.email, role_id: sub.role_id, name: '' })
    }
    return data
  }

  const value = {
    user,
    token,
    login,
    logout,
    setToken,
    loading,
    isAdmin: user?.role_id === 1,
    isTeacher: user?.role_id === 2,
    isStudent: user?.role_id === 3,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
