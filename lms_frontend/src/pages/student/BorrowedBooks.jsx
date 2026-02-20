import { useEffect, useState } from 'react'
import { borrowApi } from '../../api/services'
import LoadingSpinner from '../../components/LoadingSpinner'
import toast from 'react-hot-toast'

export default function BorrowedBooks() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)

  const load = () => {
    borrowApi.myActive().then(({ data }) => setItems(data)).finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const returnBook = async (bookId) => {
    try {
      const { data } = await borrowApi.return(bookId)
      toast.success(data.fine_amount > 0 ? `Returned. Fine: Rs ${data.fine_amount}` : 'Book returned successfully')
      load()
    } catch (e) {
      toast.error(e.response?.data?.error || 'Failed')
    }
  }

  if (loading) return <LoadingSpinner />

  return (
    <>
      <h2 className="text-2xl font-bold text-slate-800 mb-6">Borrowed Books</h2>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Title</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Author</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Issue Date</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Due Date</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Action</th>
            </tr>
          </thead>
          <tbody>
            {items.map((b) => (
              <tr key={b.borrow_id} className="border-b border-slate-100">
                <td className="px-6 py-4">{b.title}</td>
                <td className="px-6 py-4">{b.author}</td>
                <td className="px-6 py-4">{new Date(b.issue_date).toLocaleDateString()}</td>
                <td className="px-6 py-4">{new Date(b.due_date).toLocaleDateString()}</td>
                <td className="px-6 py-4">
                  <button onClick={() => returnBook(b.book_id)} className="px-3 py-1 bg-primary-600 text-white rounded text-sm">Return</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {items.length === 0 && <p className="p-8 text-slate-500 text-center">No borrowed books</p>}
      </div>
    </>
  )
}
