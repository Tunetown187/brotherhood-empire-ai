import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Dashboard from './components/Dashboard';
import EmailManagement from './components/EmailManagement';
import PaymentsManagement from './components/PaymentsManagement';
import DocumentsManagement from './components/DocumentsManagement';
import Settings from './components/Settings';
import AutomationPlatforms from './components/AutomationPlatforms';
import Sidebar from './components/Sidebar';
import { Box } from '@mui/material';
import AICaller from './components/AICaller';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9',
    },
    secondary: {
      main: '#f48fb1',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex' }}>
          <Sidebar />
          <Box component="main" sx={{ flexGrow: 1, p: 3, mt: 8 }}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/email" element={<EmailManagement />} />
              <Route path="/payments" element={<PaymentsManagement />} />
              <Route path="/documents" element={<DocumentsManagement />} />
              <Route path="/automations" element={<AutomationPlatforms />} />
              <Route path="/ai-caller" element={<AICaller />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
