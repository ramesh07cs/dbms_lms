import { Outlet } from 'react-router-dom'
import SidebarLayout from './SidebarLayout'

const navItems = [
  { to: '/student', label: 'Dashboard', icon: '📊', end: true },
  { to: '/student/books', label: 'View Books', icon: '📖' },
  { to: '/student/borrowed', label: 'Borrowed Books', icon: '📥' },
  { to: '/student/history', label: 'Borrow History', icon: '📜' },
  { to: '/student/fines', label: 'My Fines', icon: '💰' },
]

export default function StudentLayout() {
  return (
    <SidebarLayout navItems={navItems}>
      <Outlet />
    </SidebarLayout>
  )
}
