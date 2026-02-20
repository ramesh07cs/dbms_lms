import api from './axios'

export const authApi = {
  login: (email, password) => api.post('/users/login', { email, password }),
  register: (data) => api.post('/users/register', data),
  logout: () => api.post('/users/logout'),
  profile: () => api.get('/users/profile'),
}

export const booksApi = {
  getAll: () => api.get('/books/'),
  getUnavailable: () => api.get('/books/unavailable'),
  getOne: (id) => api.get(`/books/${id}`),
  create: (data) => api.post('/books/', data),
  update: (id, data) => api.put(`/books/${id}`, data),
  delete: (id) => api.delete(`/books/${id}`),
}

export const borrowApi = {
  issue: (bookId) => api.post('/borrow/issue', { book_id: bookId }),
  return: (bookId) => api.post('/borrow/return', { book_id: bookId }),
  myActive: () => api.get('/borrow/my/active'),
  myHistory: (page = 1) => api.get('/borrow/my/history', { params: { page } }),
  adminUsers: () => api.get('/borrow/admin/users'),
  adminActive: () => api.get('/borrow/admin/active'),
  adminIssue: (userId, bookId) => api.post('/borrow/admin/issue', { user_id: userId, book_id: bookId }),
  adminReturn: (borrowId) => api.post('/borrow/admin/return', { borrow_id: borrowId }),
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
  getAll: (page = 1, limit = 20) => api.get('/audit/all', { params: { page, limit } }),
  myLogs: (page = 1, limit = 20) => api.get('/audit/my-logs', { params: { page, limit } }),
}

export const usersApi = {
  pending: () => api.get('/users/pending'),
  approve: (userId) => api.post(`/users/approve/${userId}`),
  reject: (userId) => api.post(`/users/reject/${userId}`),
}

export const statsApi = {
  admin: () => api.get('/stats/admin'),
  teacher: () => api.get('/stats/teacher'),
  student: () => api.get('/stats/student'),
}
