import { useEffect, useState } from 'react'
import { fineApi } from '../../api/services'
import LoadingSpinner from '../../components/LoadingSpinner'

export default function TeacherMyFines() {
    const [fines, setFines] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fineApi.my()
            .then(({ data }) => setFines(Array.isArray(data) ? data : []))
            .catch(() => setFines([]))
            .finally(() => setLoading(false))
    }, [])

    if (loading) return <LoadingSpinner />

    return (
        <>
            <h2 className="text-2xl font-bold text-slate-800 mb-6">My Fines</h2>
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                <table className="w-full">
                    <thead className="bg-slate-50 border-b border-slate-200">
                        <tr>
                            <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Book Title</th>
                            <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Amount</th>
                            <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Paid</th>
                            <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {fines.map((f) => (
                            <tr key={f.fine_id} className="border-b border-slate-100">
                                <td className="px-6 py-4">{f.book_title || '-'}</td>
                                <td className="px-6 py-4">Rs {f.amount ?? 0}</td>
                                <td className="px-6 py-4">{f.paid_status ? 'Yes' : 'No'}</td>
                                <td className="px-6 py-4">{f.created_at ? new Date(f.created_at).toLocaleDateString() : '-'}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {fines.length === 0 && <p className="p-8 text-slate-500 text-center">No fines</p>}
            </div>
        </>
    )
}
