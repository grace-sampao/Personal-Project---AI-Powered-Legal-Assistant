import chromadb


client = chromadb.PersistentClient()
collection = client.get_or_create_collection(name="my_collection")

collection.upsert(
    ids=["id1", "id2"],
    documents=[
        "This is a document about pineapples",
        "This is a document about oranges"
    ]
)

results = collection.query(
    query_texts=["This is a query document about Florida"],      # Chroma will embed this for you
    n_results=2         # How many results to return   
)

print(results)
