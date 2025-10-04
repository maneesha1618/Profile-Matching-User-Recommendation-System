"""===============================================================================  
                               GoFreeLab Proprietary  
-------------------------------------------------------------------------------  

Project Name    : Skill RAG Clustering  
File Name       : ranking_and_clustering.py  
Author          : <Author Name>  
Created Date    : <Date>  
Version         : <Version>  
Description     : This script processes similarity results by grouping them based on  
                  user modules, ranking them in descending order by similarity scores,  
                  and applying KMeans clustering to categorize results into a specified  
                  number of clusters. The clusters are then reordered based on their  
                  average similarity scores to ensure meaningful grouping. This enables  
                  structured and efficient organization of similarity profiles for  
                  further analysis.  

-------------------------------------------------------------------------------  
Copyright (c) 2025 GoFreeLab. All rights reserved.  

This source code and all its contents are the proprietary property of GoFreeLab.  
Unauthorized copying, sharing, or distribution of this code, in whole or in part,  
via any medium is strictly prohibited without prior written permission from GoFreeLab.  

This software is for use only by employees, contractors, or partners of GoFreeLab  
with explicit authorization.  

For questions or permissions, please contact: info@gofreelab.com  
===============================================================================  
"""  
import numpy as np
import logging
from typing import List, Dict, Any
from config import get_env_variable  # Import from config.py

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class RankingAndClustering:
    """Class to handle ranking and clustering of similarity results by module."""

    @staticmethod
    def convert_numpy_types(obj):
        """
        Recursively convert numpy types in a given object to native Python types.
        """
        if isinstance(obj, np.generic):
            return obj.item()
        elif isinstance(obj, dict):
            return {k: RankingAndClustering.convert_numpy_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [RankingAndClustering.convert_numpy_types(x) for x in obj]
        else:
            return obj

    @staticmethod
    def rank_and_cluster_by_module(similarity_results: List[Dict[str, Any]]) -> Dict[str, Dict[int, List[Dict[str, Any]]]]:
        
        
        num_clusters = int(get_env_variable("NUM_CLUSTERS", 6))  # Load cluster count from config

        if not similarity_results:
            logger.warning("No similarity results provided for ranking and clustering by module.")
            return {}

        # Filter out results without a 'similarity_score' key
        filtered_results = [res for res in similarity_results if "similarity_score" in res]

        if len(filtered_results) < len(similarity_results):
            logger.warning(f"Filtered out {len(similarity_results) - len(filtered_results)} results without a 'similarity_score' key.")

        # Group results by module
        grouped_results = {}
        for result in filtered_results:
            module = result.get("user1", {}).get("module", "Unknown")  # Avoid KeyError
            grouped_results.setdefault(module, []).append(result)

        module_clusters = {}
        for module, results in grouped_results.items():
            # Sort results by similarity_score in descending order
            sorted_results = sorted(results, key=lambda x: x.get("similarity_score", 0), reverse=True)
            logger.info(f"Module '{module}' has {len(sorted_results)} similarity results after sorting.")

            # Ensure at least one cluster per module
            cluster_size = max(len(sorted_results) // num_clusters, 1)  
            clusters = {i: [] for i in range(num_clusters)}

            for idx, res in enumerate(sorted_results):
                cluster_id = min(idx // cluster_size, num_clusters - 1)  # Ensure max cluster index is num_clusters - 1
                clusters[cluster_id].append(res)

            module_clusters[module] = clusters

            # Log cluster assignments with average similarity score
            for label, cluster in clusters.items():
                avg_sim = np.mean([p["similarity_score"] for p in cluster]) if cluster else 0
                logger.info(f"Module '{module}', Cluster {label} (Avg Sim: {avg_sim:.3f}) contains {len(cluster)} profiles.")

        return module_clusters
