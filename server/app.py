import openenv
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openenv.core.env_server import create_fastapi_app
from env.email_env import EmailEnv, EmailAction, EmailObservation

# Log startup information to stdout (Hugging Face Logs)
print(f"[STARTUP] Python Version: {sys.version}")
print(f"[STARTUP] OpenEnv Version: {openenv.__version__ if hasattr(openenv, '__version__') else 'unknown'}")

# Initialize core helper-based app
app = create_fastapi_app(EmailEnv, EmailAction, EmailObservation)

# Add CORS support for autograder/browser connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Explicit health check for autograder
@app.get("/health")
def health():
    print("[DEBUG] /health reached")
    return {"status": "ok"}

@app.get("/")
def root():
    print("[DEBUG] / (root) reached")
    return {
        "message": "Email Triage OpenEnv API is Running",
        "description": "Multi-step AI environment for email triage",
        "endpoints": ["/reset", "/step", "/state", "/health"]
    }

# The app object is now ready for uvicorn server.app:app