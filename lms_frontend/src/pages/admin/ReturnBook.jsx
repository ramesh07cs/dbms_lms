import { useEffect, useState } from 'react'
import { borrowApi } from '../../api/services'
import toast from 'react-hot-toast'

export default function ReturnBook() {
  const [borrows, setBorrows] = useState([])
  const [borrowId, setBorrowId] = useState('')
  const [loading, setLoading] = useState(false)

  const load = () => {
    borrowApi.adminActive().then(({ data }) => setBorrows(data)).catch(() => {})
  }

  useEffect(() => { load() }, [])

  const submit = async (e) => {
    e.preventDefault()
    if (!borrowId) {
      toast.error('Select a borrow')
      return
    }
    setLoading(true)
    try {
      const { data } = await borrowApi.adminReturn(parseInt(borrowId))
      toast.success(data.fine_amount > 0 ? `Returned. Fine: Rs ${data.fine_amount}` : 'Book returned')
      setBorrowId('')
      load()
    } catch (e) {
      toast.error(e.response?.data?.error || 'Failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <h2 className="text-2xl font-bold text-slate-800 mb-6">Return Book</h2>
      <form onSubmit={submit} className="max-w-md space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Select Active Borrow</label>
          <select value={borrowId} onChange={(e) => setBorrowId(e.target.value)} className="w-full px-4 py-2 border rounded-lg" required>
            <option value="">-- Select borrow --</option>
            {borrows.map((b) => (
              <option key={b.borrow_id} value={b.borrow_id}>
                {b.user_name} - {b.title} (due: {new Date(b.due_date).toLocaleDateString()})
              </option>
            ))}
          </select>
        </div>
        <button type="submit" disabled={loading} className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50">Return</button>
      </form>
    </>
  )
}
