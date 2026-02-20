import { Outlet } from 'react-router-dom'
import SidebarLayout from './SidebarLayout'

const navItems = [
  { to: '/teacher', label: 'Dashboard', icon: '📊', end: true },
  { to: '/teacher/available', label: 'Available Books', icon: '📚' },
  { to: '/teacher/books', label: 'View Books', icon: '📖' },
  { to: '/teacher/borrowed', label: 'Borrowed Books', icon: '📥' },
  { to: '/teacher/reservations', label: 'Reservations', icon: '📋' },
]

export default function TeacherLayout() {
  return (
    <SidebarLayout navItems={navItems}>
      <Outlet />
    </SidebarLayout>
  )
}
