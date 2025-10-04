from db import connect_to_mongo
from PipelineTemplate import PipelineTemplate
from SampleProfileMatching import SampleProfileMatching
from FullProfileMatching import FullProfileMatching
from RankingClustering import RankingClustering
from data_processor import DataProcessor
import config  # Import the new config file

class SkillRAGPipeline(PipelineTemplate):
    """Concrete implementation of the Skill RAG Clustering pipeline."""

    def __init__(self):
        self.mongo_uri = config.MONGO_URI
        self.db_name = config.DB_NAME
        self.collection_name = config.COLLECTION_NAME
        self.collection_name_out = config.COLLECTION_NAME_OUT
        self.vector_collection = config.VECTOR_COLLECTION
        self.threshold = config.THRESHOLD
        self.sample_size = config.SAMPLE_SIZE
        self.database = connect_to_mongo(self.mongo_uri, self.db_name)
        self.top_comparable_keys = []  # Initialize to prevent potential errors

    def step1_sample_profile_matching(self):
        """Step 1: Perform sample profile matching."""
        print("🔹 Running Step 1: Sample Profile Matching...")
        sample_matcher = SampleProfileMatching(self.database, self.collection_name, self.sample_size, self.threshold)
        self.top_comparable_keys = sample_matcher.execute()
        
        if not self.top_comparable_keys:
            print("⚠ Warning: No comparable keys found in Step 1!")

    def step2_full_profile_matching(self):
        """Step 2: Perform full profile matching."""
        print("🔹 Running Step 2: Full Profile Matching...")
        
        if not self.top_comparable_keys:
            print("⚠ Warning: No comparable keys from Step 1. Skipping full profile matching.")
            return  # Skip Step 2 if no keys are found

        full_matcher = FullProfileMatching(self.database, self.collection_name_out, self.top_comparable_keys, self.threshold)
        full_matcher.execute()

    def step3_ranking_and_clustering(self):
        """Step 3: Perform ranking and clustering."""
        print("🔹 Running Step 3: Ranking and Clustering...")
        rank_cluster = RankingClustering(self.database, self.collection_name_out)
        rank_cluster.execute()

    def cleanup(self):
        """Close database connections and clean up resources."""
        print("🧹 Cleaning up resources...")
        data_processor = DataProcessor(self.mongo_uri, self.db_name, self.collection_name)
        data_processor.close_connection()
        print("✅ Cleanup complete!")
