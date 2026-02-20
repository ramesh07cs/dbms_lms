import { useEffect, useState } from 'react'
import { booksApi } from '../../api/services'
import LoadingSpinner from '../../components/LoadingSpinner'
import toast from 'react-hot-toast'

export default function ManageBooks() {
  const [books, setBooks] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState({ title: '', author: '', category: '', isbn: '', total_copies: '', available_copies: '' })

  const load = () => {
    booksApi.getAll()
      .then(({ data }) => setBooks(data))
      .catch(() => toast.error('Failed to load'))
      .finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const openAdd = () => {
    setEditing(null)
    setForm({ title: '', author: '', category: '', isbn: '', total_copies: '', available_copies: '' })
    setShowModal(true)
  }

  const openEdit = (b) => {
    setEditing(b)
    setForm({
      title: b.title,
      author: b.author,
      category: b.category || '',
      isbn: b.isbn,
      total_copies: String(b.total_copies ?? ''),
      available_copies: String(b.available_copies ?? ''),
    })
    setShowModal(true)
  }

  const save = async () => {
    if (!form.title || !form.author || !form.isbn || !form.total_copies) {
      toast.error('Title, author, ISBN and total copies required')
      return
    }
    const total = parseInt(form.total_copies, 10)
    const avail = form.available_copies !== '' ? parseInt(form.available_copies, 10) : total
    if (isNaN(total) || total < 0) {
      toast.error('Total copies must be a non-negative number')
      return
    }
    if (editing && form.available_copies !== '' && (isNaN(avail) || avail < 0 || avail > total)) {
      toast.error('Available copies must be between 0 and total copies')
      return
    }
    try {
      if (editing) {
        await booksApi.update(editing.book_id, {
          ...form,
          total_copies: total,
          available_copies: form.available_copies !== '' ? avail : Number(editing.available_copies),
        })
        toast.success('Book updated')
      } else {
        await booksApi.create({
          ...form,
          total_copies: total,
          available_copies: form.available_copies !== '' ? avail : total,
        })
        toast.success('Book added')
      }
      setShowModal(false)
      load()
    } catch (e) {
      toast.error(e.response?.data?.error || 'Failed')
    }
  }

  const del = async (id) => {
    if (!confirm('Delete this book?')) return
    try {
      await booksApi.delete(id)
      toast.success('Book deleted')
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
      <h2 className="text-2xl font-bold text-slate-800 mb-6">Manage Books</h2>
      <div className="flex gap-4 mb-4">
        <input
          type="text"
          placeholder="Search..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-1 max-w-xs px-4 py-2 border border-slate-300 rounded-lg"
        />
        <button onClick={openAdd} className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">Add Book</button>
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Title</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Author</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Category</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">ISBN</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Total</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Available</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Actions</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((b) => (
              <tr key={b.book_id} className="border-b border-slate-100 hover:bg-slate-50">
                <td className="px-6 py-4">{b.title}</td>
                <td className="px-6 py-4">{b.author}</td>
                <td className="px-6 py-4">{b.category || '-'}</td>
                <td className="px-6 py-4">{b.isbn}</td>
                <td className="px-6 py-4">{b.total_copies}</td>
                <td className="px-6 py-4">{b.available_copies}</td>
                <td className="px-6 py-4 flex gap-2">
                  <button onClick={() => openEdit(b)} className="text-primary-600 hover:underline">Edit</button>
                  <button onClick={() => del(b.book_id)} className="text-red-600 hover:underline">Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 w-full max-w-md">
            <h3 className="text-lg font-bold mb-4">{editing ? 'Edit Book' : 'Add Book'}</h3>
            <div className="space-y-3">
              <input value={form.title} onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))} placeholder="Title" className="w-full px-4 py-2 border rounded" />
              <input value={form.author} onChange={(e) => setForm((f) => ({ ...f, author: e.target.value }))} placeholder="Author" className="w-full px-4 py-2 border rounded" />
              <input value={form.category} onChange={(e) => setForm((f) => ({ ...f, category: e.target.value }))} placeholder="Category" className="w-full px-4 py-2 border rounded" />
              <input value={form.isbn} onChange={(e) => setForm((f) => ({ ...f, isbn: e.target.value }))} placeholder="ISBN" className="w-full px-4 py-2 border rounded" disabled={!!editing} />
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Total Copies</label>
                <input type="number" min={0} value={form.total_copies} onChange={(e) => setForm((f) => ({ ...f, total_copies: e.target.value }))} placeholder="Total copies" className="w-full px-4 py-2 border rounded" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Available Copies</label>
                <input type="number" min={0} value={form.available_copies} onChange={(e) => setForm((f) => ({ ...f, available_copies: e.target.value }))} placeholder="Available (e.g. same as total)" className="w-full px-4 py-2 border rounded" />
              </div>
            </div>
            <div className="flex gap-2 mt-6">
              <button onClick={save} className="flex-1 py-2 bg-primary-600 text-white rounded">Save</button>
              <button onClick={() => setShowModal(false)} className="flex-1 py-2 border rounded">Cancel</button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
