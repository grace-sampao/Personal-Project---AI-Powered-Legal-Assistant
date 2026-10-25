# 1. Agent starts with a greeting that includes the user's name(s).
# 2. User queries agent about a particular issue contained in the data.
# 3. Agent responds to the query, citing references from the data.
import os
from dotenv import load_dotenv
import asyncio

from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.deepseek import DeepSeek
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


load_dotenv()

# Settings control global defaults
Settings.llm = DeepSeek(
    model="deepseek-chat",
    api_key=os.environ["DEEPSEEK_API_KEY"],
    request_timeout=360.0,
    # Manually set the context window to limit memory usage
    context_window=8000,
)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

def chat_agent():
    # Create a RAG tool using LlamaIndex
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    chat_engine = index.as_chat_engine()

    def multiply(a: float, b: float) -> float:
        """Useful for multiplying two numbers."""
        return a * b

    async def search_documents(query: str) -> str:
        """Useful for answering natural language questions about a personal essay 
        written by Paul Graham."""
        response = await chat_engine.achat(query)
        return str(response)

    # Create an enhanced workflow with both tools
    agent = FunctionAgent(
        tools=[multiply, search_documents],
        llm=Settings.llm,
        system_prompt="""You are a helpful assistant that can perform calculations 
        and search through documents to answer questions."""
    )

    user_prompt = input("Hello, what do you need help with today?\n").strip()

    if not user_prompt:
        return "Kindly input your query..."

    # Define local runner and RETURN the asyncio result
    async def run_agent(query: str):
        return await agent.run(query)

    # Explicitly return the output of asyncio.run(...)
    return asyncio.run(run_agent(user_prompt))

# Execution at entry point
if __name__ == "__main__":
    response = chat_agent()
    print("\n--- Agent Response ---")
    print(response)
