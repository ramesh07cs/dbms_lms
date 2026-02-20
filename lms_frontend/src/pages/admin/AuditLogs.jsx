import { useEffect, useState } from 'react'
import { auditApi } from '../../api/services'
import LoadingSpinner from '../../components/LoadingSpinner'
import toast from 'react-hot-toast'

export default function AuditLogs() {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    auditApi.getAll()
      .then(({ data }) => setLogs(data))
      .catch(() => toast.error('Failed to load'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingSpinner />

  return (
    <>
      <h2 className="text-2xl font-bold text-slate-800 mb-6">Audit Logs</h2>
      <p className="text-slate-600 mb-4">All system activities (user, book, borrow, reservation, fine).</p>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">ID</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">User ID</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Action</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Entity</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Entity ID</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Description</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Date</th>
            </tr>
          </thead>
          <tbody>
            {Array.isArray(logs) && logs.map((l) => (
              <tr key={l.audit_id} className="border-b border-slate-100">
                <td className="px-6 py-4">{l.audit_id}</td>
                <td className="px-6 py-4">{l.user_id ?? '-'}</td>
                <td className="px-6 py-4 font-medium">{l.action}</td>
                <td className="px-6 py-4">{l.entity_type ?? '-'}</td>
                <td className="px-6 py-4">{l.entity_id ?? '-'}</td>
                <td className="px-6 py-4">{l.description || '-'}</td>
                <td className="px-6 py-4">{l.created_at ? new Date(l.created_at).toLocaleString() : '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {(!logs || logs.length === 0) && <p className="p-8 text-slate-500 text-center">No audit logs</p>}
      </div>
    </>
  )
}
