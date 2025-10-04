"""
===============================================================================
                             GoFreeLab Proprietary  
-------------------------------------------------------------------------------

Project Name    : Skill RAG Clustering  
File Name       : user2.py  
Author          : <Author Name>  
Created Date    : <Date>  
Version         : <Version>  
Description     : This script analyzes user similarity by extracting key-value pairs,  
                  computing embeddings, and determining similarity scores between users.  
                  It utilizes Dask for parallel computation and supports writing results  
                  to both files and MongoDB. Additionally, it integrates both word-based  
                  and sentence-based embeddings for efficient similarity analysis.

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
from dask import delayed, compute
from similarity_calculator import SimilarityCalculator
from mongodb_writer import MongoDBWriter
from embedding import EmbeddingHandler
import numpy as np
from typing import List, Dict, Any
from db import store_vector_in_db  # Import the standalone function from db.py

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserSimilarityAnalyzerFull:
    allowed_keys = {}

    @staticmethod
    def initialize_allowed_keys(allowed_keys):
        """Set allowed keys for filtering user data."""
        UserSimilarityAnalyzerFull.allowed_keys = allowed_keys

    @staticmethod
    def _filter_keys(user_data, module, role):
        """Filter user data based on allowed keys."""
        allowed = UserSimilarityAnalyzerFull.allowed_keys.get(module, {}).get(role, [])
        return {key: value for key, value in user_data.items() if key in allowed}

    @staticmethod
    def generate_key_value_pairs_full(data):
        """Generate key-value pairs from the nested dictionary structure."""
        key_value_pairs = []
        try:
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        key_value_pairs.extend(UserSimilarityAnalyzerFull.generate_key_value_pairs_full(item))
            elif isinstance(data, dict):
                for module, roles_data in data.items():
                    if isinstance(roles_data, dict):
                        for role, role_data in roles_data.items():
                            if isinstance(role_data, list):
                                for user_index, item in enumerate(role_data, start=1):
                                    temp_item = UserSimilarityAnalyzerFull._filter_keys(item, module, role)
                                    key_value_pairs.append((module, role, None, user_index, temp_item))
        except Exception as e:
            logger.error(f"Error generating key-value pairs: {e}")
        return key_value_pairs

    @staticmethod
    def handle_value(value):
        """Ensure the value passed is a string for embeddings calculation; skip non-text or numeric values."""
        if isinstance(value, (int, float, str)) and str(value).isnumeric():
            logger.warning(f"Skipping numeric value: {value}")
            return None
        elif isinstance(value, list):
            return " ".join(map(str, value))
        elif isinstance(value, dict):
            return str(value)
        elif isinstance(value, (int, float)):
            return str(value)
        else:
            return value

    @staticmethod
    def _calculate_similarity_for_pair_full(pair, all_key_value_pairs, embeddings_cache, nlp_model, threshold, embedding_handler, database, vector_collection):
        """
        Calculate similarity scores for a pair of key-value pairs.
        Returns a dictionary with key 'similarity' containing all similarity result dictionaries.
        Both short text (long_text=False) and long text (long_text=True) similarity results are appended.
        """
        sim_results = []
        module1, role1, _, user1_index, user1 = pair
        user1_filtered = UserSimilarityAnalyzerFull._filter_keys(user1, module1, role1)

        logger.info(f"Checking pair: {pair}")

        for module2, role2, _, user2_index, user2 in all_key_value_pairs:
            user2_filtered = UserSimilarityAnalyzerFull._filter_keys(user2, module2, role2)
            # Process only if modules are the same but roles differ.
            if module1 == module2 and (role1 != role2 and user1_filtered and user2_filtered):
                for key1, raw_value1 in user1_filtered.items():
                    for key2, raw_value2 in user2_filtered.items():
                        # Preprocess values.
                        value1 = UserSimilarityAnalyzerFull.handle_value(raw_value1)
                        value2 = UserSimilarityAnalyzerFull.handle_value(raw_value2)
                        if value1 is None or value2 is None or not isinstance(value1, str) or not isinstance(value2, str):
                            logger.debug(f"Skipping pair due to invalid or numeric value: ({key1}, {key2})")
                            continue
                        # Trim texts.
                        value1 = value1.strip()
                        value2 = value2.strip()
                        if not value1 or not value2:
                            logger.warning(f"Empty text detected for keys ({key1}, {key2}). Skipping embedding.")
                            continue

                        # logger.info(f"Processing pair for keys ({key1}, {key2}).")
                        len_value1 = len(value1)
                        len_value2 = len(value2)

                        # Case 1: Both texts are short.
                        if len_value1 < 150 and len_value2 < 150:
                            try:
                                emb1 = embedding_handler.get_word_embedding(value1)
                                emb2 = embedding_handler.get_word_embedding(value2)
                                if emb1 is None or emb2 is None:
                                    logger.warning(f"One or both embeddings are None for pair ({key1}, {key2}).")
                                    continue
                                similarity_score = SimilarityCalculator.calculate_cosine_similarity(emb1, emb2)
                                if similarity_score is None:
                                    logger.warning(f"Similarity calculation returned None for pair ({key1}, {key2}).")
                                    continue
                                similarity_score = float(similarity_score)
                                if similarity_score >= threshold:
                                    sim_results.append({
                                        "user1": {"module": module1, "role": role1, "user_index": user1_index, "key": key1, "value": value1},
                                        "user2": {"module": module2, "role": role2, "user_index": user2_index, "key": key2, "value": value2},
                                        "similarity_score": similarity_score,
                                        "long_text": False
                                    })
                                    # logger.info(f"Short text similarity for pair ({key1}, {key2}): {similarity_score}")
                                else:
                                    logger.info(f"Short text similarity for pair ({key1}, {key2}) below threshold: {similarity_score}")
                            except Exception as e:
                                logger.error(f"Error calculating similarity for pair ({key1}, {key2}): {e}")
                        # Case 2: One or both texts are long.
                        elif len_value1 >= 150 and len_value2 >= 150:
                            try:
                                emb1 = embedding_handler.get_sentence_bert_embedding(value1)
                                emb2 = embedding_handler.get_sentence_bert_embedding(value2)
                                if emb1 is None or emb2 is None:
                                    logger.warning(f"One or both Sentence-BERT embeddings are None for pair ({key1}, {key2}).")
                                    continue
                                similarity_score = SimilarityCalculator.calculate_cosine_similarity(emb1, emb2)
                                if similarity_score is None:
                                    logger.warning(f"Long text similarity returned None for pair ({key1}, {key2}).")
                                    continue
                                similarity_score = float(similarity_score)
                                if similarity_score >= threshold:
                                    sim_results.append({
                                        "user1": {"module": module1, "role": role1, "user_index": user1_index, "key": key1, "value": value1},
                                        "user2": {"module": module2, "role": role2, "user_index": user2_index, "key": key2, "value": value2},
                                        "similarity_score": similarity_score,
                                        "long_text": True
                                    })
                                    # logger.info(f"Long text similarity for pair ({key1}, {key2}): {similarity_score}")
                                    # Build and store the combined document for long texts.
                                    combined_doc = {
                                        "text1": value1,
                                        "vector1": emb1.tolist() if hasattr(emb1, "tolist") else emb1,
                                        "text2": value2,
                                        "vector2": emb2.tolist() if hasattr(emb2, "tolist") else emb2
                                    }
                                    try:
                                        store_vector_in_db(combined_doc, database, vector_collection)
                                        # logger.info(f"Stored combined long text embedding document for pair ({key1}, {key2}).")
                                    except Exception as e:
                                        logger.error(f"Error storing combined long text document for pair ({key1}, {key2}): {e}")
                                else:
                                    logger.info(f"Long text similarity for pair ({key1}, {key2}) below threshold: {similarity_score}")
                            except Exception as e:
                                logger.error(f"Error processing long text similarity for pair ({key1}, {key2}): {e}")
        return {"similarity": sim_results}

    @staticmethod
    def calculate_similarity_scores_full(
        all_key_value_pairs: List[tuple],
        embeddings_cache: Dict[str, Any],
        nlp_model: Any,
        collection_name_out: str,
        threshold: float,
        mongo_writer: MongoDBWriter,
        embedding_handler: EmbeddingHandler,
        database: Any,           # Proper MongoDB database object
        vector_collection: str      # Collection name for combined long text embedding documents
    ) -> None:
        """
        Calculate similarity scores for all key-value pairs and write results to MongoDB.
        All similarity results (both short and long text) are written to collection_name_out.
        """
        overall_sim_results = []
        selected_similarity_count = 0
        similarity_tasks = []
        try:
            if not all_key_value_pairs:
                logger.warning("No key-value pairs to process.")
                return
            for pair in all_key_value_pairs:
                task = delayed(UserSimilarityAnalyzerFull._calculate_similarity_for_pair_full)(
                    pair, all_key_value_pairs, embeddings_cache, nlp_model, threshold, embedding_handler, database, vector_collection
                )
                similarity_tasks.append(task)
            task_results = compute(*similarity_tasks, scheduler='threads', num_workers=4)
            # Process each task's result.
            for result in task_results:
                if result:
                    sim_res = result.get("similarity", [])
                    if sim_res:
                        # logger.info(f"Writing {len(sim_res)} similarity results to collection: {collection_name_out}")
                        mongo_writer.write_similarity_scores(collection_name_out, sim_res)
                        for sim in sim_res:
                            overall_sim_results.append(sim)
                        selected_similarity_count += len(sim_res)
                else:
                    logger.warning("Received None result for similarity calculation.")
            mongo_writer.write_similarity_count(collection_name_out, selected_similarity_count)
            logger.info(f"Total similarity results written: {selected_similarity_count}")
        except Exception as e:
            logger.error(f"Error calculating similarity scores: {e}")




