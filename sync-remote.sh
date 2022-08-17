#!/bin/bash

curl --request POST "https://api.render.com/v1/services/$ADAPT_RENDER_ID_DEV/jobs" \
    --header "Authorization: Bearer $ADAPT_RENDER_KEY" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "startCommand": "python3 sync.py"
    }'