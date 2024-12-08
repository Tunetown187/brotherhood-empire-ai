import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
  Alert,
  Snackbar,
  IconButton,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Tabs,
  Tab,
  Tooltip,
} from '@mui/material';
import {
  Add as AddIcon,
  ExpandMore as ExpandMoreIcon,
  SupervisorAccount as SupervisorIcon,
  Person as WorkerIcon,
  VpnKey as KeyIcon,
} from '@mui/icons-material';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const availableTools = [
  'EmailTool',
  'InvoiceTool',
  'PaymentProcessor',
  'CalendarTool',
  'CustomerServiceTool',
  'DocumentGenerator',
];

const credentialTypes = [
  { value: 'api_key', label: 'API Key' },
  { value: 'oauth', label: 'OAuth' },
  { value: 'username_password', label: 'Username & Password' },
];

function Dashboard() {
  const [agents, setAgents] = useState([]);
  const [credentials, setCredentials] = useState({});
  const [openAgent, setOpenAgent] = useState(false);
  const [openCredential, setOpenCredential] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [tabValue, setTabValue] = useState(0);
  
  const [newAgent, setNewAgent] = useState({
    name: '',
    role: 'worker',
    description: '',
    tools: [],
    instructions: '',
    supervised_agents: [],
    required_credentials: [],
    schedule: {},
  });

  const [newCredential, setNewCredential] = useState({
    name: '',
    type: 'api_key',
    data: {},
  });

  useEffect(() => {
    fetchAgents();
    fetchCredentials();
  }, []);

  const fetchAgents = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/agents`);
      setAgents(response.data || []);
      setError('');
    } catch (error) {
      console.error('Error fetching agents:', error);
      setError(error.response?.data?.detail || 'Error fetching agents');
    } finally {
      setLoading(false);
    }
  };

  const fetchCredentials = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/credentials`);
      setCredentials(response.data || {});
    } catch (error) {
      console.error('Error fetching credentials:', error);
    }
  };

  const handleOpenAgent = () => setOpenAgent(true);
  const handleCloseAgent = () => {
    setOpenAgent(false);
    setNewAgent({
      name: '',
      role: 'worker',
      description: '',
      tools: [],
      instructions: '',
      supervised_agents: [],
      required_credentials: [],
      schedule: {},
    });
  };

  const handleOpenCredential = () => setOpenCredential(true);
  const handleCloseCredential = () => {
    setOpenCredential(false);
    setNewCredential({
      name: '',
      type: 'api_key',
      data: {},
    });
  };

  const handleSubmitAgent = async () => {
    try {
      setLoading(true);
      await axios.post(`${API_BASE_URL}/agents`, newAgent);
      setSuccess('Agent created successfully');
      handleCloseAgent();
      fetchAgents();
    } catch (error) {
      console.error('Error creating agent:', error);
      setError(error.response?.data?.detail || 'Error creating agent');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitCredential = async () => {
    try {
      setLoading(true);
      await axios.post(`${API_BASE_URL}/credentials`, newCredential);
      setSuccess('Credential saved successfully');
      handleCloseCredential();
      fetchCredentials();
    } catch (error) {
      console.error('Error saving credential:', error);
      setError(error.response?.data?.detail || 'Error saving credential');
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const renderAgentCard = (agent) => (
    <Grid item xs={12} md={6} lg={4} key={agent.name}>
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            {agent.role === 'supervisor' ? (
              <SupervisorIcon color="primary" sx={{ mr: 1 }} />
            ) : (
              <WorkerIcon color="secondary" sx={{ mr: 1 }} />
            )}
            <Typography variant="h6">
              {agent.name}
            </Typography>
          </Box>
          <Typography color="textSecondary" paragraph>
            {agent.description}
          </Typography>
          
          <Typography variant="subtitle2" gutterBottom>Tools:</Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
            {agent.tools.map((tool) => (
              <Chip key={tool} label={tool} size="small" />
            ))}
          </Box>

          {agent.supervised_agents.length > 0 && (
            <>
              <Typography variant="subtitle2" gutterBottom>Supervises:</Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                {agent.supervised_agents.map((agentName) => (
                  <Chip 
                    key={agentName} 
                    label={agentName}
                    size="small"
                    color="primary"
                    variant="outlined"
                  />
                ))}
              </Box>
            </>
          )}

          {agent.required_credentials.length > 0 && (
            <>
              <Typography variant="subtitle2" gutterBottom>Required Credentials:</Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {agent.required_credentials.map((credName) => (
                  <Chip 
                    key={credName}
                    label={credName}
                    size="small"
                    icon={<KeyIcon />}
                  />
                ))}
              </Box>
            </>
          )}
        </CardContent>
      </Card>
    </Grid>
  );

  return (
    <Box>
      <Snackbar open={!!error} autoHideDuration={6000} onClose={() => setError('')}>
        <Alert onClose={() => setError('')} severity="error">
          {error}
        </Alert>
      </Snackbar>

      <Snackbar open={!!success} autoHideDuration={6000} onClose={() => setSuccess('')}>
        <Alert onClose={() => setSuccess('')} severity="success">
          {success}
        </Alert>
      </Snackbar>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange}>
          <Tab label="AI Agents" />
          <Tab label="Credentials" />
        </Tabs>
      </Box>

      {tabValue === 0 && (
        <>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
            <Typography variant="h4">AI Agents</Typography>
            <Button 
              variant="contained" 
              color="primary" 
              onClick={handleOpenAgent}
              disabled={loading}
              startIcon={<AddIcon />}
            >
              Create New Agent
            </Button>
          </Box>

          <Grid container spacing={3}>
            {agents.map(renderAgentCard)}
          </Grid>
        </>
      )}

      {tabValue === 1 && (
        <>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
            <Typography variant="h4">Credentials</Typography>
            <Button 
              variant="contained" 
              color="primary" 
              onClick={handleOpenCredential}
              disabled={loading}
              startIcon={<AddIcon />}
            >
              Add New Credential
            </Button>
          </Box>

          <Grid container spacing={3}>
            {Object.entries(credentials).map(([name, cred]) => (
              <Grid item xs={12} md={6} lg={4} key={name}>
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <KeyIcon sx={{ mr: 1 }} />
                      <Typography variant="h6">
                        {name}
                      </Typography>
                    </Box>
                    <Typography color="textSecondary">
                      Type: {cred.type}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </>
      )}

      {/* Create Agent Dialog */}
      <Dialog 
        open={openAgent} 
        onClose={handleCloseAgent} 
        maxWidth="md" 
        fullWidth
      >
        <DialogTitle>Create New Agent</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <TextField
              label="Agent Name"
              value={newAgent.name}
              onChange={(e) => setNewAgent({ ...newAgent, name: e.target.value })}
              fullWidth
              required
            />
            
            <FormControl fullWidth required>
              <InputLabel>Role</InputLabel>
              <Select
                value={newAgent.role}
                onChange={(e) => setNewAgent({ ...newAgent, role: e.target.value })}
              >
                <MenuItem value="supervisor">Supervisor</MenuItem>
                <MenuItem value="worker">Worker</MenuItem>
              </Select>
            </FormControl>

            <TextField
              label="Description"
              value={newAgent.description}
              onChange={(e) => setNewAgent({ ...newAgent, description: e.target.value })}
              fullWidth
              multiline
              rows={2}
              required
            />

            <FormControl fullWidth required>
              <InputLabel>Tools</InputLabel>
              <Select
                multiple
                value={newAgent.tools}
                onChange={(e) => setNewAgent({ ...newAgent, tools: e.target.value })}
                renderValue={(selected) => (
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {selected.map((value) => (
                      <Chip key={value} label={value} />
                    ))}
                  </Box>
                )}
              >
                {availableTools.map((tool) => (
                  <MenuItem key={tool} value={tool}>
                    {tool}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            {newAgent.role === 'supervisor' && (
              <FormControl fullWidth>
                <InputLabel>Supervised Agents</InputLabel>
                <Select
                  multiple
                  value={newAgent.supervised_agents}
                  onChange={(e) => setNewAgent({ ...newAgent, supervised_agents: e.target.value })}
                  renderValue={(selected) => (
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {selected.map((value) => (
                        <Chip key={value} label={value} />
                      ))}
                    </Box>
                  )}
                >
                  {agents
                    .filter(a => a.role !== 'supervisor')
                    .map((agent) => (
                      <MenuItem key={agent.name} value={agent.name}>
                        {agent.name}
                      </MenuItem>
                    ))}
                </Select>
              </FormControl>
            )}

            <FormControl fullWidth>
              <InputLabel>Required Credentials</InputLabel>
              <Select
                multiple
                value={newAgent.required_credentials}
                onChange={(e) => setNewAgent({ ...newAgent, required_credentials: e.target.value })}
                renderValue={(selected) => (
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {selected.map((value) => (
                      <Chip key={value} label={value} />
                    ))}
                  </Box>
                )}
              >
                {Object.keys(credentials).map((credName) => (
                  <MenuItem key={credName} value={credName}>
                    {credName}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <TextField
              label="Instructions"
              value={newAgent.instructions}
              onChange={(e) => setNewAgent({ ...newAgent, instructions: e.target.value })}
              fullWidth
              multiline
              rows={4}
              required
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseAgent}>Cancel</Button>
          <Button 
            onClick={handleSubmitAgent}
            variant="contained" 
            color="primary"
            disabled={loading || !newAgent.name || !newAgent.description || newAgent.tools.length === 0}
          >
            {loading ? 'Creating...' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Add Credential Dialog */}
      <Dialog 
        open={openCredential} 
        onClose={handleCloseCredential}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Add New Credential</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <TextField
              label="Credential Name"
              value={newCredential.name}
              onChange={(e) => setNewCredential({ ...newCredential, name: e.target.value })}
              fullWidth
              required
              helperText="e.g., Gmail, Stripe, etc."
            />

            <FormControl fullWidth required>
              <InputLabel>Credential Type</InputLabel>
              <Select
                value={newCredential.type}
                onChange={(e) => setNewCredential({ ...newCredential, type: e.target.value })}
              >
                {credentialTypes.map((type) => (
                  <MenuItem key={type.value} value={type.value}>
                    {type.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            {newCredential.type === 'api_key' && (
              <TextField
                label="API Key"
                type="password"
                value={newCredential.data.api_key || ''}
                onChange={(e) => setNewCredential({
                  ...newCredential,
                  data: { api_key: e.target.value }
                })}
                fullWidth
                required
              />
            )}

            {newCredential.type === 'username_password' && (
              <>
                <TextField
                  label="Username"
                  value={newCredential.data.username || ''}
                  onChange={(e) => setNewCredential({
                    ...newCredential,
                    data: { ...newCredential.data, username: e.target.value }
                  })}
                  fullWidth
                  required
                />
                <TextField
                  label="Password"
                  type="password"
                  value={newCredential.data.password || ''}
                  onChange={(e) => setNewCredential({
                    ...newCredential,
                    data: { ...newCredential.data, password: e.target.value }
                  })}
                  fullWidth
                  required
                />
              </>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseCredential}>Cancel</Button>
          <Button 
            onClick={handleSubmitCredential}
            variant="contained" 
            color="primary"
            disabled={loading || !newCredential.name || !newCredential.type}
          >
            {loading ? 'Saving...' : 'Save'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default Dashboard;
