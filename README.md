# Brotherhood Empire AI Business Management System

An advanced AI-powered system for managing and automating business operations, integrating with various services and APIs to provide comprehensive business automation solutions.

## Features

- 🤖 Multi-AI Integration (Claude-3 & DeepSeek)
- 🚀 Marketing Campaign Automation
- 📊 Market Analysis
- 💼 Business Process Optimization
- 🔄 Workflow Automation
- 📱 Telegram Bot Interface

## Core Components

1. **AI Agents**
   - Marketing Agent
   - Sales Agent
   - Operations Agent
   - Business Strategy Agent

2. **Integrations**
   - GoHighLevel CRM
   - Make.com Automation
   - Telegram Bot API
   - Firebase Database
   - Anthropic Claude-3
   - DeepSeek AI

## Setup Instructions

1. **Environment Setup**
   ```bash
   # Clone the repository
   git clone https://github.com/brotherhood-empire/agency-swarm.git
   cd agency-swarm

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configure API Keys**
   Create a `.env` file with:
   ```env
   ANTHROPIC_API_KEY=your_anthropic_key
   DEEPSEEK_API_KEY=your_deepseek_key
   GHL_API_KEY=your_ghl_key
   TELEGRAM_BOT_TOKEN=your_telegram_token
   MAKE_API_KEY=your_make_key
   ```

3. **Firebase Setup**
   - Create a Firebase project
   - Download credentials and save as `firebase-credentials.json`

4. **Start the System**
   ```bash
   cd ghl-automation/empire_core
   python telegram_handler.py
   ```

## Usage

### Telegram Commands
- `/start` - Initialize the bot
- `/help` - View available commands
- `/campaign [type] [budget]` - Launch marketing campaigns
- `/market [industry] [region]` - Analyze market conditions
- `/workflow [process]` - Optimize business workflows

## Architecture

The system uses a modular architecture with:
- AI Agents for decision making
- Service integrations for execution
- Asynchronous operations for performance
- Multi-model AI for enhanced reliability

## Security

- API keys and credentials are stored securely
- Firebase for secure data storage
- Environment variables for sensitive data
- Proper error handling and logging

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is proprietary software owned by Brotherhood Empire.
All rights reserved.

---

# GitHub Actions Workflow Guide

This project is configured for automated deployment using GitHub Actions. Below are the steps and requirements for successful CI/CD:

## Directory Structure

- `update_requirements.py` — Updates dependencies (placeholder provided)
- `requirements.txt` — Python requirements (ensure this is up to date)
- `master_controller.py` — Entry point for master controller (placeholder provided)
- `main.py` — Entry point for agent logic (placeholder provided)
- `brotherhood-empire-final/` — Directory for deployable site (empty placeholder provided)
- `.github/workflows/deploy.yml` — GitHub Actions workflow file

## GitHub Actions Secrets Required

Set these in your repository Settings > Secrets and variables > Actions:
- `VERCEL_TOKEN`, `ORG_ID`, `PROJECT_ID` (for Vercel deploy)
- `NETLIFY_AUTH_TOKEN`, `NETLIFY_SITE_ID` (for Netlify deploy)
- `TELEGRAM_BOT_TOKEN`, `GHL_API_KEY`, `MAKE_WEBHOOK_URL`, `AWS_ACCESS_KEY`, `AWS_SECRET_KEY`, `STRIPE_SECRET_KEY`, `FIREBASE_ADMIN_KEY`, `OPENAI_API_KEY` (for agent startup)

If a secret is missing, the corresponding step will be skipped (not fail).

## How to Deploy
- Push to the `main` branch or open a PR targeting `main`.
- The workflow will run automatically.

## Next Steps
- Replace the placeholder scripts with your actual logic.
- Add deployable content to `brotherhood-empire-final/`.
- Keep `requirements.txt` up to date.

## 📄 Documentation

This project uses [MkDocs](https://www.mkdocs.org/) for documentation. Docs are published automatically to GitHub Pages on every push to `main` or `master` via the `.github/workflows/docs.yml` workflow.

- To edit documentation, modify the files in the `docs/` directory and push your changes.
- The navigation and site settings are in `mkdocs.yml`.
- The workflow installs dependencies from `requirements_docs.txt`.

**To disable documentation deployment:**
Rename or delete `.github/workflows/docs.yml`.

---

For further help, edit this README or contact your project maintainer.
