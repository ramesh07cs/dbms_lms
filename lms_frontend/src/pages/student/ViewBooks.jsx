import { useEffect, useState } from 'react'
import { booksApi } from '../../api/services'
import LoadingSpinner from '../../components/LoadingSpinner'

export default function StudentViewBooks() {
  const [books, setBooks] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')

  useEffect(() => {
    booksApi.getAll().then(({ data }) => setBooks(data)).finally(() => setLoading(false))
  }, [])

  const filtered = books.filter((b) =>
    [b.title, b.author, b.isbn, b.category].some((v) => (v || '').toLowerCase().includes(search.toLowerCase()))
  )

  if (loading) return <LoadingSpinner />

  return (
    <>
      <h2 className="text-2xl font-bold text-slate-800 mb-6">View Books</h2>
      <input type="text" placeholder="Search..." value={search} onChange={(e) => setSearch(e.target.value)} className="mb-4 max-w-xs px-4 py-2 border rounded-lg" />
      <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-50"><tr><th className="text-left px-6 py-3">Title</th><th className="text-left px-6 py-3">Author</th><th className="text-left px-6 py-3">Category</th><th className="text-left px-6 py-3">Available</th></tr></thead>
          <tbody>
            {filtered.map((b) => (
              <tr key={b.book_id} className="border-b border-slate-100"><td className="px-6 py-4">{b.title}</td><td className="px-6 py-4">{b.author}</td><td className="px-6 py-4">{b.category || '-'}</td><td className="px-6 py-4">{b.available_copies}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  )
}
