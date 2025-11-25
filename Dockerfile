# Use the official Eclipse Mosquitto image as the base
FROM python:3.11-slim

# Install mosquitto broker
LABEL maintainer="johnscode <iotagg@johnscode.com>"
RUN apt-get update \
	&& DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends mosquitto \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy configuration and health check
COPY mosquitto.conf /mosquitto/config/mosquitto.conf
COPY health/health.py /app/health.py
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose MQTT, WebSockets and health ports
EXPOSE 1883
EXPOSE 9001
EXPOSE 8080

CMD ["/app/start.sh"]