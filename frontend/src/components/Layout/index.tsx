import { ReactNode } from 'react'
import { Box } from '@mui/material'
import Navbar from '../Navbar'

interface LayoutProps {
  children: ReactNode
}

function Layout({ children }: LayoutProps) {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />
      <Box component="main" sx={{ flexGrow: 1, py: 3 }}>
        {children}
      </Box>
    </Box>
  )
}

export default Layout
