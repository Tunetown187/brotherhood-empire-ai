import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  TextField,
  Switch,
  FormControlLabel,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemSecondary,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
  Snackbar,
  CircularProgress,
  Tab,
  Tabs,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Paper,
  Chip,
} from '@mui/material';
import {
  Save as SaveIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Add as AddIcon,
  Refresh as RefreshIcon,
  Security as SecurityIcon,
  Notifications as NotificationsIcon,
  Email as EmailIcon,
  Payment as PaymentIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

function Settings() {
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [settings, setSettings] = useState({
    general: {
      companyName: '',
      companyEmail: '',
      timezone: 'UTC',
      dateFormat: 'YYYY-MM-DD',
      currency: 'USD',
    },
    email: {
      defaultTemplate: '',
      signature: '',
      ccAdmin: false,
      sendCopyToSender: false,
    },
    notifications: {
      emailNotifications: true,
      paymentReminders: true,
      documentUpdates: true,
      reminderFrequency: 'weekly',
      reminderDaysBefore: 7,
    },
    payment: {
      paymentMethods: ['credit_card', 'bank_transfer'],
      defaultPaymentTerms: 30,
      lateFeePercentage: 5,
      automaticReminders: true,
    },
    security: {
      twoFactorAuth: false,
      sessionTimeout: 30,
      ipWhitelist: [],
      passwordExpiryDays: 90,
    },
  });

  const [openDialog, setOpenDialog] = useState('');
  const [editItem, setEditItem] = useState(null);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/settings`);
      setSettings(response.data);
    } catch (error) {
      console.error('Error fetching settings:', error);
      setError('Failed to fetch settings');
    }
  };

  const handleSaveSettings = async (section, data) => {
    try {
      setLoading(true);
      await axios.post(`${API_BASE_URL}/settings/${section}`, data);
      setSuccess('Settings saved successfully');
      fetchSettings();
    } catch (error) {
      console.error('Error saving settings:', error);
      setError('Failed to save settings');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (section, field, value) => {
    setSettings(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value
      }
    }));
  };

  const renderGeneralSettings = () => (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          General Settings
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <TextField
              label="Company Name"
              value={settings.general.companyName}
              onChange={(e) => handleChange('general', 'companyName', e.target.value)}
              fullWidth
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Company Email"
              value={settings.general.companyEmail}
              onChange={(e) => handleChange('general', 'companyEmail', e.target.value)}
              fullWidth
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel>Timezone</InputLabel>
              <Select
                value={settings.general.timezone}
                onChange={(e) => handleChange('general', 'timezone', e.target.value)}
              >
                <MenuItem value="UTC">UTC</MenuItem>
                <MenuItem value="America/New_York">Eastern Time</MenuItem>
                <MenuItem value="America/Los_Angeles">Pacific Time</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel>Date Format</InputLabel>
              <Select
                value={settings.general.dateFormat}
                onChange={(e) => handleChange('general', 'dateFormat', e.target.value)}
              >
                <MenuItem value="YYYY-MM-DD">YYYY-MM-DD</MenuItem>
                <MenuItem value="MM/DD/YYYY">MM/DD/YYYY</MenuItem>
                <MenuItem value="DD/MM/YYYY">DD/MM/YYYY</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel>Currency</InputLabel>
              <Select
                value={settings.general.currency}
                onChange={(e) => handleChange('general', 'currency', e.target.value)}
              >
                <MenuItem value="USD">USD ($)</MenuItem>
                <MenuItem value="EUR">EUR (€)</MenuItem>
                <MenuItem value="GBP">GBP (£)</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );

  const renderEmailSettings = () => (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Email Settings
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              label="Default Email Template"
              value={settings.email.defaultTemplate}
              onChange={(e) => handleChange('email', 'defaultTemplate', e.target.value)}
              multiline
              rows={4}
              fullWidth
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              label="Email Signature"
              value={settings.email.signature}
              onChange={(e) => handleChange('email', 'signature', e.target.value)}
              multiline
              rows={4}
              fullWidth
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControlLabel
              control={
                <Switch
                  checked={settings.email.ccAdmin}
                  onChange={(e) => handleChange('email', 'ccAdmin', e.target.checked)}
                />
              }
              label="CC Admin on All Emails"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControlLabel
              control={
                <Switch
                  checked={settings.email.sendCopyToSender}
                  onChange={(e) => handleChange('email', 'sendCopyToSender', e.target.checked)}
                />
              }
              label="Send Copy to Sender"
            />
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );

  const renderNotificationSettings = () => (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Notification Settings
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <FormControlLabel
              control={
                <Switch
                  checked={settings.notifications.emailNotifications}
                  onChange={(e) => handleChange('notifications', 'emailNotifications', e.target.checked)}
                />
              }
              label="Email Notifications"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControlLabel
              control={
                <Switch
                  checked={settings.notifications.paymentReminders}
                  onChange={(e) => handleChange('notifications', 'paymentReminders', e.target.checked)}
                />
              }
              label="Payment Reminders"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControlLabel
              control={
                <Switch
                  checked={settings.notifications.documentUpdates}
                  onChange={(e) => handleChange('notifications', 'documentUpdates', e.target.checked)}
                />
              }
              label="Document Update Notifications"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Reminder Frequency</InputLabel>
              <Select
                value={settings.notifications.reminderFrequency}
                onChange={(e) => handleChange('notifications', 'reminderFrequency', e.target.value)}
              >
                <MenuItem value="daily">Daily</MenuItem>
                <MenuItem value="weekly">Weekly</MenuItem>
                <MenuItem value="monthly">Monthly</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Reminder Days Before"
              type="number"
              value={settings.notifications.reminderDaysBefore}
              onChange={(e) => handleChange('notifications', 'reminderDaysBefore', parseInt(e.target.value))}
              fullWidth
            />
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );

  const renderPaymentSettings = () => (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Payment Settings
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Payment Methods</InputLabel>
              <Select
                multiple
                value={settings.payment.paymentMethods}
                onChange={(e) => handleChange('payment', 'paymentMethods', e.target.value)}
              >
                <MenuItem value="credit_card">Credit Card</MenuItem>
                <MenuItem value="bank_transfer">Bank Transfer</MenuItem>
                <MenuItem value="paypal">PayPal</MenuItem>
                <MenuItem value="cash">Cash</MenuItem>
                <MenuItem value="check">Check</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Default Payment Terms (Days)"
              type="number"
              value={settings.payment.defaultPaymentTerms}
              onChange={(e) => handleChange('payment', 'defaultPaymentTerms', parseInt(e.target.value))}
              fullWidth
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Late Fee Percentage"
              type="number"
              value={settings.payment.lateFeePercentage}
              onChange={(e) => handleChange('payment', 'lateFeePercentage', parseFloat(e.target.value))}
              fullWidth
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControlLabel
              control={
                <Switch
                  checked={settings.payment.automaticReminders}
                  onChange={(e) => handleChange('payment', 'automaticReminders', e.target.checked)}
                />
              }
              label="Automatic Payment Reminders"
            />
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );

  const renderSecuritySettings = () => (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Security Settings
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <FormControlLabel
              control={
                <Switch
                  checked={settings.security.twoFactorAuth}
                  onChange={(e) => handleChange('security', 'twoFactorAuth', e.target.checked)}
                />
              }
              label="Two-Factor Authentication"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Session Timeout (minutes)"
              type="number"
              value={settings.security.sessionTimeout}
              onChange={(e) => handleChange('security', 'sessionTimeout', parseInt(e.target.value))}
              fullWidth
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Password Expiry (days)"
              type="number"
              value={settings.security.passwordExpiryDays}
              onChange={(e) => handleChange('security', 'passwordExpiryDays', parseInt(e.target.value))}
              fullWidth
            />
          </Grid>
          <Grid item xs={12}>
            <Typography variant="subtitle2" gutterBottom>
              IP Whitelist
            </Typography>
            <Box sx={{ mb: 2 }}>
              {settings.security.ipWhitelist.map((ip, index) => (
                <Chip
                  key={index}
                  label={ip}
                  onDelete={() => {
                    const newList = [...settings.security.ipWhitelist];
                    newList.splice(index, 1);
                    handleChange('security', 'ipWhitelist', newList);
                  }}
                  sx={{ mr: 1, mb: 1 }}
                />
              ))}
              <Button
                size="small"
                startIcon={<AddIcon />}
                onClick={() => {
                  const ip = prompt('Enter IP address:');
                  if (ip) {
                    handleChange('security', 'ipWhitelist', [...settings.security.ipWhitelist, ip]);
                  }
                }}
              >
                Add IP
              </Button>
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
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

      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Settings
        </Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={() => handleSaveSettings(
            ['general', 'email', 'notifications', 'payment', 'security'][activeTab],
            settings[['general', 'email', 'notifications', 'payment', 'security'][activeTab]]
          )}
          startIcon={loading ? <CircularProgress size={20} /> : <SaveIcon />}
          disabled={loading}
        >
          Save Changes
        </Button>
      </Box>

      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={activeTab}
          onChange={(e, newValue) => setActiveTab(newValue)}
          variant="scrollable"
          scrollButtons="auto"
        >
          <Tab icon={<SettingsIcon />} label="General" />
          <Tab icon={<EmailIcon />} label="Email" />
          <Tab icon={<NotificationsIcon />} label="Notifications" />
          <Tab icon={<PaymentIcon />} label="Payment" />
          <Tab icon={<SecurityIcon />} label="Security" />
        </Tabs>
      </Paper>

      <Box sx={{ mt: 3 }}>
        {activeTab === 0 && renderGeneralSettings()}
        {activeTab === 1 && renderEmailSettings()}
        {activeTab === 2 && renderNotificationSettings()}
        {activeTab === 3 && renderPaymentSettings()}
        {activeTab === 4 && renderSecuritySettings()}
      </Box>
    </Box>
  );
}

export default Settings;
