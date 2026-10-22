import os
import asyncio

from dotenv import load_dotenv
from llama_index.core import Settings
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.deepseek import DeepSeek


load_dotenv()

# Settings control global defaults
Settings.llm = DeepSeek(
    model="deepseek-chat",
    api_key=os.environ["DEEPSEEK_API_KEY"],
    request_timeout=360.0,
    # Manually set the context window to limit memory usage
    context_window=8000,
)

# Define a simple calculator tool
def multiply(a: float, b: float) -> float:
    """Useful for multiplying two numbers."""
    return a * b

# Create an agent workflow
agent = FunctionAgent(
    tools=[multiply],
    llm=Settings.llm,
    system_prompt=prompts.system_prompt,
)

async def main():
    # Run the agent
    response = await agent.run(prompts.user_prompt)
    print(str(response))

# Run the agent
if __name__ == "__main__":
    asyncio.run(main())