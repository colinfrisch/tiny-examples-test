from chunking import chunk_to_words

from mistralai import Mistral
from tqdm import tqdm
import numpy as np
from dotenv import load_dotenv

import requests
import math
import chromadb
import os

# ------------------- configuration -------------------

load_dotenv()

api_key = os.getenv('MISTRAL_API_KEY')
client = Mistral(api_key=api_key)

chroma_client = chromadb.PersistentClient(path = 'chroma_data')

response = requests.get('https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt')
text = response.text
text = text[0:math.floor(len(text)/2)]

# ------------------- chunking and embedding -------------------

chunks = chunk_to_words([text], chunk_size_in_words=150)

def get_text_embedding(chunk_list : list[str]) -> np.array:
    """
    Transforms a list of texts into a list of embeddings

    Args:
        chunk_list (list[str]): List of texts to embed

    Returns:
        np.array: List of embeddings
    """

    embedded_chunks : list[np.array] = []

    try : 

        for chunk in tqdm(chunk_list, desc='embedding chunks with mistral...'):
        
            embedded_chunks_resp = client.embeddings.create(
                model = 'mistral-embed',
                inputs = chunk,
            )
            
            embedded_chunks.append(embedded_chunks_resp.data[0].embedding)
        
    except Exception as e :
        print(e)

        


    return embedded_chunks


class MyEmbeddingFunction:
    def __init__(self, model_id: str = "custom-embedder-v1"):
        self._name = f"custom:{model_id}"
    def __call__(self, input: list[str]) -> list[list[float]]:
        return get_text_embedding(input)
    def name(self) -> str:  # Chroma calls this to persist/validate EF config
        return self._name

chroma_client = chromadb.PersistentClient(path="chroma_data")


# ------------------- dataset setup -------------------

if __name__ == '__main__':
    
    ef = MyEmbeddingFunction() 

    collection = chroma_client.get_or_create_collection('essay', embedding_function=ef)

    collection.add(
        ids = [str(i) for i in range(len(chunks))],
        documents = chunks,
        #embeddings = get_text_embedding(chunks)
    )

