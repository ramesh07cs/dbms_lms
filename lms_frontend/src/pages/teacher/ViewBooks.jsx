import { useEffect, useState } from 'react'
import { booksApi, borrowApi, reservationApi } from '../../api/services'
import LoadingSpinner from '../../components/LoadingSpinner'
import toast from 'react-hot-toast'

export default function TeacherViewBooks() {
  const [books, setBooks] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [acting, setActing] = useState(null)

  const load = () => {
    booksApi.getAll().then(({ data }) => setBooks(data)).finally(() => setLoading(false))
  }
  useEffect(() => { load() }, [])

  const handleRequestBorrow = async (bookId) => {
    setActing(bookId)
    try {
      await borrowApi.request(bookId)
      toast.success('Borrow request submitted. Wait for admin approval.')
      load()
    } catch (e) {
      const errorMsg = e.response?.data?.error || e.message || 'Failed to submit borrow request'
      console.error('Borrow request failed:', errorMsg, e)
      toast.error(errorMsg)
    } finally {
      setActing(null)
    }
  }

  const handleReserve = async (bookId) => {
    setActing(bookId)
    try {
      await reservationApi.create(bookId)
      toast.success('Reserved. You will get a borrow request when a copy is available.')
      load()
    } catch (e) {
      toast.error(e.response?.data?.error || 'Failed')
    } finally {
      setActing(null)
    }
  }

  const filtered = books.filter((b) =>
    [b.title, b.author, b.isbn, b.category].some((v) => (v || '').toLowerCase().includes(search.toLowerCase()))
  )

  if (loading) return <LoadingSpinner />

  return (
    <>
      <h2 className="text-2xl font-bold text-slate-800 mb-6">View Books</h2>
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
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">ISBN</th>
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
                <td className="px-6 py-4">{b.isbn}</td>
                <td className="px-6 py-4">{b.available_copies}</td>
                <td className="px-6 py-4">
                  {Number(b.available_copies) >= 1 ? (
                    <button onClick={() => handleRequestBorrow(b.book_id)} disabled={acting !== null} className="px-3 py-1 bg-primary-600 text-white rounded text-sm disabled:opacity-50">Request Borrow</button>
                  ) : (
                    <button onClick={() => handleReserve(b.book_id)} disabled={acting !== null} className="px-3 py-1 bg-amber-600 text-white rounded text-sm disabled:opacity-50">Reserve</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  )
}
