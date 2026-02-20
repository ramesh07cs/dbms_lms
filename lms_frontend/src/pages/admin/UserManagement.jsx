import { useEffect, useState } from 'react'
import { useAuth } from '../../context/AuthContext'
import { usersApi } from '../../api/services'
import LoadingSpinner from '../../components/LoadingSpinner'
import toast from 'react-hot-toast'

export default function UserManagement() {
    const { user } = useAuth()
    const [users, setUsers] = useState([])
    const [loading, setLoading] = useState(true)

    const load = () => {
        usersApi.all()
            .then(({ data }) => setUsers(data))
            .catch(() => toast.error('Failed to load users'))
            .finally(() => setLoading(false))
    }

    useEffect(() => { load() }, [])

    const handleStatusChange = async (userId, status) => {
        try {
            await usersApi.setStatus(userId, status)
            toast.success(`Status set to ${status}`)
            load()
        } catch (e) {
            toast.error(e.response?.data?.error || 'Failed')
        }
    }

    const handleDelete = async (userId) => {
        if (!confirm('Remove this user? This may affect related records.')) return
        try {
            await usersApi.delete(userId)
            toast.success('User removed')
            load()
        } catch (e) {
            toast.error(e.response?.data?.error || 'Failed')
        }
    }

    if (loading) return <LoadingSpinner />

    return (
        <>
            <h2 className="text-2xl font-bold text-slate-800 mb-6">User Management</h2>
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                <table className="w-full">
                    <thead className="bg-slate-50 border-b border-slate-200">
                        <tr>
                            <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Name</th>
                            <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Email</th>
                            <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Role</th>
                            <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Status</th>
                            <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.map((u) => (
                            <tr key={u.user_id} className="border-b border-slate-100">
                                <td className="px-6 py-4">{u.name}</td>
                                <td className="px-6 py-4">{u.email}</td>
                                <td className="px-6 py-4">{u.role_name}</td>
                                <td className="px-6 py-4">
                                    <span className={`px-2 py-0.5 rounded text-xs ${u.status === 'APPROVED' ? 'bg-green-100 text-green-800' : u.status === 'PENDING' ? 'bg-amber-100 text-amber-800' : 'bg-red-100 text-red-800'}`}>
                                        {u.status}
                                    </span>
                                </td>
                                <td className="px-6 py-4 flex flex-wrap gap-2 items-center">
                                    <select
                                        value={u.status}
                                        onChange={(e) => handleStatusChange(u.user_id, e.target.value)}
                                        className="text-sm border border-slate-300 rounded px-2 py-1"
                                    >
                                        <option value="APPROVED">APPROVED</option>
                                        <option value="PENDING">PENDING</option>
                                        <option value="REJECTED">REJECTED</option>
                                    </select>
                                    <button onClick={() => handleDelete(u.user_id)} disabled={u.user_id === user?.user_id} className="text-red-600 hover:underline text-sm disabled:opacity-50 disabled:cursor-not-allowed">Delete</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {users.length === 0 && <p className="p-8 text-slate-500 text-center">No users</p>}
            </div>
        </>
    )
}
