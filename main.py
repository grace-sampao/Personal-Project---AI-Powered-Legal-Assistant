from fastapi import FastAPI

from agent.chat_engine import agent
from agent.prompts import user_prompt


app = FastAPI()

@app.get("/")
async def root():
    # Run the agent
    response = await agent.run(user_prompt)
    return response
