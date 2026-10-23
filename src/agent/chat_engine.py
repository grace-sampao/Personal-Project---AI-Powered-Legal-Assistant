import os
import asyncio

from dotenv import load_dotenv
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.deepseek import DeepSeek
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from agent import prompts, tools


load_dotenv()

# Settings control global defaults
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
Settings.llm = DeepSeek(
    model="deepseek-chat",
    api_key=os.environ["DEEPSEEK_API_KEY"],
    request_timeout=360.0,
    # Manually set the context window to limit memory usage
    context_window=8000,
)

# Create a RAG tool using LlamaIndex
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
chat_engine = index.as_chat_engine()

async def search_documents(query: str) -> str:
    """Useful for answering natural language questions about a personal essay 
    written by Paul Graham."""
    response = await chat_engine.achat(query)
    return str(response)

# Create an agent workflow
agent = FunctionAgent(
    tools=[tools.multiply, search_documents],
    llm=Settings.llm,
    system_prompt=prompts.system_prompt,
)

async def main():
    # Run the agent
    response = await agent.run(prompts.user_prompt)
    print(response)

# Run the agent
if __name__ == "__main__":
    asyncio.run(main())