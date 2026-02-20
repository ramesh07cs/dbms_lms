import { useEffect, useState } from 'react'
import { usersApi } from '../../api/services'
import LoadingSpinner from '../../components/LoadingSpinner'

export default function TeacherViewUsers() {
    const [users, setUsers] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        usersApi.list()
            .then(({ data }) => setUsers(data || []))
            .catch(() => setUsers([]))
            .finally(() => setLoading(false))
    }, [])

    if (loading) return <LoadingSpinner />

    return (
        <>
            <h2 className="text-2xl font-bold text-slate-800 mb-6">View Users</h2>
            <p className="text-slate-600 mb-4">Teachers and students in the system (read-only).</p>
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                <table className="w-full">
                    <thead className="bg-slate-50 border-b border-slate-200">
                        <tr>
                            <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Name</th>
                            <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Email</th>
                            <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Role</th>
                            <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.map((u) => (
                            <tr key={u.user_id} className="border-b border-slate-100">
                                <td className="px-6 py-4">{u.name}</td>
                                <td className="px-6 py-4">{u.email}</td>
                                <td className="px-6 py-4">{u.role_name}</td>
                                <td className="px-6 py-4">{u.status}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {users.length === 0 && <p className="p-8 text-slate-500 text-center">No users</p>}
            </div>
        </>
    )
}
