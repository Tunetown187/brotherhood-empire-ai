import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  Alert,
} from '@mui/material';
import { PhoneInTalk, Stop, Assessment } from '@mui/icons-material';
import axios from 'axios';

const AICaller = () => {
  const [customerProfile, setCustomerProfile] = useState({
    id: '',
    name: '',
    company: '',
    industry: '',
    email: '',
    phone: '',
    notes: ''
  });
  
  const [objective, setObjective] = useState('');
  const [currentScript, setCurrentScript] = useState(null);
  const [callInProgress, setCallInProgress] = useState(false);
  const [callLog, setCallLog] = useState(null);
  const [showScriptDialog, setShowScriptDialog] = useState(false);
  const [showAnalyticsDialog, setShowAnalyticsDialog] = useState(false);
  const [callPatterns, setCallPatterns] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGenerateScript = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await axios.post('/api/call-scripts', {
        customer_profile: customerProfile,
        objective
      });
      setCurrentScript(response.data);
      setShowScriptDialog(true);
    } catch (err) {
      setError('Failed to generate call script: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleStartCall = async () => {
    if (!currentScript) {
      setError('Please generate a call script first');
      return;
    }

    try {
      setLoading(true);
      setError('');
      setCallInProgress(true);
      const response = await axios.post('/api/make-call', {
        script: currentScript,
        customer_profile: customerProfile
      });
      setCallLog(response.data);
    } catch (err) {
      setError('Call failed: ' + err.message);
    } finally {
      setCallInProgress(false);
      setLoading(false);
    }
  };

  const handleEndCall = () => {
    setCallInProgress(false);
  };

  const handleViewAnalytics = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await axios.get('/api/call-patterns');
      setCallPatterns(response.data);
      setShowAnalyticsDialog(true);
    } catch (err) {
      setError('Failed to load analytics: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        AI Sales Caller
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Customer Profile
          </Typography>
          
          <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(2, 1fr)' }}>
            <TextField
              label="Name"
              value={customerProfile.name}
              onChange={(e) => setCustomerProfile({ ...customerProfile, name: e.target.value })}
              fullWidth
            />
            <TextField
              label="Company"
              value={customerProfile.company}
              onChange={(e) => setCustomerProfile({ ...customerProfile, company: e.target.value })}
              fullWidth
            />
            <TextField
              label="Industry"
              value={customerProfile.industry}
              onChange={(e) => setCustomerProfile({ ...customerProfile, industry: e.target.value })}
              fullWidth
            />
            <TextField
              label="Email"
              value={customerProfile.email}
              onChange={(e) => setCustomerProfile({ ...customerProfile, email: e.target.value })}
              fullWidth
            />
            <TextField
              label="Phone"
              value={customerProfile.phone}
              onChange={(e) => setCustomerProfile({ ...customerProfile, phone: e.target.value })}
              fullWidth
            />
          </Box>

          <TextField
            label="Call Objective"
            value={objective}
            onChange={(e) => setObjective(e.target.value)}
            fullWidth
            multiline
            rows={2}
            sx={{ mt: 2 }}
          />
        </CardContent>
      </Card>

      <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
        <Button
          variant="contained"
          onClick={handleGenerateScript}
          disabled={loading || !customerProfile.name || !objective}
        >
          Generate Script
        </Button>
        <Button
          variant="contained"
          color="success"
          startIcon={<PhoneInTalk />}
          onClick={handleStartCall}
          disabled={loading || callInProgress || !currentScript}
        >
          Start Call
        </Button>
        <Button
          variant="contained"
          color="error"
          startIcon={<Stop />}
          onClick={handleEndCall}
          disabled={!callInProgress}
        >
          End Call
        </Button>
        <Button
          variant="contained"
          color="info"
          startIcon={<Assessment />}
          onClick={handleViewAnalytics}
          disabled={loading}
        >
          View Analytics
        </Button>
      </Box>

      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 3 }}>
          <CircularProgress />
        </Box>
      )}

      {/* Script Dialog */}
      <Dialog
        open={showScriptDialog}
        onClose={() => setShowScriptDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Call Script</DialogTitle>
        <DialogContent>
          {currentScript && (
            <Box>
              <Typography variant="subtitle1" gutterBottom>
                Objective: {currentScript.objective}
              </Typography>
              
              <Typography variant="h6" sx={{ mt: 2 }}>
                Key Points
              </Typography>
              <List>
                {currentScript.key_points.map((point, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={point} />
                  </ListItem>
                ))}
              </List>

              <Typography variant="h6" sx={{ mt: 2 }}>
                Objection Handlers
              </Typography>
              {Object.entries(currentScript.objection_handlers).map(([objection, handler], index) => (
                <Box key={index} sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" color="primary">
                    {objection}
                  </Typography>
                  <Typography variant="body2">{handler}</Typography>
                </Box>
              ))}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowScriptDialog(false)}>Close</Button>
        </DialogActions>
      </Dialog>

      {/* Analytics Dialog */}
      <Dialog
        open={showAnalyticsDialog}
        onClose={() => setShowAnalyticsDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Call Analytics</DialogTitle>
        <DialogContent>
          {callPatterns && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Success Patterns
              </Typography>
              <List>
                {Object.entries(callPatterns).map(([category, insights], index) => (
                  <ListItem key={index}>
                    <ListItemText
                      primary={category}
                      secondary={
                        Array.isArray(insights)
                          ? insights.join(', ')
                          : typeof insights === 'object'
                          ? JSON.stringify(insights, null, 2)
                          : insights
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowAnalyticsDialog(false)}>Close</Button>
        </DialogActions>
      </Dialog>

      {/* Call Log */}
      {callLog && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Call Summary
            </Typography>
            
            <Typography variant="subtitle2" color="primary">
              Duration: {callLog.duration} seconds
            </Typography>
            
            <Typography variant="h6" sx={{ mt: 2 }}>
              Sentiment Analysis
            </Typography>
            <Box sx={{ display: 'flex', gap: 2 }}>
              {Object.entries(callLog.sentiment_analysis).map(([sentiment, score], index) => (
                <Typography key={index} variant="body2">
                  {sentiment}: {(score * 100).toFixed(1)}%
                </Typography>
              ))}
            </Box>

            <Typography variant="h6" sx={{ mt: 2 }}>
              Objections Handled
            </Typography>
            <List>
              {callLog.objections_handled.map((objection, index) => (
                <ListItem key={index}>
                  <ListItemText primary={objection} />
                </ListItem>
              ))}
            </List>

            <Typography variant="h6" sx={{ mt: 2 }}>
              Learning Points
            </Typography>
            <List>
              {callLog.learning_points.map((point, index) => (
                <ListItem key={index}>
                  <ListItemText primary={point} />
                </ListItem>
              ))}
            </List>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default AICaller;
