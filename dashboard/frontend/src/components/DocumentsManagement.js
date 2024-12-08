import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemSecondary,
  Chip,
  Divider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Snackbar,
  Alert,
  CircularProgress,
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
  Delete as DeleteIcon,
  Edit as EditIcon,
  Refresh as RefreshIcon,
  CloudUpload as UploadIcon,
  Download as DownloadIcon,
  Folder as FolderIcon,
  Description as FileIcon,
} from '@mui/icons-material';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

function DocumentsManagement() {
  const [documents, setDocuments] = useState([]);
  const [folders, setFolders] = useState([]);
  const [currentFolder, setCurrentFolder] = useState(null);
  const [openUpload, setOpenUpload] = useState(false);
  const [openNewFolder, setOpenNewFolder] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  const [newFolder, setNewFolder] = useState({
    name: '',
    parent_id: null,
  });

  useEffect(() => {
    fetchDocuments();
    fetchFolders();
  }, [currentFolder]);

  const fetchDocuments = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/documents`, {
        params: { folder_id: currentFolder }
      });
      setDocuments(response.data);
    } catch (error) {
      console.error('Error fetching documents:', error);
      setError('Failed to fetch documents');
    }
  };

  const fetchFolders = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/documents/folders`);
      setFolders(response.data);
    } catch (error) {
      console.error('Error fetching folders:', error);
      setError('Failed to fetch folders');
    }
  };

  const handleFileSelect = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    try {
      setLoading(true);
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('folder_id', currentFolder);

      await axios.post(`${API_BASE_URL}/documents/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      setSuccess('Document uploaded successfully');
      setOpenUpload(false);
      setSelectedFile(null);
      fetchDocuments();
    } catch (error) {
      console.error('Error uploading document:', error);
      setError('Failed to upload document');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateFolder = async () => {
    try {
      setLoading(true);
      await axios.post(`${API_BASE_URL}/documents/folders`, {
        ...newFolder,
        parent_id: currentFolder
      });
      setSuccess('Folder created successfully');
      setOpenNewFolder(false);
      setNewFolder({ name: '', parent_id: null });
      fetchFolders();
    } catch (error) {
      console.error('Error creating folder:', error);
      setError('Failed to create folder');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (documentId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/documents/${documentId}/download`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', documents.find(d => d.id === documentId)?.name || 'document');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error downloading document:', error);
      setError('Failed to download document');
    }
  };

  const handleDelete = async (documentId) => {
    try {
      await axios.delete(`${API_BASE_URL}/documents/${documentId}`);
      setSuccess('Document deleted successfully');
      fetchDocuments();
    } catch (error) {
      console.error('Error deleting document:', error);
      setError('Failed to delete document');
    }
  };

  const getBreadcrumbs = () => {
    if (!currentFolder) return [{ id: null, name: 'Root' }];
    
    const breadcrumbs = [{ id: null, name: 'Root' }];
    let current = folders.find(f => f.id === currentFolder);
    
    while (current) {
      breadcrumbs.unshift(current);
      current = folders.find(f => f.id === current.parent_id);
    }
    
    return breadcrumbs;
  };

  const filteredDocuments = documents.filter(doc =>
    doc.name.toLowerCase().includes(searchQuery.toLowerCase())
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
          Documents
        </Typography>
        <Box>
          <Button
            variant="contained"
            color="primary"
            onClick={() => setOpenNewFolder(true)}
            startIcon={<FolderIcon />}
            sx={{ mr: 2 }}
          >
            New Folder
          </Button>
          <Button
            variant="contained"
            color="primary"
            onClick={() => setOpenUpload(true)}
            startIcon={<UploadIcon />}
          >
            Upload Document
          </Button>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* Breadcrumbs and Search */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  {getBreadcrumbs().map((folder, index) => (
                    <React.Fragment key={folder.id}>
                      {index > 0 && <Typography>/</Typography>}
                      <Button
                        onClick={() => setCurrentFolder(folder.id)}
                        color="primary"
                      >
                        {folder.name}
                      </Button>
                    </React.Fragment>
                  ))}
                </Box>
                <TextField
                  placeholder="Search documents..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  size="small"
                  sx={{ width: 300 }}
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Folders */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Folders
              </Typography>
              <Grid container spacing={2}>
                {folders
                  .filter(folder => folder.parent_id === currentFolder)
                  .map((folder) => (
                    <Grid item xs={12} sm={6} md={4} lg={3} key={folder.id}>
                      <Card
                        variant="outlined"
                        sx={{
                          cursor: 'pointer',
                          '&:hover': { bgcolor: 'action.hover' }
                        }}
                        onClick={() => setCurrentFolder(folder.id)}
                      >
                        <CardContent>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <FolderIcon color="primary" />
                            <Typography>{folder.name}</Typography>
                          </Box>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Documents */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Documents
              </Typography>
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Name</TableCell>
                      <TableCell>Type</TableCell>
                      <TableCell>Size</TableCell>
                      <TableCell>Modified</TableCell>
                      <TableCell>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {filteredDocuments.map((doc) => (
                      <TableRow key={doc.id}>
                        <TableCell>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <FileIcon />
                            {doc.name}
                          </Box>
                        </TableCell>
                        <TableCell>{doc.type}</TableCell>
                        <TableCell>{formatFileSize(doc.size)}</TableCell>
                        <TableCell>
                          {new Date(doc.modified_at).toLocaleString()}
                        </TableCell>
                        <TableCell>
                          <IconButton
                            onClick={() => handleDownload(doc.id)}
                            size="small"
                          >
                            <DownloadIcon />
                          </IconButton>
                          <IconButton
                            onClick={() => handleDelete(doc.id)}
                            size="small"
                            color="error"
                          >
                            <DeleteIcon />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Upload Dialog */}
      <Dialog
        open={openUpload}
        onClose={() => setOpenUpload(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Upload Document</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <Button
              variant="outlined"
              component="label"
              startIcon={<UploadIcon />}
            >
              Choose File
              <input
                type="file"
                hidden
                onChange={handleFileSelect}
              />
            </Button>
            {selectedFile && (
              <Typography variant="body2">
                Selected: {selectedFile.name}
              </Typography>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenUpload(false)}>Cancel</Button>
          <Button
            onClick={handleUpload}
            variant="contained"
            color="primary"
            disabled={!selectedFile || loading}
            startIcon={loading ? <CircularProgress size={20} /> : <UploadIcon />}
          >
            Upload
          </Button>
        </DialogActions>
      </Dialog>

      {/* New Folder Dialog */}
      <Dialog
        open={openNewFolder}
        onClose={() => setOpenNewFolder(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Create New Folder</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <TextField
              label="Folder Name"
              value={newFolder.name}
              onChange={(e) => setNewFolder({ ...newFolder, name: e.target.value })}
              fullWidth
              required
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenNewFolder(false)}>Cancel</Button>
          <Button
            onClick={handleCreateFolder}
            variant="contained"
            color="primary"
            disabled={!newFolder.name || loading}
            startIcon={loading ? <CircularProgress size={20} /> : <FolderIcon />}
          >
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

export default DocumentsManagement;
