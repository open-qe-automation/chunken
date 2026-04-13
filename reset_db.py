#!/usr/bin/env python3
"""Reset ChromaDB and PostgreSQL for fresh pipeline run."""

import os
import sys
import psycopg2

def reset_chroma(chroma_path):
    """Delete ChromaDB files."""
    if os.path.exists(chroma_path):
        for f in os.listdir(chroma_path):
            fp = os.path.join(chroma_path, f)
            if os.path.isfile(fp):
                os.remove(fp)
        print(f"Cleared ChromaDB: {chroma_path}")
    else:
        print(f"ChromaDB path not found: {chroma_path}")

def reset_postgres(conn_string, table_name):
    """Delete all rows from PostgreSQL table."""
    try:
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        cur.execute(f'DELETE FROM "{table_name}"')
        conn.commit()
        print(f"Cleared PostgreSQL table: {table_name}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error clearing PostgreSQL: {e}")

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    share_dir = os.path.join(base_dir, 'share')
    
    chroma_path = os.path.join(share_dir, 'chroma_db')
    reset_chroma(chroma_path)
    
    conn_string = 'postgresql://postgres:ragpassword@localhost:5432/rag'
    reset_postgres(conn_string, 'rag-system')
    
    print("\nDatabase reset complete. Run pipeline:")
    print("  cd texten && python app.py")
    print("  cd chunken && python app.py")