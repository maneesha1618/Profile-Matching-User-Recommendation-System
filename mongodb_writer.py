import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBWriter:
    def __init__(self, uri: str, db_name: str):
        """Initialize MongoDB client and database."""
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def close(self) -> None:
        """Close the MongoDB client connection."""
        self.client.close()
        logger.info("MongoDB client connection closed.")

    def write_similarity_scores(self, collection_name_out: str, results: list) -> None:
        """Write similarity scores to a MongoDB collection."""
        try:
            collection = self.db[collection_name_out]
            if results:  # Check if results are not empty
                collection.insert_many(results)
                logger.info(f"Inserted {len(results)} similarity scores into {collection_name_out}.")
            else:
                logger.warning("No results to insert.")
        except PyMongoError as e:
            logger.error(f"Error writing similarity scores to MongoDB: {e}")

    def write_similarity_count(self, collection_name_out: str, selected_similarity_count: int) -> None:
        """Write the count of selected similarity scores to a MongoDB collection."""
        try:
            collection = self.db[collection_name_out]
            count_document = {"selected_similarity_count": selected_similarity_count}
            # Insert count as a single document
            collection.update_one({}, {"$set": count_document}, upsert=True)
            logger.info(f"Inserted similarity count into {collection_name_out}.")
        except PyMongoError as e:
            logger.error(f"Error writing similarity count to MongoDB: {e}")

