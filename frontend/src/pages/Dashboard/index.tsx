import { Typography, Grid, Paper, Box } from '@mui/material'

function Dashboard() {
  return (
    <div>
      <Typography variant="h4" component="h1" gutterBottom>
        Dashboard
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6} lg={4}>
          <Paper sx={{ p: 2 }}>
            <Box>
              <Typography variant="h6" gutterBottom>
                Sensor Readings
              </Typography>
              {/* Add sensor components here */}
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6} lg={4}>
          <Paper sx={{ p: 2 }}>
            <Box>
              <Typography variant="h6" gutterBottom>
                Controls
              </Typography>
              {/* Add control components here */}
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={12} lg={4}>
          <Paper sx={{ p: 2 }}>
            <Box>
              <Typography variant="h6" gutterBottom>
                System Status
              </Typography>
              {/* Add status components here */}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </div>
  )
}

export default Dashboard
