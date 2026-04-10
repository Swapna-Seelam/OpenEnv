import uvicorn
from openenv.core.env_server import create_web_interface_app
from env.email_env import EmailEnv, EmailAction, EmailObservation

# Create the FastAPI app with the Web Interface enabled
# We pass the class EmailEnv, which the framework expects
app = create_web_interface_app(EmailEnv, EmailAction, EmailObservation)

def main():
    # Run the server on port 7860 (Hugging Face default)
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()