import api from './axios'

export const authApi = {
  login: (email, password) => api.post('/users/login', { email, password }),
  register: (data) => api.post('/users/register', data),
  logout: () => api.post('/users/logout'),
  profile: () => api.get('/users/profile'),
}

export const booksApi = {
  getAll: () => api.get('/books/'),
  getOne: (id) => api.get(`/books/${id}`),
  create: (data) => api.post('/books/', data),
  update: (id, data) => api.put(`/books/${id}`, data),
  delete: (id) => api.delete(`/books/${id}`),
}

export const borrowApi = {
  request: (bookId) => {
    const payload = { book_id: Number(bookId) }
    console.log('[Borrow Request] Payload:', payload)
    console.log('[Borrow Request] Endpoint: POST /borrow/request')
    console.log('[Borrow Request] Token:', window.__LMS_TOKEN__ ? 'Present' : 'Missing')
    return api.post('/borrow/request', payload)
      .then((response) => {
        console.log('[Borrow Request] Success:', response.data)
        return response
      })
      .catch((error) => {
        console.error('[Borrow Request] Error:', error)
        console.error('[Borrow Request] Response:', error.response?.data)
        console.error('[Borrow Request] Status:', error.response?.status)
        throw error
      })
  },
  return: (bookId) => api.post('/borrow/return', { book_id: bookId }),
  myActive: () => api.get('/borrow/my/active'),
  myHistory: (page = 1) => api.get('/borrow/my/history', { params: { page } }),
  adminPending: () => api.get('/borrow/admin/pending'),
  adminAll: () => api.get('/borrow/admin/all'),
  adminApprove: (borrowId) => api.post(`/borrow/admin/approve/${borrowId}`),
  adminReject: (borrowId) => api.post(`/borrow/admin/reject/${borrowId}`),
  adminUsers: () => api.get('/borrow/admin/users'),
  adminActive: () => api.get('/borrow/admin/active'),
  adminIssue: (userId, bookId) => api.post('/borrow/admin/issue', { user_id: userId, book_id: bookId }),
  adminReturn: (borrowId) => api.post('/borrow/admin/return', { borrow_id: borrowId }),
  teacherStudents: () => api.get('/borrow/teacher/students'),
  teacherIssue: (userId, bookId) => api.post('/borrow/teacher/issue', { user_id: userId, book_id: bookId }),
}

export const reservationApi = {
  create: (bookId) => api.post('/reservation/create', { book_id: bookId }),
  cancel: (id) => api.delete(`/reservation/cancel/${id}`),
  my: () => api.get('/reservation/my'),
  all: (page = 1) => api.get('/reservation/all', { params: { page } }),
}

export const fineApi = {
  my: (page = 1) => api.get('/fine/my', { params: { page } }),
  all: (page = 1) => api.get('/fine/all', { params: { page } }),
  pay: (fineId) => api.post(`/fine/pay/${fineId}`),
}

export const auditApi = {
  getAll: (page = 1, limit = 20) => api.get('/admin/audit/', { params: { page, limit } }),
}

export const usersApi = {
  pending: () => api.get('/users/pending'),
  all: () => api.get('/users/all'),
  list: () => api.get('/users/list'),
  approve: (userId) => api.post(`/users/approve/${userId}`),
  reject: (userId) => api.post(`/users/reject/${userId}`),
  setStatus: (userId, status) => api.put(`/users/${userId}/status`, { status }),
  delete: (userId) => api.delete(`/users/${userId}`),
}

export const statsApi = {
  admin: () => api.get('/stats/admin'),
  teacher: () => api.get('/stats/teacher'),
  student: () => api.get('/stats/student'),
}
