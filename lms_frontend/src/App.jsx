import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'

import Login from './pages/Login'
import Register from './pages/Register'
import AdminLayout from './layouts/AdminLayout'
import TeacherLayout from './layouts/TeacherLayout'
import StudentLayout from './layouts/StudentLayout'

import AdminDashboard from './pages/admin/Dashboard'
import VerifyUsers from './pages/admin/VerifyUsers'
import ManageBooks from './pages/admin/ManageBooks'
import IssueBook from './pages/admin/IssueBook'
import ReturnBook from './pages/admin/ReturnBook'
import AllReservations from './pages/admin/AllReservations'
import FineManagement from './pages/admin/FineManagement'
import AuditLogs from './pages/admin/AuditLogs'

import TeacherDashboard from './pages/teacher/Dashboard'
import TeacherIssueReturn from './pages/teacher/IssueReturn'
import TeacherViewBooks from './pages/teacher/ViewBooks'
import TeacherReservations from './pages/teacher/Reservations'

import StudentDashboard from './pages/student/Dashboard'
import AvailableBooks from './pages/student/AvailableBooks'
import StudentViewBooks from './pages/student/ViewBooks'
import BorrowedBooks from './pages/student/BorrowedBooks'
import MyFines from './pages/student/MyFines'

function ProtectedRoute({ children, allowedRoles }) {
  const { user, loading } = useAuth()
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-100">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary-500 border-t-transparent" />
      </div>
    )
  }
  if (!user) return <Navigate to="/login" replace />
  if (allowedRoles && !allowedRoles.includes(user.role_id)) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-100">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-red-600">403 Unauthorized</h1>
          <p className="text-slate-600 mt-2">You don't have permission to access this page.</p>
        </div>
      </div>
    )
  }
  return children
}

function RoleRedirect() {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" replace />
  if (user.role_id === 1) return <Navigate to="/admin" replace />
  if (user.role_id === 2) return <Navigate to="/teacher" replace />
  return <Navigate to="/student" replace />
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/" element={<RoleRedirect />} />

      <Route
        path="/admin"
        element={
          <ProtectedRoute allowedRoles={[1]}>
            <AdminLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<AdminDashboard />} />
        <Route path="verify-users" element={<VerifyUsers />} />
        <Route path="books" element={<ManageBooks />} />
        <Route path="issue-book" element={<IssueBook />} />
        <Route path="return-book" element={<ReturnBook />} />
        <Route path="reservations" element={<AllReservations />} />
        <Route path="fines" element={<FineManagement />} />
        <Route path="audit" element={<AuditLogs />} />
      </Route>

      <Route
        path="/teacher"
        element={
          <ProtectedRoute allowedRoles={[2]}>
            <TeacherLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<TeacherDashboard />} />
        <Route path="issue-return" element={<TeacherIssueReturn />} />
        <Route path="books" element={<TeacherViewBooks />} />
        <Route path="reservations" element={<TeacherReservations />} />
      </Route>

      <Route
        path="/student"
        element={
          <ProtectedRoute allowedRoles={[3]}>
            <StudentLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<StudentDashboard />} />
        <Route path="available" element={<AvailableBooks />} />
        <Route path="books" element={<StudentViewBooks />} />
        <Route path="borrowed" element={<BorrowedBooks />} />
        <Route path="fines" element={<MyFines />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
