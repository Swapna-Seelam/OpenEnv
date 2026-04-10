import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openenv.core.env_server import create_fastapi_app
from env.email_env import EmailEnv, EmailAction, EmailObservation

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
    return {"status": "ok"}

@app.get("/")
def root():
    return {
        "message": "Email Triage OpenEnv API is Running",
        "description": "Multi-step AI environment for email triage",
        "endpoints": ["/reset", "/step", "/state", "/health"]
    }

def main():
    # HF expects port 7860
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()