# pawra_backend_api
Backend for Pawra REST API

# How to Install
## Requirements
- Posgtresql database
- Python installed
## Steps
- Clone repo from git
- Copy `.env.example` dan rename it to `.env`, then fill it
- To get the secret key, run `openssl rand -hex 32` in terminal
- Run `pip install --no-cache-dir -r requirements.txt` in terminal
- Finally, to run the application type `uvicorn app.main:app --reload --port 8000` in terminal
- Access the provided API in [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)