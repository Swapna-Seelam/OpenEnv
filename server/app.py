from openenv_core import OpenEnv

app = OpenEnv()

@app.action
def email_text(text: str):
    return {"output": text}