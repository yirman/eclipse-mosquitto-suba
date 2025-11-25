#!/bin/sh
set -e

echo "Starting mosquitto..."
/usr/sbin/mosquitto -c /mosquitto/config/mosquitto.conf &
MOSQ_PID=$!

# Give mosquitto a moment to start
sleep 1

echo "Starting health server..."
exec python3 /app/health.py
