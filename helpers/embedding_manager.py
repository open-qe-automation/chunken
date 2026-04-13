# Embedding Manager - Abstraction layer for different embedding providers
# Supports: OpenAI (cloud), Ollama (local)

import os
import logging as log

class EmbeddingManager:
    def __init__(self, provider="openai", model=None, api_key=None, base_url="http://localhost:11434"):
        self.provider = provider.lower()
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.client = None
        
        if self.provider == "openai":
            self._init_openai()
        elif self.provider == "ollama":
            self._init_ollama()
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    def execute(self, text):
        return self.embed(text)
    
    def embed(self, text):
        if self.provider == "openai":
            return self._embed_openai(text)
        elif self.provider == "ollama":
            return self._embed_ollama(text)
    
    def _init_ollama(self):
        # Import local Ollama helper
        import sys
        import os
        sys.path.insert(0, os.path.dirname(__file__))
        from ollama_helper import OllamaEmbeddings
        self.client = OllamaEmbeddings(model=self.model, base_url=self.base_url)
        log.info(f"EmbeddingManager initialized with Ollama: {self.model}")
    
    def _embed_openai(self, text):
        response = self.client.embeddings.create(
            input=text,
            model=self.model
        )
        return {
            "data": [{
                "embedding": response.data[0].embedding
            }]
        }
    
    def _embed_ollama(self, text):
        embedding = self.client.execute(text)
        if embedding:
            return {"data": [{"embedding": embedding}]}
        return None
    
    def get_model(self):
        return self.model
    
    def get_provider(self):
        return self.provider


def create_embedding_manager(config):
    """Factory function to create embedding manager from config"""
    provider = config.get("embedding_provider", "openai")
    model = config.get("embedding_model")
    api_key = config.get("embedding_api_key")
    base_url = config.get("embedding_base_url", "http://localhost:11434")
    
    return EmbeddingManager(
        provider=provider,
        model=model,
        api_key=api_key,
        base_url=base_url
    )