#!/bin/bash

# Create new site
SITE_ID=$(curl -X POST "https://api.netlify.com/api/v1/sites" \
  -H "Authorization: Bearer nfp_WNL31hXmMCt3xAwvpdFcQfHHsRRL99Uvfb8c" \
  -H "Content-Type: application/json" \
  --data '{"name":"ghl-automation-ai"}' | jq -r '.site_id')

# Link site
netlify link --id $SITE_ID

# Set environment variables
netlify env:set OPENAI_API_KEY $OPENAI_API_KEY
netlify env:set GHL_API_KEY $GHL_API_KEY
netlify env:set GHL_LOCATION_ID $GHL_LOCATION_ID

# Deploy
netlify deploy --prod
