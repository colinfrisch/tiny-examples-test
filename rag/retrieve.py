import chromadb
from preprocess_docs import MyEmbeddingFunction

ef = MyEmbeddingFunction()
chroma_client = chromadb.PersistentClient(path="chroma_data")
collection = chroma_client.get_or_create_collection('essay', embedding_function=ef)

def retrieve(question : str, n_results : int = 1) -> str:
    """
    Retrieve the most relevant documents chunks from the collection
    """

    res = collection.query(
        query_texts = [question],
        n_results = n_results,
        include=["documents","distances","metadatas","embeddings"]
    )

    return str(res["documents"][0])

if __name__ == "__main__":
    question = "What classes did the author take ?"
    hits = retrieve(question)
    print(hits)
