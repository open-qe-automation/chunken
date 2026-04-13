# MetadataDB Manager - Store chunk text and metadata
# Supports: PostgreSQL (local), MongoDB (cloud)

import logging as log

class MetadataDBManager:
    def __init__(self, provider="postgresql", config=None):
        self.provider = provider.lower()
        self.config = config or {}
        self.client = None
        self.cursor = None
        
        if self.provider == "postgresql":
            self._init_postgresql()
        elif self.provider == "mongodb":
            self._init_mongodb()
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    def _init_postgresql(self):
        from .postgres_helper import PostgresDB
        conn_string = self.config.get("connection_string")
        self.client = PostgresDB(connection_string=conn_string)
        self.client.connect()
        self.client.create_chunks_table()
        log.info("MetadataDBManager initialized with PostgreSQL")
    
    def _init_mongodb(self):
        from helpers.mongo_helper import MongoDatabase
        mongo_uri = self.config.get("mongo_uri")
        self.client = MongoDatabase(mongo_uri)
        log.info("MetadataDBManager initialized with MongoDB")
    
    def save_chunks(self, database, namespace, chunks_data):
        """Save chunk text and metadata"""
        if self.provider == "postgresql":
            return self._save_postgresql(database, chunks_data)
        elif self.provider == "mongodb":
            return self._save_mongodb(database, namespace, chunks_data)
    
    def _save_postgresql(self, table_name, chunks_data):
        # Convert chunks_data format for PostgreSQL
        formatted_chunks = []
        for chunk in chunks_data.get("data", []):
            formatted_chunks.append({
                "chunk_id": chunk.get("chunk_id"),
                "parent_id": chunks_data.get("_id"),
                "source": chunks_data.get("source"),
                "chunk_number": chunk.get("chunk_number"),
                "text": chunk.get("text"),
                "metadata": {}
            })
        return self.client.insert_chunks(table_name, formatted_chunks)
    
    def _save_mongodb(self, database, namespace, chunks_data):
        with self.client as client:
            result = client.insert_or_update_chunk(database, namespace, chunks_data)
            return result
    
    def get_chunk_by_id(self, database, chunk_id):
        """Retrieve chunk text by ID"""
        if self.provider == "postgresql":
            return self.client.get_chunk_by_id(database, chunk_id)
        elif self.provider == "mongodb":
            # MongoDB implementation would be different
            return None
    
    def get_chunks_by_parent(self, database, parent_id):
        """Get all chunks for a source file"""
        if self.provider == "postgresql":
            return self.client.get_chunks_by_parent_id(database, parent_id)
        elif self.provider == "mongodb":
            return None
    
    def close(self):
        if self.client and self.provider == "postgresql":
            self.client.disconnect()
    
    def get_provider(self):
        return self.provider


def create_metadata_db_manager(config):
    """Factory function to create metadata DB manager from config"""
    provider = config.get("metadata_db_provider", "postgresql")
    
    provider_config = {}
    if provider == "mongodb":
        from env_config import envs
        env = envs()
        provider_config = {"mongo_uri": env.mongo_uri}
    elif provider == "postgresql":
        provider_config = {
            "connection_string": config.get("postgresql_connection_string")
        }
    
    return MetadataDBManager(provider=provider, config=provider_config)