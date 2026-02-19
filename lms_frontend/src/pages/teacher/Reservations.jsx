import { useEffect, useState } from 'react'
import { reservationApi } from '../../api/services'
import LoadingSpinner from '../../components/LoadingSpinner'
import toast from 'react-hot-toast'

export default function TeacherReservations() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    reservationApi.my().then(({ data }) => setItems(data)).finally(() => setLoading(false))
  }, [])

  const cancel = async (id) => {
    try {
      await reservationApi.cancel(id)
      toast.success('Cancelled')
      setItems((prev) => prev.filter((r) => r.reservation_id !== id))
    } catch {
      toast.error('Failed')
    }
  }

  if (loading) return <LoadingSpinner />

  const active = items.filter((r) => r.reservation_status === 'ACTIVE')

  return (
    <>
      <h2 className="text-2xl font-bold text-slate-800 mb-6">View Reservations</h2>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Book</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Date</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Expiry</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Status</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Actions</th>
            </tr>
          </thead>
          <tbody>
            {items.map((r) => (
              <tr key={r.reservation_id} className="border-b border-slate-100">
                <td className="px-6 py-4">{r.title}</td>
                <td className="px-6 py-4">{new Date(r.reservation_date).toLocaleString()}</td>
                <td className="px-6 py-4">{r.expiry_date ? new Date(r.expiry_date).toLocaleString() : '-'}</td>
                <td className="px-6 py-4">
                  <span className={r.reservation_status === 'ACTIVE' ? 'text-green-600' : 'text-slate-500'}>{r.reservation_status}</span>
                </td>
                <td className="px-6 py-4">
                  {r.reservation_status === 'ACTIVE' && (
                    <button onClick={() => cancel(r.reservation_id)} className="text-red-600 hover:underline">Cancel</button>
                  )}
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
