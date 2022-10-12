#!/bin/bash
PUBLIC_IP_ADDRESS=$(ip route get 8.8.8.8 | sed -n '/src/{s/.*src *\([^ ]*\).*/\1/p;q}')
uvicorn app:app --host $PUBLIC_IP_ADDRESS --port 5000 --reload