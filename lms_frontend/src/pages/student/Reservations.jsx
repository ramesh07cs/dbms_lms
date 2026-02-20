import { useEffect, useState } from 'react'
import { booksApi, reservationApi } from '../../api/services'
import LoadingSpinner from '../../components/LoadingSpinner'
import toast from 'react-hot-toast'

export default function Reservations() {
  const [books, setBooks] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')

  const load = () => {
    booksApi.getUnavailable().then(({ data }) => setBooks(data)).finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const reserve = async (bookId) => {
    try {
      await reservationApi.create(bookId)
      toast.success('Reserved')
      load()
    } catch (e) {
      toast.error(e.response?.data?.error || 'Failed')
    }
  }

  const filtered = books.filter((b) =>
    [b.title, b.author, b.isbn, b.category].some((v) => (v || '').toLowerCase().includes(search.toLowerCase()))
  )

  if (loading) return <LoadingSpinner />

  return (
    <>
      <h2 className="text-2xl font-bold text-slate-800 mb-6">Reservations</h2>
      <p className="text-slate-600 mb-4">Books with no available copies. Reserve to join the waiting queue.</p>
      <input
        type="text"
        placeholder="Search..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="mb-4 max-w-xs px-4 py-2 border border-slate-300 rounded-lg"
      />
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Title</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Author</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Category</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Available</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Action</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((b) => (
              <tr key={b.book_id} className="border-b border-slate-100">
                <td className="px-6 py-4">{b.title}</td>
                <td className="px-6 py-4">{b.author}</td>
                <td className="px-6 py-4">{b.category || '-'}</td>
                <td className="px-6 py-4">{b.available_copies}</td>
                <td className="px-6 py-4">
                  <button onClick={() => reserve(b.book_id)} className="px-3 py-1 bg-amber-600 text-white rounded text-sm">Reserve</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 && <p className="p-8 text-slate-500 text-center">No unavailable books to reserve</p>}
      </div>
    </>
  )
}
