import asyncio

from fastapi import FastAPI

import src.ai_powered_legal_assistant.agent as agent


app = FastAPI()

@app.get("/")
def read_root():
    if __name__ == "__main__":
        # Instantiate the service object once (simulating server startup)
        rag_service = agent.RAGAgentService(data_dir="data")
        user_prompt = input("Hello, what do you need help with today?\n>").strip()

        if user_prompt:
            result = asyncio.run(rag_service.run_query(user_prompt))

            return result
            # print("\n--- Agent Response ---")
            # print(result)
        else:
            return "Kindly input your query..."
            # print("Kindly input your query...")

    # return {"Hello": "World"}
