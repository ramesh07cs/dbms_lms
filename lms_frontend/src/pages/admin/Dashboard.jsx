import { useEffect, useState } from 'react'
import { useAuth } from '../../context/AuthContext'
import { statsApi, borrowApi } from '../../api/services'
import StatCard from '../../components/StatCard'
import LoadingSpinner from '../../components/LoadingSpinner'
import toast from 'react-hot-toast'

export default function AdminDashboard() {
  const { user } = useAuth()
  const [stats, setStats] = useState(null)
  const [pending, setPending] = useState([])
  const [loading, setLoading] = useState(true)
  const [acting, setActing] = useState(null)

  const loadStats = () => {
    statsApi.admin()
      .then(({ data }) => setStats(data))
      .catch(() => setStats({
        total_issued_books: 0,
        total_available_books: 0,
        total_students: 0,
        total_teachers: 0,
        total_fine_collected: 0,
      }))
  }

  const loadPending = () => {
    borrowApi.adminPending()
      .then(({ data }) => setPending(data))
      .catch(() => setPending([]))
  }

  useEffect(() => {
    Promise.all([statsApi.admin().then(({ data }) => setStats(data)).catch(() => setStats({ total_issued_books: 0, total_available_books: 0, total_students: 0, total_teachers: 0, total_fine_collected: 0 })), borrowApi.adminPending().then(({ data }) => setPending(data)).catch(() => setPending([]))])
      .finally(() => setLoading(false))
  }, [])

  const handleApprove = async (borrowId) => {
    setActing(borrowId)
    try {
      await borrowApi.adminApprove(borrowId)
      toast.success('Borrow approved')
      loadPending()
      loadStats()
    } catch (e) {
      toast.error(e.response?.data?.error || 'Failed')
    } finally {
      setActing(null)
    }
  }

  const handleReject = async (borrowId) => {
    setActing(borrowId)
    try {
      await borrowApi.adminReject(borrowId)
      toast.success('Borrow rejected')
      loadPending()
    } catch (e) {
      toast.error(e.response?.data?.error || 'Failed')
    } finally {
      setActing(null)
    }
  }

  if (loading) return <LoadingSpinner />

  return (
    <>
      <h2 className="text-2xl font-bold text-slate-800 mb-6">Welcome back, {user?.name || 'Admin'}! Here&apos;s what&apos;s happening with your library account.</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
        <StatCard title="Total Issued Books" value={stats?.total_issued_books ?? 0} icon="📤" />
        <StatCard title="Total Available Books" value={stats?.total_available_books ?? 0} icon="📚" />
        <StatCard title="Total Students" value={stats?.total_students ?? 0} icon="👨‍🎓" />
        <StatCard title="Total Teachers" value={stats?.total_teachers ?? 0} icon="👨‍🏫" />
        <StatCard title="Total Fine Collected" value={`Rs ${stats?.total_fine_collected ?? 0}`} icon="💰" />
      </div>

      <h3 className="text-lg font-semibold text-slate-700 mb-3">Pending Borrow Requests</h3>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">User</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Book</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Role</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Actions</th>
            </tr>
          </thead>
          <tbody>
            {pending.length === 0 && (
              <tr><td colSpan={4} className="px-6 py-4 text-slate-500 text-center">No pending requests</td></tr>
            )}
            {pending.map((b) => (
              <tr key={b.borrow_id} className="border-b border-slate-100">
                <td className="px-6 py-4">{b.user_name} ({b.email})</td>
                <td className="px-6 py-4">{b.title} – {b.author}</td>
                <td className="px-6 py-4">{b.role_name}</td>
                <td className="px-6 py-4 flex gap-2">
                  <button onClick={() => handleApprove(b.borrow_id)} disabled={acting !== null} className="px-3 py-1 bg-green-600 text-white rounded text-sm disabled:opacity-50">Approve</button>
                  <button onClick={() => handleReject(b.borrow_id)} disabled={acting !== null} className="px-3 py-1 bg-red-600 text-white rounded text-sm disabled:opacity-50">Reject</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  )
}
