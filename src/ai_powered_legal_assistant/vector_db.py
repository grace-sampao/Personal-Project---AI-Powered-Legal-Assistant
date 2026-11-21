import os
from dotenv import load_dotenv

import chromadb
import chromadb.utils.embedding_functions as embedding_functions


load_dotenv()

google_ef = embedding_functions.GoogleGeminiEmbeddingFunction(
    model_name="gemini-embedding-001",
    task_type="RETRIEVAL_DOCUMENT",
    api_key_env_var="GEMINI_API_KEY",
    dimension=768,
)
# google_ef(["./data/paul_graham_essay.txt"])

client = chromadb.PersistentClient()
collection = client.get_or_create_collection(
    name="test_docs",
    embedding_function=google_ef,
)

# collection.upsert(
#     ids=["id1", "id2"],
#     documents=[
#         "This is a document about pineapples",
#         "This is a document about oranges"
#     ]
# )

# results = collection.query(
#     query_texts=["This is a query document about Florida"],      # Chroma will embed this for you
#     n_results=2         # How many results to return   
# )

# print(results)
