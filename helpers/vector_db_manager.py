# VectorDB Manager - Abstraction layer for different vector databases
# Supports: ChromaDB (local), Pinecone (cloud)

import logging as log

class VectorDBManager:
    def __init__(self, provider="chroma", config=None):
        self.provider = provider.lower()
        self.config = config or {}
        self.client = None
        
        if self.provider == "chroma":
            self._init_chroma()
        elif self.provider == "pinecone":
            self._init_pinecone()
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    def _init_chroma(self):
        from .chroma_helper import ChromaDB
        persist_dir = self.config.get("chroma_persist_directory", "./chroma_db")
        print(f"DEBUG: Initializing ChromaDB at {persist_dir}")
        self.client = ChromaDB(persist_directory=persist_dir)
        log.info(f"ChromaDB initialized at: {persist_dir}")
    
    def _init_pinecone(self):
        from pinecone import Pinecone
        api_key = self.config.get("pinecone_api_key")
        self.client = Pinecone(api_key=api_key)
        log.info("Pinecone initialized")
    
    def upsert(self, vectors, namespace="default"):
        """Insert or update vectors"""
        if self.provider == "chroma":
            return self._upsert_chroma(vectors, namespace)
        elif self.provider == "pinecone":
            return self._upsert_pinecone(vectors, namespace)
    
    def _upsert_chroma(self, vectors, namespace):
        print(f"DEBUG: _upsert_chroma called with {len(vectors)} vectors, namespace={namespace}")
        
        ids = [v["id"] for v in vectors]
        embeddings = [v["values"] for v in vectors]
        metadatas = [v.get("metadata", {}) for v in vectors]
        documents = [v.get("text", "") for v in vectors]
        
        print(f"DEBUG: ids={len(ids)}, embeddings={len(embeddings)}, docs={len(documents)}")
        
        collection = self.client.get_or_create_collection(namespace)
        
        try:
            collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents)
            print(f"DEBUG: Added {len(ids)} items to collection {namespace}")
        except Exception as e:
            print(f"DEBUG: Add failed: {e}")
            
        return {"upserted_count": len(vectors)}
    
    def _upsert_pinecone(self, vectors, namespace):
        return self.index.upsert(vectors=vectors, namespace=namespace)
    
    def query(self, query_embedding, top_k=5, namespace="default", filter=None):
        """Search for similar vectors"""
        if self.provider == "chroma":
            return self._query_chroma(query_embedding, top_k, namespace)
        elif self.provider == "pinecone":
            return self._query_pinecone(query_embedding, top_k, namespace, filter)
    
    def _query_chroma(self, query_embedding, top_k, namespace):
        collection = self.client.get_or_create_collection(namespace)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return self._convert_chroma_results(results)
    
    def _query_pinecone(self, query_embedding, top_k, namespace, filter=None):
        return self.index.query(
            vector=query_embedding,
            top_k=top_k,
            namespace=namespace,
            filter=filter,
            include_metadata=True,
            include_values=True
        )
    
    def _convert_chroma_results(self, results):
        """Convert ChromaDB format to match Pinecone"""
        return {
            "matches": [
                {
                    "id": results["ids"][0][i],
                    "score": 1 - results["distances"][0][i] if results.get("distances") else 0,
                    "values": results["embeddings"][0][i] if results.get("embeddings") else [],
                    "metadata": results["metadatas"][0][i] if results.get("metadatas") else {}
                }
                for i in range(len(results.get("ids", [[]])[0]))
            ]
        }
    
    def delete(self, ids, namespace="default"):
        """Delete vectors by ID"""
        if self.provider == "chroma":
            collection = self.client.get_or_create_collection(namespace)
            return {"deleted_count": 0}
        elif self.provider == "pinecone":
            return self.index.delete(ids=ids, namespace=namespace)
    
    def get_provider(self):
        return self.provider


def create_vector_db_manager(config):
    """Factory function to create vector DB manager from config"""
    provider = config.get("vector_db_provider", "chroma")
    
    provider_config = {}
    if provider == "pinecone":
        from env_config import envs
        env = envs()
        provider_config = {
            "pinecone_api_key": env.pinecone_key,
            "database": config.get("database")
        }
    elif provider == "chroma":
        provider_config = {
            "chroma_persist_directory": config.get("chroma_persist_directory", "./chroma_db")
        }
    
    return VectorDBManager(provider=provider, config=provider_config)