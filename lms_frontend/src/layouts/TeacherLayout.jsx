import { Outlet } from 'react-router-dom'
import SidebarLayout from './SidebarLayout'

const navItems = [
  { to: '/teacher', label: 'Dashboard', icon: '📊', end: true },
  { to: '/teacher/issue-return', label: 'Issue/Return Books', icon: '📚' },
  { to: '/teacher/books', label: 'View Books', icon: '📖' },
  { to: '/teacher/reservations', label: 'View Reservations', icon: '📋' },
]

export default function TeacherLayout() {
  return (
    <SidebarLayout navItems={navItems}>
      <Outlet />
    </SidebarLayout>
  )
}
