import { useEffect, useState } from 'react'
import { usersApi } from '../../api/services'
import LoadingSpinner from '../../components/LoadingSpinner'
import toast from 'react-hot-toast'

export default function VerifyUsers() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)

  const load = () => {
    usersApi.pending()
      .then(({ data }) => setUsers(data))
      .catch(() => toast.error('Failed to load'))
      .finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const approve = async (userId) => {
    try {
      await usersApi.approve(userId)
      toast.success('User approved')
      load()
    } catch {
      toast.error('Failed to approve')
    }
  }

  const reject = async (userId) => {
    try {
      await usersApi.reject(userId)
      toast.success('User rejected')
      load()
    } catch {
      toast.error('Failed to reject')
    }
  }

  if (loading) return <LoadingSpinner />

  return (
    <>
      <h2 className="text-2xl font-bold text-slate-800 mb-6">Verify Users</h2>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        {users.length === 0 ? (
          <p className="p-8 text-slate-500 text-center">No pending registrations</p>
        ) : (
          <table className="w-full">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Name</th>
                <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Email</th>
                <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Phone</th>
                <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Role</th>
                <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.user_id} className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="px-6 py-4">{u.name}</td>
                  <td className="px-6 py-4">{u.email}</td>
                  <td className="px-6 py-4">{u.phone || '-'}</td>
                  <td className="px-6 py-4">{u.role_name || (u.role_id === 2 ? 'Teacher' : 'Student')}</td>
                  <td className="px-6 py-4 flex gap-2">
                    <button onClick={() => approve(u.user_id)} className="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700">Approve</button>
                    <button onClick={() => reject(u.user_id)} className="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700">Reject</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </>
  )
}
