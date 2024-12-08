# Agency Swarm Dashboard

A user-friendly dashboard for managing your AI agents and business automation tasks.

## Features

- Visual configuration of AI agents
- Email management integration
- Invoice and payment processing
- Document generation and management
- Real-time agent communication monitoring

## Getting Started

### Backend Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
.\venv\Scripts\activate
```

2. Install backend dependencies:
```bash
cd dashboard
pip install -r requirements.txt
```

3. Start the backend server:
```bash
cd backend
uvicorn main:app --reload
```

### Frontend Setup

1. Install frontend dependencies:
```bash
cd dashboard/frontend
npm install
```

2. Start the frontend development server:
```bash
npm start
```

The dashboard will be available at http://localhost:3015

## Usage

1. Create New Agents:
   - Click "Create New Agent" button
   - Fill in the agent's name, description, and instructions
   - Select the tools the agent should have access to
   - Click "Create" to save the agent

2. Configure Email Settings:
   - Navigate to Email Management
   - Enter your SMTP server details
   - Save the configuration

3. Setup Payment Processing:
   - Go to Invoices & Payments
   - Enter your Stripe API keys
   - Configure webhook settings

4. Monitor Agent Activities:
   - View agent communications in real-time
   - Track task completion status
   - Review generated documents and sent emails

## Security Notes

- Store sensitive information (API keys, passwords) in environment variables
- Regularly review agent permissions and access
- Monitor agent activities for any unusual behavior
