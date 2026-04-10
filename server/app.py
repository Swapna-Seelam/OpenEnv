from openenv_core.env_server import create_fastapi_app
from env import EmailEnv
from models import EmailAction, EmailObservation
import uvicorn
import os

app = create_fastapi_app(EmailEnv, EmailAction, EmailObservation)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "OpenEnv Email Triage API Running"}

def main():
    # This main function is required for openenv validation
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()