import { useEffect, useState } from 'react'
import { statsApi } from '../../api/services'
import StatCard from '../../components/StatCard'
import LoadingSpinner from '../../components/LoadingSpinner'

export default function StudentDashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    statsApi.student()
      .then(({ data }) => setStats(data))
      .catch(() => setStats({ borrowed_count: 0, due_soon: [], total_fines: 0, active_reservations: 0 }))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingSpinner />

  return (
    <>
      <h2 className="text-2xl font-bold text-slate-800 mb-6">Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <StatCard title="Currently Borrowed" value={stats?.borrowed_count ?? 0} icon="📚" />
        <StatCard title="Books Due Soon" value={stats?.due_soon?.length ?? 0} icon="📅" />
        <StatCard title="Total Fines" value={`Rs ${stats?.total_fines ?? 0}`} icon="💰" />
        <StatCard title="Active Reservations" value={stats?.active_reservations ?? 0} icon="📋" />
      </div>
      {(stats?.due_soon?.length > 0) && (
        <div>
          <h3 className="font-semibold text-slate-800 mb-2">Books Due Soon</h3>
          <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
            <table className="w-full">
              <thead className="bg-slate-50"><tr><th className="text-left px-6 py-2">Title</th><th className="text-left px-6 py-2">Author</th><th className="text-left px-6 py-2">Due Date</th></tr></thead>
              <tbody>
                {stats.due_soon.map((b) => (
                  <tr key={b.borrow_id}><td className="px-6 py-3">{b.title}</td><td className="px-6 py-3">{b.author}</td><td className="px-6 py-3 text-amber-600">{new Date(b.due_date).toLocaleDateString()}</td></tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </>
  )
}
