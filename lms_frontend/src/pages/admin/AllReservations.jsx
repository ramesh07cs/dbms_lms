import { useEffect, useState } from 'react'
import { reservationApi } from '../../api/services'
import LoadingSpinner from '../../components/LoadingSpinner'
import toast from 'react-hot-toast'

export default function AllReservations() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    reservationApi.all()
      .then(({ data }) => setItems(data))
      .catch(() => toast.error('Failed to load'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingSpinner />

  return (
    <>
      <h2 className="text-2xl font-bold text-slate-800 mb-6">All Reservations</h2>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">User</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Book</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Date</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Expiry</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Status</th>
            </tr>
          </thead>
          <tbody>
            {items.map((r) => (
              <tr key={r.reservation_id} className="border-b border-slate-100">
                <td className="px-6 py-4">{r.user_name} ({r.email})</td>
                <td className="px-6 py-4">{r.book_title}</td>
                <td className="px-6 py-4">{new Date(r.reservation_date).toLocaleString()}</td>
                <td className="px-6 py-4">{r.expiry_date ? new Date(r.expiry_date).toLocaleString() : '-'}</td>
                <td className="px-6 py-4">
                  <span className={r.reservation_status === 'ACTIVE' ? 'bg-green-100 text-green-800 px-2 py-0.5 rounded text-xs' : 'bg-slate-100 px-2 py-0.5 rounded text-xs'}>
                    {r.reservation_status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {items.length === 0 && <p className="p-8 text-slate-500 text-center">No reservations</p>}
      </div>
    </>
  )
}
