#!/bin/bash

# Build and deploy the entire crypto ecosystem

# 1. Setup virtual environment
python -m venv venv
source venv/bin/activate  # For Unix
# venv\Scripts\activate  # For Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start all services
docker-compose up -d

# 4. Deploy to cloud platforms
# Vercel
vercel --prod

# Netlify
netlify deploy --prod

# 5. Setup monitoring
python -m automation.telegram_bot &
python -m automation.security_manager &

# 6. Start the master controller
python master_controller.py
