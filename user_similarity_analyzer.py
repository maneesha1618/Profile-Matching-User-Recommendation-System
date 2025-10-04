"""===============================================================================  
                             GoFreeLab Proprietary  
-------------------------------------------------------------------------------  

Project Name    : Skill Rag Clustering  
File Name       : user_similarity_analyzer.py  
Author          : <Author Name>  
Created Date    : <Date>  
Version         : <Version>  
Description     : This script analyzes user similarity by extracting key-value pairs,  
                  computing embeddings, and determining similarity scores between users.  
                  It utilizes Dask for parallel computation and supports writing results  
                  to both files and MongoDB.

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

import random  # Import random for random sampling
import logging
import numpy as np
from dask import delayed, compute
from similarity_calculator import SimilarityCalculator
from file_writer import FileWriter
from mongodb_writer import MongoDBWriter
from embedding import EmbeddingHandler
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class UserSimilarityAnalyzer:
    excluded_keys = {"name", "phone", "contact", "mobile number", "email"}

    @staticmethod
    def generate_key_value_pairs(data, sample_size=5):
        """
        Generate key-value pairs from the nested dictionary structure, limited to a random sample of size per role.
        Excludes specific keys defined in excluded_keys.
        """
        key_value_pairs = []
        try:
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        key_value_pairs.extend(UserSimilarityAnalyzer.generate_key_value_pairs(item, sample_size))
            elif isinstance(data, dict):
                for module, roles_data in data.items():
                    if isinstance(roles_data, dict):
                        for role, role_data in roles_data.items():
                            if isinstance(role_data, list):
                                limited_role_data = random.sample(role_data, min(sample_size, len(role_data)))
                                role_index = len(key_value_pairs) + 1
                                for user_index, item in enumerate(limited_role_data, start=1):
                                    temp_item = {k: v for k, v in item.items() if k != 'id' and k.lower() not in UserSimilarityAnalyzer.excluded_keys}
                                    key_value_pairs.append((module, role, role_index, user_index, temp_item))
        except Exception as e:
            logger.error(f"Error generating key-value pairs: {e}")
        return key_value_pairs

    @staticmethod
    def _calculate_similarity_for_pair(pair1, all_key_value_pairs, embeddings_cache, nlp_model, threshold):
        """
        Calculate similarity scores for a pair of key-value pairs, excluding specified keys from consideration.
        """
        results = []
        module1, role1, role1_index, user1_index, user1 = pair1

        for module2, role2, role2_index, user2_index, user2 in all_key_value_pairs:
            if role1 == role2:
                continue  # Skip if the roles are the same

            for key1, value1 in user1.items():
                if key1.lower() in UserSimilarityAnalyzer.excluded_keys or not isinstance(value1, str):
                    continue
                for key2, value2 in user2.items():
                    if key2.lower() in UserSimilarityAnalyzer.excluded_keys or not isinstance(value2, str):
                        continue

                    embedding1 = SimilarityCalculator.get_word_embedding(value1, embeddings_cache, nlp_model)
                    embedding2 = SimilarityCalculator.get_word_embedding(value2, embeddings_cache, nlp_model)

                    if embedding1 is None or embedding2 is None or np.isnan(embedding1).any() or np.isnan(embedding2).any():
                        logger.warning(f"Skipping similarity calculation due to invalid embeddings: ({key1}, {key2})")
                        continue

                    similarity_score = SimilarityCalculator.calculate_cosine_similarity(embedding1, embedding2)
                    if similarity_score >= threshold:
                        results.append({
                            "user1": {"module": module1, "role": role1, "role_index": role1_index, "user_index": user1_index, "key": key1, "value": value1},
                            "user2": {"module": module2, "role": role2, "role_index": role2_index, "user_index": user2_index, "key": key2, "value": value2},
                            "similarity_score": float(similarity_score)
                        })
        return results

    @staticmethod
    def calculate_similarity_scores(all_key_value_pairs, embeddings_cache, nlp_model, output_filename, threshold):
        """
        Calculate similarity scores for all key-value pairs using Dask and write results to file.
        """
        results = []
        selected_similarity_count=0
        similarity_tasks = []
        try:
            for pair in all_key_value_pairs:
                task = delayed(UserSimilarityAnalyzer._calculate_similarity_for_pair)(
                    pair, all_key_value_pairs, embeddings_cache, nlp_model, threshold
                )
                similarity_tasks.append(task)
            task_results = compute(*similarity_tasks, scheduler='threads')
            for result in task_results:
                results.extend(result)
                selected_similarity_count+=len(result)
            FileWriter.write_similarity_scores(output_filename, results)
            FileWriter.write_similarity_count(output_filename, selected_similarity_count)
        except Exception as e:
            logger.error(f"Error calculating similarity scores: {e}")
        return results
