Overview
--------
This repository includes a FastAPI backend (`Swift-Chatbot/`) and a React frontend (`../swiftIntelli_implementation_chatbot/swiftintelli`). The `docker-compose.yml` in this folder builds both images.

Build and run locally
---------------------
From the `Swift-Chatbot` folder run:

```bash
docker compose build
docker compose up -d
```

The FastAPI app will be available on port `8000` and the frontend on port `80`.

Notes for Hostinger (Ubuntu + Docker)
------------------------------------
- Upload the project to your Hostinger Ubuntu server (scp / git clone).
- Install Docker and Docker Compose on the server.
- From `Swift-Chatbot` run the same `docker compose` commands above.
- If your MySQL / phpMyAdmin is hosted separately (XAMPP), configure the FastAPI DB connection via environment variables or update `database.py` accordingly — do NOT run a bundled XAMPP inside these containers.

Environment
-----------
- To point the frontend to your deployed backend, set `REACT_APP_API_URL` in the `frontend` service or inject a runtime config.
