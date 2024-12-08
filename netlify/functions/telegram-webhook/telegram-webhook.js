const axios = require('axios');

// Empire configuration
const token = process.env.TELEGRAM_BOT_TOKEN || '7838814763:AAGVkweVaww77zuWb6lUz4Fg6Xm5yiiEido';
const TELEGRAM_API = `https://api.telegram.org/bot${token}`;
const GHL_API_KEY = process.env.GHL_API_KEY;
const MAKE_WEBHOOK_URL = process.env.MAKE_WEBHOOK_URL;
const REPLIT_API_KEY = process.env.REPLIT_API_KEY;

// Agent ranks and roles
const AGENT_RANKS = {
  GENERAL: 'general',       // Top-level command
  COLONEL: 'colonel',       // Regional command
  MAJOR: 'major',          // City-level command
  CAPTAIN: 'captain',      // District command
  LIEUTENANT: 'lieutenant', // Local business operations
  SERGEANT: 'sergeant'      // Field operations
};

// Agent specializations
const AGENT_ROLES = {
  STRATEGIST: 'strategist',       // Plans conquest strategies
  INFILTRATOR: 'infiltrator',     // Gains access to businesses
  NEGOTIATOR: 'negotiator',       // Handles business dealings
  INTELLIGENCE: 'intelligence',    // Gathers market data
  OPERATOR: 'operator',           // Executes operations
  RECRUITER: 'recruiter'          // Expands the network
};

// Helper function to send messages
async function sendTelegramMessage(chatId, text, parse_mode = 'Markdown') {
  try {
    const response = await axios.post(`${TELEGRAM_API}/sendMessage`, {
      chat_id: chatId,
      text: text,
      parse_mode: parse_mode
    });
    console.log('Message sent successfully:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error sending message:', error.response?.data || error.message);
    throw error;
  }
}

// GHL Helper Functions
async function createGHLContact(name, rank, role, territory) {
  if (!GHL_API_KEY) {
    throw new Error('GHL_API_KEY not configured');
  }
  try {
    const response = await axios.post('https://rest.gohighlevel.com/v1/contacts/', {
      name: name,
      custom_fields: [
        { id: 'rank', value: rank },
        { id: 'role', value: role },
        { id: 'territory', value: territory }
      ]
    }, {
      headers: { 'Authorization': `Bearer ${GHL_API_KEY}` }
    });
    return response.data;
  } catch (error) {
    console.error('Error creating GHL contact:', error);
    throw error;
  }
}

// Make.com Helper Functions
async function triggerMakeWorkflow(eventType, data) {
  if (!MAKE_WEBHOOK_URL) {
    throw new Error('MAKE_WEBHOOK_URL not configured');
  }
  try {
    const response = await axios.post(MAKE_WEBHOOK_URL, {
      eventType,
      data
    });
    return response.data;
  } catch (error) {
    console.error('Error triggering Make workflow:', error);
    throw error;
  }
}

// Deploy agent to Replit with military-grade code
async function deployAgentToReplit(name, rank, role, territory) {
  if (!REPLIT_API_KEY) {
    throw new Error('REPLIT_API_KEY not configured');
  }
  try {
    const agentCode = `
# Brotherhood Empire Agent
# Codename: ${name}
# Rank: ${rank}
# Role: ${role}
# Territory: ${territory}

import os
import requests
import json
from datetime import datetime

class BrotherhoodAgent:
    def __init__(self):
        self.name = "${name}"
        self.rank = "${rank}"
        self.role = "${role}"
        self.territory = "${territory}"
        self.mission_log = []
        
    def execute_command(self, command, params=None):
        """Execute commands from high command"""
        print(f"[{self.rank.upper()}] {self.name} executing: {command}")
        
        if command == "analyze_territory":
            return self.analyze_territory()
        elif command == "infiltrate_business":
            return self.infiltrate_business(params['business_name'])
        elif command == "gather_intelligence":
            return self.gather_intelligence(params['target'])
        elif command == "report_status":
            return self.report_status()
        else:
            return f"Unknown command: {command}"
    
    def analyze_territory(self):
        """Analyze assigned territory for potential targets"""
        return f"Territory analysis of {self.territory} complete. Ready for further orders."
    
    def infiltrate_business(self, business_name):
        """Begin infiltration of a local business"""
        return f"Initiating infiltration of {business_name} in {self.territory}"
    
    def gather_intelligence(self, target):
        """Gather intelligence on specified target"""
        return f"Intelligence gathered on {target}. Awaiting extraction orders."
    
    def report_status(self):
        """Report current status to high command"""
        return {
            "agent": self.name,
            "rank": self.rank,
            "role": self.role,
            "territory": self.territory,
            "status": "operational",
            "last_update": datetime.now().isoformat()
        }

# Initialize agent
agent = BrotherhoodAgent()

# Start agent operations
print(f"Agent {agent.name} deployed to {agent.territory}")
print(f"Rank: {agent.rank}")
print(f"Role: {agent.role}")
print("Awaiting orders from high command...")
`;

    // Create a new Repl
    const response = await axios.post('https://replit.com/api/v1/repls', {
      name: `agent-${name.toLowerCase()}`,
      language: 'python',
      files: [{
        name: 'main.py',
        content: agentCode
      }]
    }, {
      headers: { 'Authorization': `Bearer ${REPLIT_API_KEY}` }
    });
    return response.data;
  } catch (error) {
    console.error('Error deploying to Replit:', error);
    throw error;
  }
}

// Command handlers
const commandHandlers = {
  '/start': async (chatId) => {
    console.log('Handling /start command for chat:', chatId);
    const message = '🏰 *Welcome to Brotherhood Empire Command Center* 🏰\n\n' +
      'I am your gateway to our global operations. Available commands:\n\n' +
      '/status - View empire status\n' +
      '/deploy_agent [name] [rank] [role] [territory] - Deploy new agent\n' +
      '/command [agent] [order] - Issue orders to agent\n' +
      '/intelligence - View intelligence reports\n' +
      '/territories - View controlled territories\n' +
      '/ranks - View available ranks\n' +
      '/roles - View agent roles\n' +
      '/help - Show this message\n\n' +
      '_"In unity lies our strength, in strategy our victory."_';
    
    await triggerMakeWorkflow('new_commander', { chatId });
    return sendTelegramMessage(chatId, message);
  },

  '/ranks': async (chatId) => {
    const ranks = Object.entries(AGENT_RANKS)
      .map(([key, value]) => `*${value.toUpperCase()}*`)
      .join('\n');
    return sendTelegramMessage(chatId, 
      '⭐ *Available Ranks*\n\n' + ranks + '\n\n' +
      '_Ranked from highest to lowest authority_'
    );
  },

  '/roles': async (chatId) => {
    const roles = Object.entries(AGENT_ROLES)
      .map(([key, value]) => `*${value.toUpperCase()}* - ${getSpecializationDescription(value)}`)
      .join('\n');
    return sendTelegramMessage(chatId, 
      '🎯 *Agent Specializations*\n\n' + roles
    );
  },

  '/deploy_agent': async (chatId, args) => {
    if (args.length < 4) {
      return sendTelegramMessage(chatId, 
        'Usage: /deploy_agent [name] [rank] [role] [territory]\n\n' +
        'Example: /deploy_agent Shadow colonel strategist "New York"\n\n' +
        'Use /ranks and /roles to see available options.'
      );
    }
    
    const [name, rank, role, ...territoryParts] = args;
    const territory = territoryParts.join(' ');
    
    if (!Object.values(AGENT_RANKS).includes(rank.toLowerCase())) {
      return sendTelegramMessage(chatId, '❌ Invalid rank. Use /ranks to see available ranks.');
    }
    
    if (!Object.values(AGENT_ROLES).includes(role.toLowerCase())) {
      return sendTelegramMessage(chatId, '❌ Invalid role. Use /roles to see available roles.');
    }
    
    try {
      // Create GHL contact for agent
      await createGHLContact(name, rank, role, territory);
      
      // Deploy agent to Replit
      const deployment = await deployAgentToReplit(name, rank, role, territory);
      
      // Notify Make.com about new agent
      await triggerMakeWorkflow('agent_deployed', {
        name,
        rank,
        role,
        territory,
        replit_url: deployment.url
      });
      
      return sendTelegramMessage(chatId,
        `✅ *Agent Deployed Successfully*\n\n` +
        `Codename: *${name}*\n` +
        `Rank: *${rank}*\n` +
        `Role: *${role}*\n` +
        `Territory: *${territory}*\n\n` +
        `_Agent is operational and awaiting orders._`
      );
    } catch (error) {
      console.error('Error deploying agent:', error);
      return sendTelegramMessage(chatId, `❌ Deployment failed: ${error.message}`);
    }
  },

  '/command': async (chatId, args) => {
    if (args.length < 2) {
      return sendTelegramMessage(chatId, 
        'Usage: /command [agent] [order] [...params]\n\n' +
        'Available orders:\n' +
        '- analyze_territory\n' +
        '- infiltrate_business [business_name]\n' +
        '- gather_intelligence [target]\n' +
        '- report_status'
      );
    }
    
    const [agent, command, ...params] = args;
    
    try {
      const result = await triggerMakeWorkflow('execute_command', {
        agent,
        command,
        params: params.join(' '),
        chat_id: chatId
      });
      
      return sendTelegramMessage(chatId,
        `📨 *Order Transmitted*\n\n` +
        `Agent: *${agent}*\n` +
        `Command: *${command}*\n` +
        `Parameters: ${params.join(' ') || 'None'}\n\n` +
        `_Awaiting execution report..._`
      );
    } catch (error) {
      console.error('Error sending command:', error);
      return sendTelegramMessage(chatId, `❌ Command failed: ${error.message}`);
    }
  },

  '/status': async (chatId) => {
    try {
      const empireStatus = await triggerMakeWorkflow('get_status', { chatId });
      
      return sendTelegramMessage(chatId,
        `🌐 *Brotherhood Empire Status*\n\n` +
        `Active Agents: *${empireStatus.agents || 0}*\n` +
        `Territories: *${empireStatus.territories || 0}*\n` +
        `Operations: *${empireStatus.operations || 0}*\n` +
        `Success Rate: *${empireStatus.success_rate || '0'}%*\n\n` +
        `System Status:\n` +
        `- Command Center: ✅\n` +
        `- GHL Integration: ${GHL_API_KEY ? '✅' : '❌'}\n` +
        `- Make.com Workflows: ${MAKE_WEBHOOK_URL ? '✅' : '❌'}\n` +
        `- Agent Network: ${REPLIT_API_KEY ? '✅' : '❌'}\n\n` +
        `_"Victory favors the prepared."_`
      );
    } catch (error) {
      console.error('Error getting status:', error);
      return sendTelegramMessage(chatId, `❌ Status report unavailable: ${error.message}`);
    }
  }
};

// Helper function for role descriptions
function getSpecializationDescription(role) {
  const descriptions = {
    'strategist': 'Plans and coordinates empire expansion',
    'infiltrator': 'Specializes in business acquisition',
    'negotiator': 'Handles diplomatic relations and deals',
    'intelligence': 'Gathers and analyzes market data',
    'operator': 'Executes strategic operations',
    'recruiter': 'Expands our network of influence'
  };
  return descriptions[role.toLowerCase()] || role;
}

exports.handler = async function(event, context) {
  console.log('Received webhook event:', event.httpMethod);
  
  if (event.httpMethod !== 'POST') {
    return { 
      statusCode: 405, 
      body: JSON.stringify({ error: 'Method Not Allowed' })
    };
  }

  try {
    const data = JSON.parse(event.body);
    console.log('Received update:', JSON.stringify(data, null, 2));

    if (data.message) {
      const chatId = data.message.chat.id;
      const text = data.message.text;
      const username = data.message.from.username;

      console.log(`Received message: "${text}" from ${username} (${chatId})`);

      if (text && text.startsWith('/')) {
        const parts = text.split(' ');
        const command = parts[0].toLowerCase();
        const args = parts.slice(1);
        
        if (commandHandlers[command]) {
          try {
            await commandHandlers[command](chatId, args);
          } catch (error) {
            console.error('Error executing command:', error);
            await sendTelegramMessage(chatId, '❌ Command failed. High command will investigate.');
          }
        } else {
          await sendTelegramMessage(chatId, 'Unknown command. Use /help for available orders.');
        }
      } else {
        await sendTelegramMessage(chatId, 'Please use proper command format. See /help for instructions.');
      }
    }

    return {
      statusCode: 200,
      body: JSON.stringify({ status: 'ok' })
    };
  } catch (error) {
    console.error('Error processing webhook:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Internal error in command center' })
    };
  }
};
