import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers.embedding_manager import EmbeddingManager, create_embedding_manager


class TestEmbeddingManager:
    def test_create_ollama_manager(self):
        config = {
            "embedding_provider": "ollama",
            "embedding_model": "mxbai-embed-large"
        }
        manager = create_embedding_manager(config)
        assert manager.get_provider() == "ollama"
        assert manager.get_model() == "mxbai-embed-large"

    def test_create_openai_manager(self):
        # Skip if no OpenAI key available
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("No OPENAI_API_KEY set")
        config = {
            "embedding_provider": "openai",
            "embedding_model": "text-embedding-3-small"
        }
        manager = create_embedding_manager(config)
        assert manager.get_provider() == "openai"
        assert manager.get_model() == "text-embedding-3-small"

    def test_default_provider(self):
        # Skip if no OpenAI key available
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("No OPENAI_API_KEY set")
        config = {}
        manager = create_embedding_manager(config)
        assert manager.get_provider() == "openai"

    def test_unknown_provider(self):
        config = {"embedding_provider": "unknown"}
        with pytest.raises(ValueError):
            create_embedding_manager(config)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])