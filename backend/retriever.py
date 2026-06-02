import os
import chromadb
from sentence_transformers import SentenceTransformer

class DocumentRetriever:
    def __init__(self, db_path="./vector_store", collection_name="pdf_documents"):
        print("Initializing Local Database Retriever...")
        self.db_path = os.path.abspath(db_path)
        
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.collection = self.client.get_collection(name=collection_name)
        
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

    def get_context(self, subject: str, n_results: int = 4) -> str:
        print(f"Retrieving context for subject: '{subject}'")
        
        q_embed = self.embedder.encode(subject).tolist()
        res = self.collection.query(query_embeddings=[q_embed], n_results=n_results)
        
        if not res['documents'] or not res['documents'][0]:
            return "NO_CONTEXT_FOUND"
            
        return "\n---\n".join(res['documents'][0])