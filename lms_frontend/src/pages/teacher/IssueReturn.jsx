import { useEffect, useState } from 'react'
import { borrowApi, booksApi } from '../../api/services'
import toast from 'react-hot-toast'

export default function TeacherIssueReturn() {
  const [books, setBooks] = useState([])
  const [activeBorrows, setActiveBorrows] = useState([])
  const [bookId, setBookId] = useState('')
  const [returnBookId, setReturnBookId] = useState('')
  const [loading, setLoading] = useState(false)

  const load = () => {
    booksApi.getAll().then(({ data }) => setBooks(data.filter((b) => b.available_copies > 0)))
    borrowApi.myActive().then(({ data }) => setActiveBorrows(data))
  }

  useEffect(() => { load() }, [])

  const issue = async (e) => {
    e.preventDefault()
    if (!bookId) { toast.error('Select a book'); return }
    setLoading(true)
    try {
      await borrowApi.issue(parseInt(bookId))
      toast.success('Book issued')
      setBookId('')
      load()
    } catch (e) {
      toast.error(e.response?.data?.error || 'Failed')
    } finally {
      setLoading(false)
    }
  }

  const returnBook = async (e) => {
    e.preventDefault()
    if (!returnBookId) { toast.error('Select a borrow'); return }
    setLoading(true)
    try {
      await borrowApi.return(parseInt(returnBookId))
      toast.success('Book returned')
      setReturnBookId('')
      load()
    } catch (e) {
      toast.error(e.response?.data?.error || 'Failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <h2 className="text-2xl font-bold text-slate-800 mb-6">Issue / Return Books</h2>
      <div className="grid md:grid-cols-2 gap-8">
        <form onSubmit={issue} className="space-y-3">
          <h3 className="font-semibold">Issue Book</h3>
          <select value={bookId} onChange={(e) => setBookId(e.target.value)} className="w-full px-4 py-2 border rounded-lg">
            <option value="">Select book</option>
            {books.map((b) => <option key={b.book_id} value={b.book_id}>{b.title} (avail: {b.available_copies})</option>)}
          </select>
          <button type="submit" disabled={loading} className="px-4 py-2 bg-primary-600 text-white rounded-lg">Issue</button>
        </form>
        <form onSubmit={returnBook} className="space-y-3">
          <h3 className="font-semibold">Return Book</h3>
          <select value={returnBookId} onChange={(e) => setReturnBookId(e.target.value)} className="w-full px-4 py-2 border rounded-lg">
            <option value="">Select active borrow</option>
            {activeBorrows.map((b) => <option key={b.borrow_id} value={b.book_id}>{b.title} (due: {new Date(b.due_date).toLocaleDateString()})</option>)}
          </select>
          <button type="submit" disabled={loading} className="px-4 py-2 bg-primary-600 text-white rounded-lg">Return</button>
        </form>
      </div>
    </>
  )
}
