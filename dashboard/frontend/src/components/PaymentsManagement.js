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
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material';
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  Refresh as RefreshIcon,
  Send as SendIcon,
  Receipt as ReceiptIcon,
  Payment as PaymentIcon,
  AttachMoney as MoneyIcon,
  Download as DownloadIcon,
} from '@mui/icons-material';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

function PaymentsManagement() {
  const [invoices, setInvoices] = useState([]);
  const [payments, setPayments] = useState([]);
  const [clients, setClients] = useState([]);
  const [openInvoice, setOpenInvoice] = useState(false);
  const [openPayment, setOpenPayment] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const [newInvoice, setNewInvoice] = useState({
    client_id: '',
    items: [{ description: '', amount: '', quantity: 1 }],
    due_date: '',
    notes: '',
  });

  const [newPayment, setNewPayment] = useState({
    invoice_id: '',
    amount: '',
    payment_method: '',
    payment_date: new Date().toISOString().split('T')[0],
    notes: '',
  });

  useEffect(() => {
    fetchInvoices();
    fetchPayments();
    fetchClients();
  }, []);

  const fetchInvoices = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/invoices`);
      setInvoices(response.data);
    } catch (error) {
      console.error('Error fetching invoices:', error);
      setError('Failed to fetch invoices');
    }
  };

  const fetchPayments = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/payments`);
      setPayments(response.data);
    } catch (error) {
      console.error('Error fetching payments:', error);
      setError('Failed to fetch payments');
    }
  };

  const fetchClients = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/clients`);
      setClients(response.data);
    } catch (error) {
      console.error('Error fetching clients:', error);
      setError('Failed to fetch clients');
    }
  };

  const handleCreateInvoice = async () => {
    try {
      setLoading(true);
      await axios.post(`${API_BASE_URL}/invoices`, newInvoice);
      setSuccess('Invoice created successfully');
      setOpenInvoice(false);
      setNewInvoice({
        client_id: '',
        items: [{ description: '', amount: '', quantity: 1 }],
        due_date: '',
        notes: '',
      });
      fetchInvoices();
    } catch (error) {
      console.error('Error creating invoice:', error);
      setError('Failed to create invoice');
    } finally {
      setLoading(false);
    }
  };

  const handleRecordPayment = async () => {
    try {
      setLoading(true);
      await axios.post(`${API_BASE_URL}/payments`, newPayment);
      setSuccess('Payment recorded successfully');
      setOpenPayment(false);
      setNewPayment({
        invoice_id: '',
        amount: '',
        payment_method: '',
        payment_date: new Date().toISOString().split('T')[0],
        notes: '',
      });
      fetchPayments();
      fetchInvoices();
    } catch (error) {
      console.error('Error recording payment:', error);
      setError('Failed to record payment');
    } finally {
      setLoading(false);
    }
  };

  const handleAddInvoiceItem = () => {
    setNewInvoice({
      ...newInvoice,
      items: [...newInvoice.items, { description: '', amount: '', quantity: 1 }],
    });
  };

  const handleRemoveInvoiceItem = (index) => {
    const items = [...newInvoice.items];
    items.splice(index, 1);
    setNewInvoice({ ...newInvoice, items });
  };

  const calculateInvoiceTotal = (items) => {
    return items.reduce((total, item) => total + (parseFloat(item.amount) || 0) * (parseInt(item.quantity) || 1), 0);
  };

  const getInvoiceStatus = (invoice) => {
    const total = calculateInvoiceTotal(invoice.items);
    const paid = payments
      .filter(p => p.invoice_id === invoice.id)
      .reduce((sum, p) => sum + parseFloat(p.amount), 0);

    if (paid >= total) return 'paid';
    if (paid > 0) return 'partial';
    if (new Date(invoice.due_date) < new Date()) return 'overdue';
    return 'pending';
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'paid': return 'success';
      case 'partial': return 'warning';
      case 'overdue': return 'error';
      default: return 'default';
    }
  };

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
          Invoices & Payments
        </Typography>
        <Box>
          <Button
            variant="contained"
            color="primary"
            onClick={() => setOpenInvoice(true)}
            startIcon={<ReceiptIcon />}
            sx={{ mr: 2 }}
          >
            Create Invoice
          </Button>
          <Button
            variant="contained"
            color="primary"
            onClick={() => setOpenPayment(true)}
            startIcon={<PaymentIcon />}
          >
            Record Payment
          </Button>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* Invoices */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Invoices
              </Typography>
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Invoice #</TableCell>
                      <TableCell>Client</TableCell>
                      <TableCell>Date</TableCell>
                      <TableCell>Due Date</TableCell>
                      <TableCell align="right">Amount</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {invoices.map((invoice) => {
                      const status = getInvoiceStatus(invoice);
                      return (
                        <TableRow key={invoice.id}>
                          <TableCell>{invoice.id}</TableCell>
                          <TableCell>
                            {clients.find(c => c.id === invoice.client_id)?.name || 'Unknown'}
                          </TableCell>
                          <TableCell>{new Date(invoice.created_at).toLocaleDateString()}</TableCell>
                          <TableCell>{new Date(invoice.due_date).toLocaleDateString()}</TableCell>
                          <TableCell align="right">
                            ${calculateInvoiceTotal(invoice.items).toFixed(2)}
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={status.toUpperCase()}
                              color={getStatusColor(status)}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            <IconButton
                              onClick={() => window.open(`${API_BASE_URL}/invoices/${invoice.id}/pdf`)}
                            >
                              <DownloadIcon />
                            </IconButton>
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Payments */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Payments
              </Typography>
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Date</TableCell>
                      <TableCell>Invoice #</TableCell>
                      <TableCell>Client</TableCell>
                      <TableCell>Method</TableCell>
                      <TableCell align="right">Amount</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {payments.map((payment) => {
                      const invoice = invoices.find(i => i.id === payment.invoice_id);
                      return (
                        <TableRow key={payment.id}>
                          <TableCell>{new Date(payment.payment_date).toLocaleDateString()}</TableCell>
                          <TableCell>{payment.invoice_id}</TableCell>
                          <TableCell>
                            {clients.find(c => c.id === invoice?.client_id)?.name || 'Unknown'}
                          </TableCell>
                          <TableCell>{payment.payment_method}</TableCell>
                          <TableCell align="right">${parseFloat(payment.amount).toFixed(2)}</TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Create Invoice Dialog */}
      <Dialog
        open={openInvoice}
        onClose={() => setOpenInvoice(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Create Invoice</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <FormControl fullWidth>
              <InputLabel>Client</InputLabel>
              <Select
                value={newInvoice.client_id}
                onChange={(e) => setNewInvoice({ ...newInvoice, client_id: e.target.value })}
              >
                {clients.map((client) => (
                  <MenuItem key={client.id} value={client.id}>
                    {client.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <Typography variant="subtitle1">Items</Typography>
            {newInvoice.items.map((item, index) => (
              <Box key={index} sx={{ display: 'flex', gap: 2, alignItems: 'flex-start' }}>
                <TextField
                  label="Description"
                  value={item.description}
                  onChange={(e) => {
                    const items = [...newInvoice.items];
                    items[index].description = e.target.value;
                    setNewInvoice({ ...newInvoice, items });
                  }}
                  fullWidth
                />
                <TextField
                  label="Amount"
                  type="number"
                  value={item.amount}
                  onChange={(e) => {
                    const items = [...newInvoice.items];
                    items[index].amount = e.target.value;
                    setNewInvoice({ ...newInvoice, items });
                  }}
                  sx={{ width: 150 }}
                />
                <TextField
                  label="Quantity"
                  type="number"
                  value={item.quantity}
                  onChange={(e) => {
                    const items = [...newInvoice.items];
                    items[index].quantity = e.target.value;
                    setNewInvoice({ ...newInvoice, items });
                  }}
                  sx={{ width: 100 }}
                />
                <IconButton
                  onClick={() => handleRemoveInvoiceItem(index)}
                  disabled={newInvoice.items.length === 1}
                >
                  <DeleteIcon />
                </IconButton>
              </Box>
            ))}

            <Button
              startIcon={<AddIcon />}
              onClick={handleAddInvoiceItem}
              sx={{ alignSelf: 'flex-start' }}
            >
              Add Item
            </Button>

            <TextField
              label="Due Date"
              type="date"
              value={newInvoice.due_date}
              onChange={(e) => setNewInvoice({ ...newInvoice, due_date: e.target.value })}
              InputLabelProps={{ shrink: true }}
              fullWidth
            />

            <TextField
              label="Notes"
              value={newInvoice.notes}
              onChange={(e) => setNewInvoice({ ...newInvoice, notes: e.target.value })}
              multiline
              rows={3}
              fullWidth
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenInvoice(false)}>Cancel</Button>
          <Button
            onClick={handleCreateInvoice}
            variant="contained"
            color="primary"
            disabled={loading}
            startIcon={loading ? <CircularProgress size={20} /> : <ReceiptIcon />}
          >
            Create
          </Button>
        </DialogActions>
      </Dialog>

      {/* Record Payment Dialog */}
      <Dialog
        open={openPayment}
        onClose={() => setOpenPayment(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Record Payment</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <FormControl fullWidth>
              <InputLabel>Invoice</InputLabel>
              <Select
                value={newPayment.invoice_id}
                onChange={(e) => setNewPayment({ ...newPayment, invoice_id: e.target.value })}
              >
                {invoices
                  .filter(invoice => getInvoiceStatus(invoice) !== 'paid')
                  .map((invoice) => (
                    <MenuItem key={invoice.id} value={invoice.id}>
                      #{invoice.id} - {clients.find(c => c.id === invoice.client_id)?.name}
                    </MenuItem>
                  ))}
              </Select>
            </FormControl>

            <TextField
              label="Amount"
              type="number"
              value={newPayment.amount}
              onChange={(e) => setNewPayment({ ...newPayment, amount: e.target.value })}
              fullWidth
              required
            />

            <FormControl fullWidth>
              <InputLabel>Payment Method</InputLabel>
              <Select
                value={newPayment.payment_method}
                onChange={(e) => setNewPayment({ ...newPayment, payment_method: e.target.value })}
              >
                <MenuItem value="credit_card">Credit Card</MenuItem>
                <MenuItem value="bank_transfer">Bank Transfer</MenuItem>
                <MenuItem value="cash">Cash</MenuItem>
                <MenuItem value="check">Check</MenuItem>
                <MenuItem value="other">Other</MenuItem>
              </Select>
            </FormControl>

            <TextField
              label="Payment Date"
              type="date"
              value={newPayment.payment_date}
              onChange={(e) => setNewPayment({ ...newPayment, payment_date: e.target.value })}
              InputLabelProps={{ shrink: true }}
              fullWidth
            />

            <TextField
              label="Notes"
              value={newPayment.notes}
              onChange={(e) => setNewPayment({ ...newPayment, notes: e.target.value })}
              multiline
              rows={3}
              fullWidth
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenPayment(false)}>Cancel</Button>
          <Button
            onClick={handleRecordPayment}
            variant="contained"
            color="primary"
            disabled={loading}
            startIcon={loading ? <CircularProgress size={20} /> : <PaymentIcon />}
          >
            Record
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default PaymentsManagement;
