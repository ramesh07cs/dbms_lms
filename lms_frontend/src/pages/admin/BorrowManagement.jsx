import { useEffect, useState } from 'react'
import { borrowApi, booksApi } from '../../api/services'
import LoadingSpinner from '../../components/LoadingSpinner'
import toast from 'react-hot-toast'

export default function BorrowManagement() {
    const [borrows, setBorrows] = useState([])
    const [books, setBooks] = useState([])
    const [loading, setLoading] = useState(true)
    const [statusFilter, setStatusFilter] = useState('ALL')
    const [acting, setActing] = useState(null)

    const loadBorrows = () => {
        borrowApi.adminAll()
            .then(({ data }) => setBorrows(data || []))
            .catch(() => {
                toast.error('Failed to load borrows')
                setBorrows([])
            })
    }

    const loadBooks = () => {
        booksApi.getAll()
            .then(({ data }) => setBooks(data || []))
            .catch(() => setBooks([]))
    }

    useEffect(() => {
        Promise.all([loadBorrows(), loadBooks()]).finally(() => setLoading(false))
    }, [])

    const handleApprove = async (borrowId) => {
        setActing(borrowId)
        try {
            await borrowApi.adminApprove(borrowId)
            toast.success('Borrow approved')
            loadBorrows()
            loadBooks() // Refresh to update available_copies
        } catch (e) {
            toast.error(e.response?.data?.error || 'Failed to approve')
        } finally {
            setActing(null)
        }
    }

    const handleReject = async (borrowId) => {
        setActing(borrowId)
        try {
            await borrowApi.adminReject(borrowId)
            toast.success('Borrow rejected')
            loadBorrows()
        } catch (e) {
            toast.error(e.response?.data?.error || 'Failed to reject')
        } finally {
            setActing(null)
        }
    }

    const getStatusDisplay = (status) => {
        const statusMap = {
            PENDING: 'PENDING',
            ACTIVE: 'ACTIVE',
            RETURNED: 'RETURNED',
            REJECTED: 'REJECTED',
            OVERDUE: 'OVERDUE',
        }
        return statusMap[status] || status
    }

    const filteredBorrows = borrows.filter((b) => {
        if (statusFilter === 'ALL') return true
        if (statusFilter === 'PENDING') return b.borrow_status === 'PENDING'
        if (statusFilter === 'ACTIVE') return b.borrow_status === 'ACTIVE'
        if (statusFilter === 'RETURNED') return b.borrow_status === 'RETURNED'
        return true
    })

    const getBookAvailableCopies = (bookId) => {
        const book = books.find((b) => b.book_id === bookId)
        return book?.available_copies ?? '-'
    }

    if (loading) return <LoadingSpinner />

    return (
        <>
            <h2 className="text-2xl font-bold text-slate-800 mb-6">Borrow Management</h2>

            {/* Filter Tabs */}
            <div className="mb-4 flex gap-2 border-b border-slate-200">
                {['ALL', 'PENDING', 'ACTIVE', 'RETURNED'].map((status) => (
                    <button
                        key={status}
                        onClick={() => setStatusFilter(status)}
                        className={`px-4 py-2 font-medium transition-colors ${statusFilter === status
                                ? 'border-b-2 border-primary-600 text-primary-600'
                                : 'text-slate-600 hover:text-slate-800'
                            }`}
                    >
                        {status}
                        {status === 'PENDING' && borrows.filter((b) => b.borrow_status === 'PENDING').length > 0 && (
                            <span className="ml-2 px-2 py-0.5 bg-primary-100 text-primary-700 rounded-full text-xs">
                                {borrows.filter((b) => b.borrow_status === 'PENDING').length}
                            </span>
                        )}
                    </button>
                ))}
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                <table className="w-full">
                    <thead className="bg-slate-50 border-b border-slate-200">
                        <tr>
                            <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">User Name</th>
                            <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Role</th>
                            <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Book Title</th>
                            <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Requested Date</th>
                            <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Due Date</th>
                            <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Status</th>
                            <th className="text-left px-6 py-3 text-sm font-medium text-slate-700">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredBorrows.length === 0 && (
                            <tr>
                                <td colSpan={7} className="px-6 py-8 text-slate-500 text-center">
                                    No borrows found
                                </td>
                            </tr>
                        )}
                        {filteredBorrows.map((b) => (
                            <tr key={b.borrow_id} className="border-b border-slate-100 hover:bg-slate-50">
                                <td className="px-6 py-4">{b.user_name}</td>
                                <td className="px-6 py-4">{b.role_name}</td>
                                <td className="px-6 py-4">
                                    <div>{b.book_title}</div>
                                    <div className="text-xs text-slate-500">Available: {getBookAvailableCopies(b.book_id)}</div>
                                </td>
                                <td className="px-6 py-4">
                                    {b.requested_date ? new Date(b.requested_date).toLocaleDateString() : '-'}
                                </td>
                                <td className="px-6 py-4">
                                    {b.due_date ? new Date(b.due_date).toLocaleDateString() : '-'}
                                </td>
                                <td className="px-6 py-4">
                                    <span
                                        className={`px-2 py-0.5 rounded text-xs ${b.borrow_status === 'PENDING'
                                                ? 'bg-amber-100 text-amber-800'
                                                : b.borrow_status === 'ACTIVE'
                                                    ? 'bg-green-100 text-green-800'
                                                    : b.borrow_status === 'RETURNED'
                                                        ? 'bg-slate-100 text-slate-800'
                                                        : b.borrow_status === 'REJECTED'
                                                            ? 'bg-red-100 text-red-800'
                                                            : 'bg-slate-100 text-slate-800'
                                            }`}
                                    >
                                        {getStatusDisplay(b.borrow_status)}
                                    </span>
                                </td>
                                <td className="px-6 py-4">
                                    {b.borrow_status === 'PENDING' && (
                                        <div className="flex gap-2">
                                            <button
                                                onClick={() => handleApprove(b.borrow_id)}
                                                disabled={acting !== null}
                                                className="px-3 py-1 bg-green-600 text-white rounded text-sm hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                                            >
                                                Approve
                                            </button>
                                            <button
                                                onClick={() => handleReject(b.borrow_id)}
                                                disabled={acting !== null}
                                                className="px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed"
                                            >
                                                Reject
                                            </button>
                                        </div>
                                    )}
                                    {b.borrow_status !== 'PENDING' && <span className="text-slate-400 text-sm">-</span>}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </>
    )
}
