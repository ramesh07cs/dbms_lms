import { useEffect, useState } from 'react'
import { fineApi } from '../../api/services'
import LoadingSpinner from '../../components/LoadingSpinner'
import toast from 'react-hot-toast'

export default function FineManagement() {
  const [fines, setFines] = useState([])
  const [loading, setLoading] = useState(true)

  const load = () => {
    fineApi.all()
      .then(({ data }) => setFines(data))
      .catch(() => toast.error('Failed to load'))
      .finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const pay = async (fineId) => {
    try {
      await fineApi.pay(fineId)
      toast.success('Marked as paid')
      load()
    } catch {
      toast.error('Failed')
    }
  }

  if (loading) return <LoadingSpinner />

  return (
    <>
      <h2 className="text-2xl font-bold text-slate-800 mb-6">Fine Management</h2>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">ID</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">User ID</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Amount</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Status</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Actions</th>
            </tr>
          </thead>
          <tbody>
            {fines.map((f) => (
              <tr key={f.fine_id} className="border-b border-slate-100">
                <td className="px-6 py-4">{f.fine_id}</td>
                <td className="px-6 py-4">{f.user_id}</td>
                <td className="px-6 py-4">Rs {f.amount}</td>
                <td className="px-6 py-4">
                  <span className={f.paid_status ? 'text-green-600' : 'text-amber-600'}>
                    {f.paid_status ? 'Paid' : 'Unpaid'}
                  </span>
                </td>
                <td className="px-6 py-4">
                  {!f.paid_status && (
                    <button onClick={() => pay(f.fine_id)} className="px-3 py-1 bg-green-600 text-white rounded text-sm">Mark Paid</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {fines.length === 0 && <p className="p-8 text-slate-500 text-center">No fines</p>}
      </div>
    </>
  )
}
