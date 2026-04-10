import uvicorn
from fastapi import FastAPI
from openenv.core.env_server import create_fastapi_app
from env.email_env import EmailEnv, EmailAction, EmailObservation

# Use create_fastapi_app for maximum compatibility with autograders
# We pass the EmailEnv CLASS, not an instance
app = create_fastapi_app(EmailEnv, EmailAction, EmailObservation)

# Add a simple health check and root message
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Email Triage OpenEnv API is Running"}

def main():
    # HF expects port 7860
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()