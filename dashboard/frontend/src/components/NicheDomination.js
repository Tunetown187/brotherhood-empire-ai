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
  CircularProgress,
  IconButton,
} from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import MoneyIcon from '@mui/icons-material/MonetizationOn';
import BusinessIcon from '@mui/icons-material/Business';
import TimelineIcon from '@mui/icons-material/Timeline';

const NicheDomination = () => {
  const [niches, setNiches] = useState([]);
  const [selectedNiche, setSelectedNiche] = useState(null);
  const [dominating, setDominating] = useState(false);
  const [progress, setProgress] = useState({});

  useEffect(() => {
    // Fetch niches from your backend
    fetchNiches();
  }, []);

  const fetchNiches = async () => {
    try {
      const response = await fetch('/api/niches');
      const data = await response.json();
      setNiches(data);
    } catch (error) {
      console.error('Error fetching niches:', error);
    }
  };

  const startDomination = async (nicheId) => {
    setDominating(true);
    try {
      const response = await fetch('/api/dominate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nicheId }),
      });
      const data = await response.json();
      setProgress(data);
    } catch (error) {
      console.error('Error starting domination:', error);
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ mb: 4 }}>
        🚀 Niche Domination Dashboard
      </Typography>

      <Grid container spacing={3}>
        {Object.entries(niches).map(([id, niche]) => (
          <Grid item xs={12} sm={6} md={4} key={id}>
            <Card 
              sx={{ 
                height: '100%',
                cursor: 'pointer',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'scale(1.02)',
                  boxShadow: 6,
                }
              }}
              onClick={() => setSelectedNiche(id)}
            >
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  {niche.name}
                </Typography>
                
                <Box sx={{ mt: 2, display: 'flex', alignItems: 'center' }}>
                  <MoneyIcon sx={{ mr: 1 }} />
                  <Typography variant="body1">
                    Profit Potential: {niche.profit_potential}
                  </Typography>
                </Box>

                <Box sx={{ mt: 1, display: 'flex', alignItems: 'center' }}>
                  <BusinessIcon sx={{ mr: 1 }} />
                  <Typography variant="body1">
                    Sub-niches: {niche.sub_niches_count}
                  </Typography>
                </Box>

                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<PlayArrowIcon />}
                  sx={{ mt: 2 }}
                  onClick={(e) => {
                    e.stopPropagation();
                    startDomination(id);
                  }}
                >
                  Dominate This Niche
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {selectedNiche && (
        <Dialog 
          open={true} 
          onClose={() => setSelectedNiche(null)}
          maxWidth="md"
          fullWidth
        >
          <DialogTitle>
            <Typography variant="h5">
              {niches[selectedNiche]?.name} Domination Plan
            </Typography>
          </DialogTitle>
          <DialogContent>
            {dominating ? (
              <Box sx={{ textAlign: 'center', py: 3 }}>
                <CircularProgress size={60} />
                <Typography variant="h6" sx={{ mt: 2 }}>
                  AI Army Taking Over The Market...
                </Typography>
                <Typography variant="body1" sx={{ mt: 1 }}>
                  {progress.status}
                </Typography>
              </Box>
            ) : (
              <Box>
                <Typography variant="h6" gutterBottom>
                  Market Domination Strategy:
                </Typography>
                {/* Add strategy details here */}
              </Box>
            )}
          </DialogContent>
        </Dialog>
      )}
    </Box>
  );
};

export default NicheDomination;
