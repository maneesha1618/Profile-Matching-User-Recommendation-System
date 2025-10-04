"""
===============================================================================  
                             GoFreeLab Proprietary  
-------------------------------------------------------------------------------  

Project Name    : Skill Rag Clustering  
File Name       : mongodb_writer.py  
Author          : <Author Name>  
Created Date    : <Date>  
Version         : <Version>  
Description     : This script handles MongoDB operations, including storing and  
                  retrieving similarity scores, similarity counts, and vector data.  
                  It ensures efficient data handling and error management.  

-------------------------------------------------------------------------------  
Copyright (c) 2025 GoFreeLab. All rights reserved.  

This source code and all its contents are the proprietary property of GoFreeLab.  
Unauthorized copying, sharing, or distribution of this code, in whole or in  
part, via any medium is strictly prohibited without prior written permission  
from GoFreeLab.  

This software is for use only by employees, contractors, or partners of  
GoFreeLab with explicit authorization.  

For questions or permissions, please contact: info@gofreelab.com  
===============================================================================  
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import logging
import numpy as np

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBWriter:
    def __init__(self):
        """Initialize MongoDB client and database using environment variables."""
        # Load MongoDB URI and DB Name from .env
        self.uri = os.getenv('MONGO_URI')  # MongoDB URI
        self.db_name = os.getenv('DB_NAME')
        self.collection_name =os.getenv('COLLECTION_NAME')  # Database name

        if not self.uri or not self.db_name:
            raise ValueError("MONGO_URI and DB_NAME must be set in the .env file")

        # Initialize the MongoDB client with the URI
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]
        logger.info(f"Connected to MongoDB at {self.uri} and using database {self.db_name}")
        
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

    def retrieve_vector_from_db(self, text, vector_collection, timeout_ms=5000):
        """Retrieve a vector from the MongoDB vector database with a timeout."""
        try:
            vector_collection = self.db[vector_collection]
            result = vector_collection.find_one({"text": text}, max_time_ms=timeout_ms)
            if result and "vector" in result:
                logger.info(f"Retrieved vector for text '{text}'")
                return np.array(result["vector"])
            logger.warning(f"No vector found for text '{text}'")
            return None
        except PyMongoError as e:
            logger.error(f"Error retrieving vector from database for text '{text}': {e}")
            raise Exception(f"Error retrieving vector from database for text '{text}': {e}")

    def store_vector_in_db(self, text, vector, vector_collection):
        """Store a vector in the MongoDB vector database."""
        try:
            vector_collection = self.db[vector_collection]
            result = vector_collection.update_one(
                {"text": text},
                {"$set": {"vector": vector.tolist()}},  # Convert numpy array to list for JSON compatibility
                upsert=True
            )
            logger.info(f"Stored vector for text '{text}' in the collection '{vector_collection}'")
        except PyMongoError as e:
            logger.error(f"Error storing vector in database for text '{text}': {e}")
            raise Exception(f"Error storing vector in database for text '{text}': {e}")
