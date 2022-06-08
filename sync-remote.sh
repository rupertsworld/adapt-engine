curl --request POST 'https://api.render.com/v1/services/srv-cabcmnc41ls9f3cj9730/jobs' \
    --header "Authorization: Bearer $ADAPT_RENDER_KEY" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "startCommand": "python3 sync.py"
    }