#!/usr/bin/env python3
"""Simple ChromaDB viewer - queries the SQLite database directly"""
import sqlite3
import os
import sys

def view_chroma_db(path):
    if not os.path.exists(path):
        print(f"Error: {path} does not exist")
        return
    
    db_path = os.path.join(path, "chroma.sqlite3")
    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=" * 50)
    print("CHROMADB VIEWER")
    print("=" * 50)
    
    # Collections
    cursor.execute("SELECT id, name, dimension FROM collections")
    collections = cursor.fetchall()
    print(f"\nCollections ({len(collections)}):")
    for col_id, name, dim in collections:
        print(f"  - {name} (id: {col_id[:20]}..., dim: {dim})")
    
    # Segments
    cursor.execute("SELECT COUNT(*) FROM segments")
    seg_count = cursor.fetchone()[0]
    print(f"\nSegments: {seg_count}")
    
    # Embeddings
    cursor.execute("SELECT COUNT(*) FROM embeddings")
    emb_count = cursor.fetchone()[0]
    print(f"Embeddings: {emb_count}")
    
    # Tenants
    cursor.execute("SELECT * FROM tenants")
    tenants = cursor.fetchall()
    print(f"\nTenants: {tenants}")
    
    conn.close()

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "../share/chroma_db"
    view_chroma_db(path)