import asyncio
import os
from dotenv import load_dotenv

from fastapi import FastAPI

import src.ai_powered_legal_assistant.agent as agent


app = FastAPI()

@app.get("/")
def read_root():
    rag_service = agent.RAGAgentService(data_dir='./src/ai_powered_legal_assistant/data')
    user_prompt = "What did the author do growing up and what is 7 * 8?"

    result = asyncio.run(rag_service.run_query(user_prompt))

    return result

    # if __name__ == "__main__":
        # Instantiate the service object once (simulating server startup)
        # rag_service = agent.RAGAgentService(data_dir="data/paul_graham_essay.txt")
        # user_prompt = input("Hello, what do you need help with today?\n>").strip()
        # user_prompt = "What did the author do growing up and what is 7 * 8?"

    #     if user_prompt:
    #         result = asyncio.run(rag_service.run_query(user_prompt))

    #         return result
    #         print("\n--- Agent Response ---")
    #         print(result)
    #     else:
    #         return "Kindly input your query..."
    #         print("Kindly input your query...")

    # return {"Hello": "World"}
        # result = asyncio.run(rag_service.run_query(user_prompt))

        # return result
