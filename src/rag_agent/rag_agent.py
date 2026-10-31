# 1. Agent starts with a greeting that includes the user's name(s).
# 2. User queries agent about a particular issue contained in the data.
# 3. Agent responds to the query, citing references from the data.
import os
import asyncio
from dotenv import load_dotenv

from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.deepseek import DeepSeek
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


load_dotenv()

class RAGAgentService:
    def __init__(self, data_dir: str = "data"):
        """Initializes settings, loads documents and builds agent state ONCE."""
        print("Initializing RAG Agent Service...")

        # 1. Global settings configuration
        Settings.llm = DeepSeek(
            model="deepseek-chat",
            api_key=os.environ["DEEPSEEK_API_KEY"],
            request_timeout=360.0,
            context_window=8000,
        )
        Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

        # 2. Load documents and build index
        documents = SimpleDirectoryReader(data_dir).load_data()
        index = VectorStoreIndex.from_documents(documents)
        self.chat_engine = index.as_chat_engine()

        # 3. Register tools bound to this instance
        self._setup_tools()

        # 4. Initialize the Agent workflow
        self.agent = FunctionAgent(
            tools=[self.multiply, self.search_documents],
            llm=Settings.llm,
            system_prompt="""You are a helpful assistant that can perform calculations and search through documents to answer questions."""
        )

    def _setup_tools(self):
        """Defines the internal tools available to the agent."""
        def multiply(a: float, b: float) -> float:
            """Useful for multiplying two numbers."""
            return a * b

        async def search_documents(query: str) -> str:
            """Useful for answering natural language questions about documents."""
            response = await self.chat_engine.achat(query)
            return str(response)

        # Attach tools to instance scope so FunctionAgent can access them
        self.multiply = multiply
        self.search_documents = search_documents

    async def run_query(self, query: str) -> str:
        """Public interface method to run a query through the agent."""
        response = await self.agent.run(query)
        return str(response)

# --- Execution Example ---
if __name__ == "__main__":
    # Instantiate the service object once (simulating server startup)
    rag_service = RAGAgentService(data_dir="data")
    user_prompt = input("Hello, what do you need help with today?\n>").strip()

    if user_prompt:
        result = asyncio.run(rag_service.run_query(user_prompt))
        
        print("\n--- Agent Response ---")
        print(result)
    else:
        print("Kindly input your query...")
