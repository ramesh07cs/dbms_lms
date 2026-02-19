import { useEffect, useState } from 'react'
import { statsApi } from '../../api/services'
import StatCard from '../../components/StatCard'
import LoadingSpinner from '../../components/LoadingSpinner'

export default function AdminDashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    statsApi.admin()
      .then(({ data }) => setStats(data))
      .catch(() => setStats({
        total_issued_books: 0,
        total_available_books: 0,
        total_students: 0,
        total_teachers: 0,
        total_fine_collected: 0,
      }))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingSpinner />

  return (
    <>
      <h2 className="text-2xl font-bold text-slate-800 mb-6">Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <StatCard title="Total Issued Books" value={stats?.total_issued_books ?? 0} icon="📤" />
        <StatCard title="Total Available Books" value={stats?.total_available_books ?? 0} icon="📚" />
        <StatCard title="Total Students" value={stats?.total_students ?? 0} icon="👨‍🎓" />
        <StatCard title="Total Teachers" value={stats?.total_teachers ?? 0} icon="👨‍🏫" />
        <StatCard title="Total Fine Collected" value={`Rs ${stats?.total_fine_collected ?? 0}`} icon="💰" />
      </div>
    </>
  )
}
