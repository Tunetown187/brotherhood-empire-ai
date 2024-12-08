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
  Tooltip,
  CircularProgress,
} from '@mui/material';
import {
  Add as AddIcon,
  ExpandMore as ExpandMoreIcon,
  PlayArrow as PlayIcon,
  Settings as SettingsIcon,
  Check as CheckIcon,
  Error as ErrorIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const platformTypes = [
  {
    value: 'gohighlevel',
    label: 'GoHighLevel',
    fields: ['api_key', 'location_id', 'agency_id'],
    credentialTypes: ['api_key', 'oauth'],
    category: 'CRM'
  },
  {
    value: 'make',
    label: 'Make.com',
    fields: ['api_key'],
    credentialTypes: ['api_key'],
    category: 'Automation'
  },
  {
    value: 'n8n',
    label: 'n8n',
    fields: ['api_key', 'base_url'],
    credentialTypes: ['api_key', 'basic_auth'],
    category: 'Automation'
  },
  {
    value: 'wordpress',
    label: 'WordPress',
    fields: ['url', 'username', 'application_password'],
    credentialTypes: ['basic_auth'],
    category: 'Website'
  },
  {
    value: 'openai',
    label: 'OpenAI',
    fields: ['api_key'],
    credentialTypes: ['api_key'],
    category: 'AI'
  },
  {
    value: 'anthropic',
    label: 'Anthropic',
    fields: ['api_key'],
    credentialTypes: ['api_key'],
    category: 'AI'
  },
  {
    value: 'google_analytics',
    label: 'Google Analytics',
    fields: ['credentials_json'],
    credentialTypes: ['oauth', 'service_account'],
    category: 'Analytics'
  },
  {
    value: 'google_search_console',
    label: 'Google Search Console',
    fields: ['credentials_json'],
    credentialTypes: ['oauth', 'service_account'],
    category: 'SEO'
  },
  {
    value: 'ahrefs',
    label: 'Ahrefs',
    fields: ['api_key'],
    credentialTypes: ['api_key'],
    category: 'SEO'
  },
  {
    value: 'semrush',
    label: 'SEMrush',
    fields: ['api_key'],
    credentialTypes: ['api_key'],
    category: 'SEO'
  },
  {
    value: 'mailchimp',
    label: 'Mailchimp',
    fields: ['api_key', 'server_prefix'],
    credentialTypes: ['api_key'],
    category: 'Email Marketing'
  },
  {
    value: 'klaviyo',
    label: 'Klaviyo',
    fields: ['api_key'],
    credentialTypes: ['api_key'],
    category: 'Email Marketing'
  },
  {
    value: 'stripe',
    label: 'Stripe',
    fields: ['api_key', 'webhook_secret'],
    credentialTypes: ['api_key'],
    category: 'Payments'
  },
  {
    value: 'quickbooks',
    label: 'QuickBooks',
    fields: ['client_id', 'client_secret', 'refresh_token'],
    credentialTypes: ['oauth'],
    category: 'Accounting'
  },
  {
    value: 'xero',
    label: 'Xero',
    fields: ['client_id', 'client_secret', 'refresh_token'],
    credentialTypes: ['oauth'],
    category: 'Accounting'
  },
  {
    value: 'hubspot',
    label: 'HubSpot',
    fields: ['api_key'],
    credentialTypes: ['api_key', 'oauth'],
    category: 'CRM'
  },
  {
    value: 'salesforce',
    label: 'Salesforce',
    fields: ['client_id', 'client_secret', 'refresh_token', 'instance_url'],
    credentialTypes: ['oauth'],
    category: 'CRM'
  },
  {
    value: 'zoom',
    label: 'Zoom',
    fields: ['client_id', 'client_secret', 'refresh_token'],
    credentialTypes: ['oauth'],
    category: 'Meetings'
  },
  {
    value: 'calendly',
    label: 'Calendly',
    fields: ['api_key'],
    credentialTypes: ['api_key'],
    category: 'Scheduling'
  },
  {
    value: 'twilio',
    label: 'Twilio',
    fields: ['account_sid', 'auth_token'],
    credentialTypes: ['api_key'],
    category: 'Communications'
  },
  {
    value: 'slack',
    label: 'Slack',
    fields: ['bot_token', 'signing_secret'],
    credentialTypes: ['oauth'],
    category: 'Communications'
  },
  {
    value: 'discord',
    label: 'Discord',
    fields: ['bot_token'],
    credentialTypes: ['api_key'],
    category: 'Communications'
  },
  {
    value: 'github',
    label: 'GitHub',
    fields: ['access_token'],
    credentialTypes: ['oauth', 'api_key'],
    category: 'Development'
  },
  {
    value: 'asana',
    label: 'Asana',
    fields: ['access_token'],
    credentialTypes: ['oauth'],
    category: 'Project Management'
  },
  {
    value: 'monday',
    label: 'Monday.com',
    fields: ['api_key'],
    credentialTypes: ['api_key'],
    category: 'Project Management'
  },
  {
    value: 'clickup',
    label: 'ClickUp',
    fields: ['api_key'],
    credentialTypes: ['api_key'],
    category: 'Project Management'
  },
  {
    value: 'google_ads',
    label: 'Google Ads',
    fields: ['developer_token', 'client_id', 'client_secret', 'refresh_token'],
    credentialTypes: ['oauth'],
    category: 'Advertising'
  },
  {
    value: 'facebook_ads',
    label: 'Facebook Ads',
    fields: ['access_token'],
    credentialTypes: ['oauth'],
    category: 'Advertising'
  },
  {
    value: 'linkedin_ads',
    label: 'LinkedIn Ads',
    fields: ['access_token'],
    credentialTypes: ['oauth'],
    category: 'Advertising'
  },
  {
    value: 'twitter',
    label: 'Twitter',
    fields: ['api_key', 'api_secret', 'access_token', 'access_token_secret'],
    credentialTypes: ['oauth'],
    category: 'Social Media'
  },
  {
    value: 'instagram',
    label: 'Instagram',
    fields: ['access_token'],
    credentialTypes: ['oauth'],
    category: 'Social Media'
  }
];

function AutomationPlatforms() {
  const [platforms, setPlatforms] = useState({});
  const [workflows, setWorkflows] = useState([]);
  const [openPlatform, setOpenPlatform] = useState(false);
  const [openWorkflow, setOpenWorkflow] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [platformStatus, setPlatformStatus] = useState({});
  const [testingPlatform, setTestingPlatform] = useState('');

  const [newPlatform, setNewPlatform] = useState({
    platform: '',
    api_key: '',
    base_url: '',
    location_id: '',
    agency_id: '',
    workflows: {}
  });

  const [newWorkflow, setNewWorkflow] = useState({
    name: '',
    platform: '',
    workflow_id: '',
    description: '',
    triggers: [],
    required_credentials: []
  });

  useEffect(() => {
    fetchPlatforms();
    fetchWorkflows();
  }, []);

  const fetchPlatforms = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/platforms`);
      setPlatforms(response.data || {});
    } catch (error) {
      console.error('Error fetching platforms:', error);
      setError(error.response?.data?.detail || 'Error fetching platforms');
    }
  };

  const fetchWorkflows = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/workflows`);
      setWorkflows(response.data || []);
    } catch (error) {
      console.error('Error fetching workflows:', error);
      setError(error.response?.data?.detail || 'Error fetching workflows');
    }
  };

  const handleOpenPlatform = () => setOpenPlatform(true);
  const handleClosePlatform = () => {
    setOpenPlatform(false);
    setNewPlatform({
      platform: '',
      api_key: '',
      base_url: '',
      location_id: '',
      agency_id: '',
      workflows: {}
    });
  };

  const handleOpenWorkflow = () => setOpenWorkflow(true);
  const handleCloseWorkflow = () => {
    setOpenWorkflow(false);
    setNewWorkflow({
      name: '',
      platform: '',
      workflow_id: '',
      description: '',
      triggers: [],
      required_credentials: []
    });
  };

  const handleSubmitPlatform = async () => {
    try {
      setLoading(true);
      await axios.post(`${API_BASE_URL}/platforms`, newPlatform);
      setSuccess('Platform configured successfully');
      handleClosePlatform();
      fetchPlatforms();
    } catch (error) {
      console.error('Error configuring platform:', error);
      setError(error.response?.data?.detail || 'Error configuring platform');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitWorkflow = async () => {
    try {
      setLoading(true);
      await axios.post(`${API_BASE_URL}/workflows`, newWorkflow);
      setSuccess('Workflow saved successfully');
      handleCloseWorkflow();
      fetchWorkflows();
    } catch (error) {
      console.error('Error saving workflow:', error);
      setError(error.response?.data?.detail || 'Error saving workflow');
    } finally {
      setLoading(false);
    }
  };

  const testPlatformConnection = async (platformName) => {
    try {
      setTestingPlatform(platformName);
      const response = await axios.post(`${API_BASE_URL}/platforms/${platformName}/test`);
      setPlatformStatus(prev => ({
        ...prev,
        [platformName]: { status: 'connected', lastTested: new Date() }
      }));
      setSuccess(`Successfully connected to ${platformName}`);
    } catch (error) {
      console.error(`Error testing platform ${platformName}:`, error);
      setPlatformStatus(prev => ({
        ...prev,
        [platformName]: { status: 'error', error: error.response?.data?.detail || 'Connection failed' }
      }));
      setError(`Failed to connect to ${platformName}: ${error.response?.data?.detail || 'Connection failed'}`);
    } finally {
      setTestingPlatform('');
    }
  };

  const groupedPlatforms = Object.entries(platforms).reduce((acc, [name, platform]) => {
    const category = platformTypes.find(p => p.value === platform.platform)?.category || 'Other';
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push({ name, ...platform });
    return acc;
  }, {});

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

      {/* Platforms Section */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
          <Typography variant="h5">Automation Platforms</Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={handleOpenPlatform}
            startIcon={<AddIcon />}
          >
            Add Platform
          </Button>
        </Box>

        {Object.entries(groupedPlatforms).map(([category, categoryPlatforms]) => (
          <Box key={category} sx={{ mb: 4 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>{category}</Typography>
            <Grid container spacing={3}>
              {categoryPlatforms.map((platform) => (
                <Grid item xs={12} md={6} lg={4} key={platform.name}>
                  <Card>
                    <CardContent>
                      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <SettingsIcon sx={{ mr: 1 }} />
                          <Typography variant="h6">
                            {platformTypes.find(p => p.value === platform.platform)?.label || platform.platform}
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          {platformStatus[platform.name]?.status === 'connected' && (
                            <Tooltip title="Connected">
                              <CheckIcon color="success" />
                            </Tooltip>
                          )}
                          {platformStatus[platform.name]?.status === 'error' && (
                            <Tooltip title={platformStatus[platform.name].error}>
                              <ErrorIcon color="error" />
                            </Tooltip>
                          )}
                          <IconButton
                            size="small"
                            onClick={() => testPlatformConnection(platform.name)}
                            disabled={testingPlatform === platform.name}
                          >
                            {testingPlatform === platform.name ? (
                              <CircularProgress size={20} />
                            ) : (
                              <RefreshIcon />
                            )}
                          </IconButton>
                        </Box>
                      </Box>
                      {platform.base_url && (
                        <Typography color="textSecondary" gutterBottom>
                          URL: {platform.base_url}
                        </Typography>
                      )}
                      <Typography variant="subtitle2" gutterBottom>
                        Connected Workflows: {Object.keys(platform.workflows || {}).length}
                      </Typography>
                      {platformStatus[platform.name]?.lastTested && (
                        <Typography variant="caption" color="textSecondary">
                          Last tested: {new Date(platformStatus[platform.name].lastTested).toLocaleString()}
                        </Typography>
                      )}
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Box>
        ))}
      </Box>

      {/* Workflows Section */}
      <Box>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
          <Typography variant="h5">Workflows</Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={handleOpenWorkflow}
            startIcon={<AddIcon />}
          >
            Add Workflow
          </Button>
        </Box>

        <Grid container spacing={3}>
          {workflows.map((workflow) => (
            <Grid item xs={12} md={6} lg={4} key={workflow.name}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <PlayIcon sx={{ mr: 1 }} />
                    <Typography variant="h6">
                      {workflow.name}
                    </Typography>
                  </Box>
                  <Typography color="textSecondary" paragraph>
                    {workflow.description}
                  </Typography>
                  <Typography variant="subtitle2" gutterBottom>
                    Platform: {platformTypes.find(p => p.value === workflow.platform)?.label || workflow.platform}
                  </Typography>
                  {workflow.triggers.length > 0 && (
                    <Box sx={{ mt: 1 }}>
                      <Typography variant="subtitle2" gutterBottom>Triggers:</Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                        {workflow.triggers.map((trigger) => (
                          <Chip key={trigger} label={trigger} size="small" />
                        ))}
                      </Box>
                    </Box>
                  )}
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Add Platform Dialog */}
      <Dialog
        open={openPlatform}
        onClose={handleClosePlatform}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Add Automation Platform</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <FormControl fullWidth required>
              <InputLabel>Platform</InputLabel>
              <Select
                value={newPlatform.platform}
                onChange={(e) => setNewPlatform({ ...newPlatform, platform: e.target.value })}
              >
                {platformTypes.map((platform) => (
                  <MenuItem key={platform.value} value={platform.value}>
                    {platform.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            {newPlatform.platform && platformTypes
              .find(p => p.value === newPlatform.platform)
              ?.fields.map((field) => (
                <TextField
                  key={field}
                  label={field.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                  value={newPlatform[field] || ''}
                  onChange={(e) => setNewPlatform({ ...newPlatform, [field]: e.target.value })}
                  type={field.includes('key') || field.includes('token') ? 'password' : 'text'}
                  fullWidth
                  required
                />
              ))}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClosePlatform}>Cancel</Button>
          <Button
            onClick={handleSubmitPlatform}
            variant="contained"
            color="primary"
            disabled={loading || !newPlatform.platform}
          >
            {loading ? 'Saving...' : 'Save'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Add Workflow Dialog */}
      <Dialog
        open={openWorkflow}
        onClose={handleCloseWorkflow}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Add Workflow</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <TextField
              label="Workflow Name"
              value={newWorkflow.name}
              onChange={(e) => setNewWorkflow({ ...newWorkflow, name: e.target.value })}
              fullWidth
              required
            />

            <FormControl fullWidth required>
              <InputLabel>Platform</InputLabel>
              <Select
                value={newWorkflow.platform}
                onChange={(e) => setNewWorkflow({ ...newWorkflow, platform: e.target.value })}
              >
                {Object.keys(platforms).map((platform) => (
                  <MenuItem key={platform} value={platform}>
                    {platformTypes.find(p => p.value === platforms[platform]?.platform)?.label || platforms[platform]?.platform}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <TextField
              label="Workflow ID"
              value={newWorkflow.workflow_id}
              onChange={(e) => setNewWorkflow({ ...newWorkflow, workflow_id: e.target.value })}
              fullWidth
              required
              helperText="The ID of the workflow in the platform"
            />

            <TextField
              label="Description"
              value={newWorkflow.description}
              onChange={(e) => setNewWorkflow({ ...newWorkflow, description: e.target.value })}
              fullWidth
              multiline
              rows={2}
              required
            />

            <TextField
              label="Triggers"
              value={newWorkflow.triggers.join(', ')}
              onChange={(e) => setNewWorkflow({
                ...newWorkflow,
                triggers: e.target.value.split(',').map(t => t.trim()).filter(Boolean)
              })}
              fullWidth
              helperText="Comma-separated list of events that trigger this workflow"
            />

            <TextField
              label="Required Credentials"
              value={newWorkflow.required_credentials.join(', ')}
              onChange={(e) => setNewWorkflow({
                ...newWorkflow,
                required_credentials: e.target.value.split(',').map(t => t.trim()).filter(Boolean)
              })}
              fullWidth
              helperText={
                newWorkflow.platform
                  ? `Available credential types: ${platformTypes
                      .find(p => p.value === platforms[newWorkflow.platform]?.platform)
                      ?.credentialTypes.join(', ')}`
                  : 'Select a platform to see available credential types'
              }
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseWorkflow}>Cancel</Button>
          <Button
            onClick={handleSubmitWorkflow}
            variant="contained"
            color="primary"
            disabled={loading || !newWorkflow.name || !newWorkflow.platform || !newWorkflow.workflow_id}
          >
            {loading ? 'Saving...' : 'Save'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default AutomationPlatforms;
