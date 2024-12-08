import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Typography,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Grid,
  Card,
  CardContent,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Tabs,
  Tab,
  Alert,
  Snackbar,
  CircularProgress,
  Chip,
  Divider,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Send as SendIcon,
  FileCopy as FileCopyIcon,
  CloudUpload as CloudUploadIcon,
} from '@mui/icons-material';
import { Editor } from '@tinymce/tinymce-react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const TEMPLATE_CATEGORIES = [
  'Onboarding',
  'Meetings',
  'Billing',
  'Project Management',
  'Sales',
  'Marketing',
  'Support',
  'General',
];

function EmailManagement() {
  const [activeTab, setActiveTab] = useState(0);
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [openTemplateDialog, setOpenTemplateDialog] = useState(false);
  const [openBulkEmailDialog, setOpenBulkEmailDialog] = useState(false);
  const [bulkEmailJobs, setBulkEmailJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const fileInputRef = useRef();

  const [templateForm, setTemplateForm] = useState({
    name: '',
    subject: '',
    body: '',
    category: 'General',
    variables: [],
  });

  const [bulkEmailForm, setbulkEmailForm] = useState({
    templateId: '',
    csvFile: null,
  });

  useEffect(() => {
    fetchTemplates();
    fetchBulkEmailJobs();
  }, []);

  const fetchTemplates = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/email/templates`);
      setTemplates(response.data);
    } catch (error) {
      console.error('Error fetching templates:', error);
      setError('Failed to fetch email templates');
    }
  };

  const fetchBulkEmailJobs = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/email/bulk`);
      setBulkEmailJobs(response.data);
    } catch (error) {
      console.error('Error fetching bulk email jobs:', error);
    }
  };

  const handleCreateTemplate = async () => {
    try {
      setLoading(true);
      await axios.post(`${API_BASE_URL}/email/templates`, templateForm);
      setSuccess('Template created successfully');
      setOpenTemplateDialog(false);
      fetchTemplates();
      resetTemplateForm();
    } catch (error) {
      console.error('Error creating template:', error);
      setError('Failed to create template');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateTemplate = async () => {
    try {
      setLoading(true);
      await axios.put(`${API_BASE_URL}/email/templates/${selectedTemplate.id}`, templateForm);
      setSuccess('Template updated successfully');
      setOpenTemplateDialog(false);
      fetchTemplates();
      resetTemplateForm();
    } catch (error) {
      console.error('Error updating template:', error);
      setError('Failed to update template');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTemplate = async (templateId) => {
    if (!window.confirm('Are you sure you want to delete this template?')) return;
    
    try {
      setLoading(true);
      await axios.delete(`${API_BASE_URL}/email/templates/${templateId}`);
      setSuccess('Template deleted successfully');
      fetchTemplates();
    } catch (error) {
      console.error('Error deleting template:', error);
      setError('Failed to delete template');
    } finally {
      setLoading(false);
    }
  };

  const handleBulkEmail = async () => {
    try {
      setLoading(true);
      const formData = new FormData();
      formData.append('template_id', bulkEmailForm.templateId);
      formData.append('csv_file', bulkEmailForm.csvFile);

      const response = await axios.post(`${API_BASE_URL}/email/bulk`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setSuccess('Bulk email job created successfully');
      setOpenBulkEmailDialog(false);
      fetchBulkEmailJobs();
      resetBulkEmailForm();
    } catch (error) {
      console.error('Error creating bulk email job:', error);
      setError('Failed to create bulk email job');
    } finally {
      setLoading(false);
    }
  };

  const resetTemplateForm = () => {
    setTemplateForm({
      name: '',
      subject: '',
      body: '',
      category: 'General',
      variables: [],
    });
    setSelectedTemplate(null);
  };

  const resetBulkEmailForm = () => {
    setbulkEmailForm({
      templateId: '',
      csvFile: null,
    });
  };

  const handleEditTemplate = (template) => {
    setSelectedTemplate(template);
    setTemplateForm({
      name: template.name,
      subject: template.subject,
      body: template.body,
      category: template.category,
      variables: template.variables,
    });
    setOpenTemplateDialog(true);
  };

  const handleAddVariable = () => {
    const variable = prompt('Enter variable name:');
    if (variable) {
      setTemplateForm(prev => ({
        ...prev,
        variables: [...prev.variables, variable],
      }));
    }
  };

  const renderTemplatesTab = () => (
    <Box>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between' }}>
        <Typography variant="h6">Email Templates</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={() => {
            resetTemplateForm();
            setOpenTemplateDialog(true);
          }}
        >
          Create Template
        </Button>
      </Box>

      <Grid container spacing={3}>
        {templates.map((template) => (
          <Grid item xs={12} md={6} key={template.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {template.name}
                </Typography>
                <Typography variant="body2" color="textSecondary" gutterBottom>
                  Category: {template.category}
                </Typography>
                <Typography variant="body2" color="textSecondary" gutterBottom>
                  Subject: {template.subject}
                </Typography>
                <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Variables:
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {template.variables.map((variable, index) => (
                      <Chip key={index} label={variable} size="small" />
                    ))}
                  </Box>
                </Box>
                <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
                  <IconButton onClick={() => handleEditTemplate(template)}>
                    <EditIcon />
                  </IconButton>
                  <IconButton onClick={() => handleDeleteTemplate(template.id)}>
                    <DeleteIcon />
                  </IconButton>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Dialog
        open={openTemplateDialog}
        onClose={() => setOpenTemplateDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {selectedTemplate ? 'Edit Template' : 'Create Template'}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TextField
                label="Template Name"
                value={templateForm.name}
                onChange={(e) => setTemplateForm(prev => ({ ...prev, name: e.target.value }))}
                fullWidth
                margin="normal"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth margin="normal">
                <InputLabel>Category</InputLabel>
                <Select
                  value={templateForm.category}
                  onChange={(e) => setTemplateForm(prev => ({ ...prev, category: e.target.value }))}
                >
                  {TEMPLATE_CATEGORIES.map((category) => (
                    <MenuItem key={category} value={category}>
                      {category}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Subject"
                value={templateForm.subject}
                onChange={(e) => setTemplateForm(prev => ({ ...prev, subject: e.target.value }))}
                fullWidth
                margin="normal"
              />
            </Grid>
            <Grid item xs={12}>
              <Typography variant="subtitle2" gutterBottom>
                Template Variables:
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                {templateForm.variables.map((variable, index) => (
                  <Chip
                    key={index}
                    label={variable}
                    onDelete={() => {
                      const newVariables = [...templateForm.variables];
                      newVariables.splice(index, 1);
                      setTemplateForm(prev => ({ ...prev, variables: newVariables }));
                    }}
                  />
                ))}
                <Button
                  size="small"
                  startIcon={<AddIcon />}
                  onClick={handleAddVariable}
                >
                  Add Variable
                </Button>
              </Box>
            </Grid>
            <Grid item xs={12}>
              <Typography variant="subtitle2" gutterBottom>
                Email Body:
              </Typography>
              <Editor
                apiKey="your-tinymce-api-key"
                value={templateForm.body}
                init={{
                  height: 400,
                  menubar: true,
                  plugins: [
                    'advlist', 'autolink', 'lists', 'link', 'image', 'charmap', 'preview',
                    'anchor', 'searchreplace', 'visualblocks', 'code', 'fullscreen',
                    'insertdatetime', 'media', 'table', 'code', 'help', 'wordcount'
                  ],
                  toolbar: 'undo redo | blocks | ' +
                    'bold italic forecolor | alignleft aligncenter ' +
                    'alignright alignjustify | bullist numlist outdent indent | ' +
                    'removeformat | help',
                }}
                onEditorChange={(content) => setTemplateForm(prev => ({ ...prev, body: content }))}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenTemplateDialog(false)}>Cancel</Button>
          <Button
            onClick={selectedTemplate ? handleUpdateTemplate : handleCreateTemplate}
            variant="contained"
            color="primary"
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : selectedTemplate ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );

  const renderBulkEmailTab = () => (
    <Box>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between' }}>
        <Typography variant="h6">Bulk Email</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<CloudUploadIcon />}
          onClick={() => setOpenBulkEmailDialog(true)}
        >
          New Bulk Email
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Template</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Total Emails</TableCell>
              <TableCell>Sent</TableCell>
              <TableCell>Failed</TableCell>
              <TableCell>Created At</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {bulkEmailJobs.map((job) => (
              <TableRow key={job.id}>
                <TableCell>
                  {templates.find(t => t.id === job.template_id)?.name || 'Unknown Template'}
                </TableCell>
                <TableCell>
                  <Chip
                    label={job.status}
                    color={
                      job.status === 'completed' ? 'success' :
                      job.status === 'failed' ? 'error' :
                      'warning'
                    }
                    size="small"
                  />
                </TableCell>
                <TableCell>{job.total_emails}</TableCell>
                <TableCell>{job.sent_emails}</TableCell>
                <TableCell>{job.failed_emails}</TableCell>
                <TableCell>{new Date(job.created_at).toLocaleString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog
        open={openBulkEmailDialog}
        onClose={() => setOpenBulkEmailDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>New Bulk Email</DialogTitle>
        <DialogContent>
          <FormControl fullWidth margin="normal">
            <InputLabel>Email Template</InputLabel>
            <Select
              value={bulkEmailForm.templateId}
              onChange={(e) => setbulkEmailForm(prev => ({ ...prev, templateId: e.target.value }))}
            >
              {templates.map((template) => (
                <MenuItem key={template.id} value={template.id}>
                  {template.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <Box sx={{ mt: 3 }}>
            <input
              type="file"
              accept=".csv"
              ref={fileInputRef}
              style={{ display: 'none' }}
              onChange={(e) => setbulkEmailForm(prev => ({ ...prev, csvFile: e.target.files[0] }))}
            />
            <Button
              variant="outlined"
              startIcon={<CloudUploadIcon />}
              onClick={() => fileInputRef.current.click()}
              fullWidth
            >
              Upload CSV File
            </Button>
            {bulkEmailForm.csvFile && (
              <Typography variant="body2" sx={{ mt: 1 }}>
                Selected file: {bulkEmailForm.csvFile.name}
              </Typography>
            )}
          </Box>

          <Alert severity="info" sx={{ mt: 2 }}>
            CSV file should contain the following columns: email, first_name, and any other variables used in the selected template.
          </Alert>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenBulkEmailDialog(false)}>Cancel</Button>
          <Button
            onClick={handleBulkEmail}
            variant="contained"
            color="primary"
            disabled={loading || !bulkEmailForm.templateId || !bulkEmailForm.csvFile}
          >
            {loading ? <CircularProgress size={24} /> : 'Send Emails'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
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

      <Typography variant="h4" gutterBottom>
        Email Management
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
          <Tab label="Templates" />
          <Tab label="Bulk Email" />
        </Tabs>
      </Box>

      {activeTab === 0 && renderTemplatesTab()}
      {activeTab === 1 && renderBulkEmailTab()}
    </Box>
  );
}

export default EmailManagement;
