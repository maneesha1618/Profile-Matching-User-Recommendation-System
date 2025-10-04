"""
===============================================================================  
                             GoFreeLab Proprietary  
-------------------------------------------------------------------------------  

Project Name    : Skill Rag Clustering  
File Name       : similarity_calculator.py  
Author          : <Author Name>  
Created Date    : <Date>  
Version         : <Version>  
Description     : This script calculates similarity scores between user profiles  
                  using cosine similarity. It handles embedding retrieval,  
                  NaN checks, and caching for efficiency.  

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

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimilarityCalculator:
    def __init__(self, embedding_handler):
        # Embedding handler is passed to the constructor
        self.embedding_handler = embedding_handler
    
    @staticmethod
    def calculate_cosine_similarity(embedding1, embedding2):
        """Calculates cosine similarity between two embeddings, handling NaN values."""
        try:
            embedding1 = np.array(embedding1).reshape(1, -1)
            embedding2 = np.array(embedding2).reshape(1, -1)
            
            # Check for NaN values before calculation
            if np.isnan(embedding1).any() or np.isnan(embedding2).any():
                logger.error("NaN detected in embeddings. Skipping similarity calculation.")
                return None
            
            similarity_score = cosine_similarity(embedding1, embedding2)
            return similarity_score[0][0]
        except ValueError as e:
            logger.error(f"Error in calculating cosine similarity: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in similarity calculation: {e}")
            return None
    
    @staticmethod
    def get_word_embedding(value, embeddings_cache, nlp_model):
        """Fetches or generates a word embedding for the given value, with caching and NaN handling."""
        try:
            if isinstance(value, list):
                value = ' '.join(map(str, value))

            # Check if the embedding already exists in the cache
            if value in embeddings_cache:
                return embeddings_cache[value]
            
            embedding = nlp_model(str(value)).vector
            
            # Check for NaN values
            if np.isnan(embedding).any():
                logger.warning(f"Generated embedding for '{value}' contains NaN values. Skipping.")
                return None
            
            embeddings_cache[value] = embedding
            # logger.info(f"Generated new embedding for: {value}")
            return embedding
        except Exception as e:
            logger.error(f"Error generating word embedding for value '{value}': {e}")
            return None
