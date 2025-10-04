"""
===============================================================================  
                             GoFreeLab Proprietary  
-------------------------------------------------------------------------------  

Project Name    : Skill Rag Clustering  
File Name       : db.py  
Author          : <Author Name>  
Created Date    : <Date>  
Version         : <Version>  
Description     : This script manages MongoDB operations, including establishing  
                  database connections, retrieving stored vectors, and storing  
                  vectorized representations of text with upsert functionality.  
                  It includes logging and error handling to ensure database  
                  reliability.  

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

import logging
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect_to_mongo(mongo_uri, database_name):
    """Establish a connection to the MongoDB database."""
    try:
        client = MongoClient(mongo_uri)
        database = client[database_name]
        logger.info(f"Connected to MongoDB database: {database_name}")
        return database
    except PyMongoError as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise Exception(f"Failed to connect to MongoDB: {e}")

def retrieve_vector_from_db(text, database, vector_collection, timeout_ms=5000):
    """Retrieve a vector from the MongoDB vector database with a timeout."""
    try:
        vector_collection = database[vector_collection]
        result = vector_collection.find_one({"text": text}, max_time_ms=timeout_ms)
        if result and "vector" in result:
            logger.info(f"Retrieved vector for text: {text}")
            return np.array(result["vector"])
        logger.info(f"No vector found for text: {text}")
        return None
    except PyMongoError as e:
        logger.error(f"Error retrieving vector from database for text '{text}': {e}")
        raise Exception(f"Error retrieving vector from database for text '{text}': {e}")

def store_vector_in_db(doc, database, vector_collection):
    """
    Store a vector document in the MongoDB vector database.
    
    The document can be in one of two formats:
      1. Simple format: {"text": <text>, "vector": <vector>}
      2. Combined format: {"text1": <text1>, "vector1": <vector1>, "text2": <text2>, "vector2": <vector2>}
    
    The function uses an upsert operation with a filter built from the available text fields.
    """
    try:
        vector_collection = database[vector_collection]
        # Build the filter based on the document's keys.
        if "text1" in doc and "text2" in doc:
            filter_query = {"text1": doc.get("text1"), "text2": doc.get("text2")}
        elif "text" in doc:
            filter_query = {"text": doc.get("text")}
        else:
            raise ValueError("Document format not recognized. Expected keys: 'text' or both 'text1' and 'text2'.")
        # Ensure that if the vector is a numpy array, we convert it to a list
        if "vector" in doc and hasattr(doc["vector"], "tolist"):
            doc["vector"] = doc["vector"].tolist()
        if "vector1" in doc and hasattr(doc["vector1"], "tolist"):
            doc["vector1"] = doc["vector1"].tolist()
        if "vector2" in doc and hasattr(doc["vector2"], "tolist"):
            doc["vector2"] = doc["vector2"].tolist()
        vector_collection.update_one(
            filter_query,
            {"$set": doc},
            upsert=True
        )
        logger.info(f"Stored vector document: {doc}")
    except PyMongoError as e:
        logger.error(f"Error storing vector document: {e}")
        raise Exception(f"Error storing vector document: {e}")
