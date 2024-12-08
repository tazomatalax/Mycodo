import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Box, Container } from '@mui/material'
import Dashboard from './pages/Dashboard'
import Layout from './components/Layout'

function App() {
  return (
    <Router>
      <Layout>
        <Container maxWidth="lg">
          <Box sx={{ my: 4 }}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              {/* Add more routes here */}
            </Routes>
          </Box>
        </Container>
      </Layout>
    </Router>
  )
}

export default App
