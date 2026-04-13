import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers.vector_db_manager import VectorDBManager, create_vector_db_manager


class TestVectorDBManager:
    def test_create_chroma_manager(self):
        config = {"chroma_persist_directory": "./test_chroma_db"}
        manager = create_vector_db_manager(config)
        assert manager.get_provider() == "chroma"

    def test_create_chroma_manager_default(self):
        config = {}
        manager = create_vector_db_manager(config)
        assert manager.get_provider() == "chroma"

    def test_unknown_provider(self):
        config = {"vector_db_provider": "unknown"}
        with pytest.raises(ValueError):
            create_vector_db_manager(config)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])