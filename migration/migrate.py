import os
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Any
import pymongo
from pymongo import MongoClient
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataMigrator:
    def __init__(self, mongo_uri: str, pg_config: Dict[str, str], batch_size: int = 1000):
        self.mongo_uri = mongo_uri
        self.pg_config = pg_config
        self.batch_size = batch_size
        self.mongo_client = None
        self.pg_conn = None

    def connect(self):
        # Connect to MongoDB with optimal settings
        self.mongo_client = MongoClient(
            self.mongo_uri,
            maxPoolSize=50,
            waitQueueMultiple=10,
            retryWrites=True,
            retryReads=True,
            w='majority'
        )
        
        # Connect to PostgreSQL with optimal settings
        self.pg_conn = psycopg2.connect(
            **self.pg_config,
            keepalives=1,
            keepalives_idle=30,
            keepalives_interval=10,
            keepalives_count=5
        )
        self.pg_conn.set_session(autocommit=False)

    def migrate_collection(self, db_name: str, collection_name: str):
        start_time = time.time()
        collection = self.mongo_client[db_name][collection_name]
        total_docs = collection.count_documents({})
        
        logger.info(f"Starting migration of {total_docs} documents")
        
        cursor = collection.find({}, batch_size=self.batch_size)
        processed = 0
        
        with self.pg_conn.cursor() as cur:
            while True:
                batch = list(cursor.limit(self.batch_size))
                if not batch:
                    break
                
                # Transform batch
                transformed_data = [self.transform_document(doc) for doc in batch]
                
                # Insert batch using execute_values for better performance
                insert_query = f"""
                    INSERT INTO {collection_name} (id, data, created_at, updated_at)
                    VALUES %s
                    ON CONFLICT (id) DO UPDATE
                    SET data = EXCLUDED.data,
                        updated_at = EXCLUDED.updated_at;
                """
                
                execute_values(cur, insert_query, transformed_data)
                self.pg_conn.commit()
                
                processed += len(batch)
                elapsed = time.time() - start_time
                rate = processed / elapsed
                
                logger.info(
                    f"Processed {processed}/{total_docs} documents "
                    f"({(processed/total_docs)*100:.2f}%) "
                    f"at {rate:.2f} docs/sec"
                )

    @staticmethod
    def transform_document(doc: Dict) -> tuple:
        return (
            str(doc['_id']),
            psycopg2.extras.Json(doc),
            doc.get('createdAt', datetime.utcnow()),
            doc.get('updatedAt', datetime.utcnow())
        )

    def close(self):
        if self.mongo_client:
            self.mongo_client.close()
        if self.pg_conn:
            self.pg_conn.close()