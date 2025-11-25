# mqtt
A Docker setup for running Eclipse Mosquitto MQTT broker


run using 

```shell
docker run -d -p 1883:1883 -p 9001:9001 --name iot-mqtt iot-mqtt
```

Local development with health endpoint

- Build and start both the broker and a small HTTP health service that checks MQTT connectivity:

```powershell
docker compose up --build
```

- The health endpoint will be available at `http://localhost:8080/health` and will return JSON:
	- `200` and `{ "status": "ok", "target": "mosquitto:1883" }` when it can connect to the broker
	- `503` and `{ "status": "unhealthy", "error": "..." }` otherwise

Notes
- The health service is a tiny Python server in `health/` that opens a TCP connection to the broker (service name `mosquitto`) to determine health.
- This uses a sidecar container pattern. It's also possible to run a health server inside the same container or use Docker's `HEALTHCHECK` instruction if you prefer a single-container approach.


