import { useEffect, useState } from 'react'
import { borrowApi, booksApi } from '../../api/services'
import toast from 'react-hot-toast'

export default function IssueBook() {
  const [users, setUsers] = useState([])
  const [books, setBooks] = useState([])
  const [userId, setUserId] = useState('')
  const [bookId, setBookId] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    borrowApi.adminUsers().then(({ data }) => setUsers(data)).catch(() => { })
    booksApi.getAll().then(({ data }) => setBooks(data.filter((b) => b.available_copies > 0))).catch(() => { })
  }, [])

  const submit = async (e) => {
    e.preventDefault()
    if (!userId || !bookId) {
      toast.error('Select user and book')
      return
    }
    setLoading(true)
    try {
      await borrowApi.adminIssue(parseInt(userId), parseInt(bookId))
      toast.success('Book issued')
      setUserId('')
      setBookId('')
    } catch (e) {
      toast.error(e.response?.data?.error || 'Failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <h2 className="text-2xl font-bold text-slate-800 mb-6">Issue Book</h2>
      <form onSubmit={submit} className="max-w-md space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Select User</label>
          <select value={userId} onChange={(e) => setUserId(e.target.value)} className="w-full px-4 py-2 border rounded-lg" required>
            <option value="">-- Select user --</option>
            {users.map((u) => (
              <option key={u.user_id} value={u.user_id}>{u.name} ({u.email}) - {u.role_name}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Select Book</label>
          <select value={bookId} onChange={(e) => setBookId(e.target.value)} className="w-full px-4 py-2 border rounded-lg" required>
            <option value="">-- Select book --</option>
            {books.filter((b) => b.available_copies > 0).map((b) => (
              <option key={b.book_id} value={b.book_id}>{b.title} by {b.author} (avail: {b.available_copies})</option>
            ))}
          </select>
        </div>
        <button type="submit" disabled={loading} className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50">Issue</button>
      </form>
    </>
  )
}
