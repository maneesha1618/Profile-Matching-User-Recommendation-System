import logging
from ranking_and_clustering import RankingAndClustering
from file_writer import FileWriter
from config import get_env_variable  

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class RankingClustering:
    """Handles Step 3: Ranking and Clustering."""

    def __init__(self, database, collection_name_out=None):
        """
        Initialize the RankingClustering class.

        Args:
            database: MongoDB database instance.
            collection_name_out: Name of the collection storing similarity results.
        """
        self.database = database
        self.collection_name_out = collection_name_out or get_env_variable("COLLECTION_NAME_OUT", "modified_data")
        self.num_clusters = int(get_env_variable("NUM_CLUSTERS", 6))  

    def execute(self):
        """Perform ranking and clustering of similarity results."""
        logger.info("🔹 Executing Step 3: Ranking and Clustering...")

        try:
            # Fetch similarity results from MongoDB
            collection = self.database[self.collection_name_out]
            final_similarity_results = list(collection.find({}))

            if not final_similarity_results:
                logger.warning(f"⚠️ No similarity results found in '{self.collection_name_out}'. Skipping ranking and clustering.")
                return

            # Convert NumPy types for compatibility
            final_similarity_results = RankingAndClustering.convert_numpy_types(final_similarity_results)

            # Rank and cluster results
            clusters = RankingAndClustering.rank_and_cluster_by_module(final_similarity_results)

            # Ensure cluster keys are string for JSON serialization
            clusters_clean = {str(module): {str(k): v for k, v in cluster_dict.items()} for module, cluster_dict in clusters.items()}

            # Save clusters to a JSON file
            FileWriter.write_clusters(clusters_clean, "clusters.json")
            logger.info(f"✅ Ranking and clustering completed successfully. Clusters saved to 'clusters.json'.")

        except Exception as e:
            logger.error(f"❌ Error during ranking and clustering: {e}", exc_info=True)
