import { Outlet } from 'react-router-dom'
import SidebarLayout from './SidebarLayout'

const navItems = [
  { to: '/admin', label: 'Dashboard', icon: '📊', end: true },
  { to: '/admin/verify-users', label: 'Verify Users', icon: '✓' },
  { to: '/admin/books', label: 'Manage Books', icon: '📚' },
  { to: '/admin/issue-book', label: 'Issue Book', icon: '📤' },
  { to: '/admin/return-book', label: 'Return Book', icon: '📥' },
  { to: '/admin/reservations', label: 'All Reservations', icon: '📋' },
  { to: '/admin/fines', label: 'Fine Management', icon: '💰' },
  { to: '/admin/audit', label: 'Audit Logs', icon: '📜' },
]

export default function AdminLayout() {
  return (
    <SidebarLayout navItems={navItems}>
      <Outlet />
    </SidebarLayout>
  )
}
