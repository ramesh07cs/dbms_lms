import { useEffect, useState } from 'react'
import { useAuth } from '../../context/AuthContext'
import { statsApi } from '../../api/services'
import StatCard from '../../components/StatCard'
import LoadingSpinner from '../../components/LoadingSpinner'

export default function TeacherDashboard() {
  const { user } = useAuth()
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    statsApi.teacher()
      .then(({ data }) => setStats(data))
      .catch(() => setStats({ issued_count: 0, due_today: [], overdue: [] }))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingSpinner />

  return (
    <>
      <h2 className="text-2xl font-bold text-slate-800 mb-6">Welcome back, {user?.name || 'Teacher'}! Here&apos;s what&apos;s happening with your library account.</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <StatCard title="Issued Books" value={stats?.issued_count ?? 0} icon="📚" />
        <StatCard title="Due Today" value={stats?.due_today?.length ?? 0} icon="📅" />
        <StatCard title="Overdue" value={stats?.overdue?.length ?? 0} icon="⚠️" />
      </div>
      {(stats?.overdue?.length > 0) && (
        <div>
          <h3 className="font-semibold text-slate-800 mb-2">Overdue Books</h3>
          <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
            <table className="w-full">
              <thead className="bg-slate-50"><tr><th className="text-left px-6 py-2">Title</th><th className="text-left px-6 py-2">Author</th><th className="text-left px-6 py-2">Due Date</th></tr></thead>
              <tbody>
                {stats.overdue.map((b) => (
                  <tr key={b.borrow_id}><td className="px-6 py-3">{b.title}</td><td className="px-6 py-3">{b.author}</td><td className="px-6 py-3 text-red-600">{new Date(b.due_date).toLocaleDateString()}</td></tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </>
  )
}
