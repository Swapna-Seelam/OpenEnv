from openenv_core.env_server import create_fastapi_app
from env import EmailEnv
from models import EmailAction, EmailObservation
import uvicorn

app = create_fastapi_app(EmailEnv, EmailAction, EmailObservation)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "OpenEnv Email Triage API Running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)