# import spacy
# from user_similarity_analyzer import UserSimilarityAnalyzer
# from key_comparator import find_comparable_keys_by_module, get_top_comparable_keys_by_module
# from config import get_env_variable  # Import configuration settings

# class SampleProfileMatching:
#     """Handles Step 1: Sample-based Profile Matching."""

#     def __init__(self, database):
#         self.database = database
#         self.collection = database[get_env_variable("COLLECTION_NAME", "modified_data")]
#         self.sample_size = int(get_env_variable("SAMPLE_SIZE", 5))
#         self.threshold = float(get_env_variable("THRESHOLD", 0.6))
#         self.user_similarity_analyzer = UserSimilarityAnalyzer()
#         self.nlp_model = spacy.load("en_core_web_md")

#     def execute(self):
#         """Perform sample profile matching and return top comparable keys."""
#         print("Executing Step 1: Sample Profile Matching...")
#         data = list(self.collection.find({}))
#         if not data:
#             raise Exception("No data found in MongoDB collection.")

#         sampled_key_value_pairs = self.user_similarity_analyzer.generate_key_value_pairs(
#             data, sample_size=self.sample_size
#         )

#         embeddings_cache = {}
#         similarity_data_sample = self.user_similarity_analyzer.calculate_similarity_scores(
#             sampled_key_value_pairs, embeddings_cache, self.nlp_model, "sample.json", self.threshold
#         )

#         comparable_keys_by_module = find_comparable_keys_by_module(similarity_data_sample, self.threshold)
#         return get_top_comparable_keys_by_module(comparable_keys_by_module, top_n=5)

import spacy
import logging
from user_similarity_analyzer import UserSimilarityAnalyzer
from key_comparator import find_comparable_keys_by_module, get_top_comparable_keys_by_module
from config import get_env_variable  # Import configuration settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SampleProfileMatching:
    """Handles Step 1: Sample-based Profile Matching."""

    def __init__(self, database, collection_name=None, sample_size=None, threshold=None):
        self.database = database
        self.collection = database[collection_name or get_env_variable("COLLECTION_NAME", "modified_data")]
        self.sample_size = sample_size or int(get_env_variable("SAMPLE_SIZE", 5))
        self.threshold = threshold or float(get_env_variable("THRESHOLD", 0.6))
        self.user_similarity_analyzer = UserSimilarityAnalyzer()
        self.nlp_model = spacy.load("en_core_web_md")

    def execute(self):
        """Perform sample profile matching and return top comparable keys."""
        logger.info("🔹 Executing Step 1: Sample Profile Matching...")
        
        try:
            data = list(self.collection.find({}))
            if not data:
                raise ValueError("❌ No data found in MongoDB collection.")
            
            logger.info(f"✅ Retrieved {len(data)} records from MongoDB.")

            # Generate key-value pairs for similarity analysis
            sampled_key_value_pairs = self.user_similarity_analyzer.generate_key_value_pairs(
                data, sample_size=self.sample_size
            )

            if not sampled_key_value_pairs:
                logger.warning("⚠️ No key-value pairs generated for similarity analysis.")
                return {}

            logger.info(f"✅ Generated {len(sampled_key_value_pairs)} key-value pairs.")

            # Compute similarity scores
            embeddings_cache = {}
            similarity_data_sample = self.user_similarity_analyzer.calculate_similarity_scores(
                sampled_key_value_pairs, embeddings_cache, self.nlp_model, "sample.json", self.threshold
            )

            if not similarity_data_sample:
                logger.warning("⚠️ No similarity scores computed. Skipping further processing.")
                return {}

            logger.info(f"✅ Computed similarity scores for {len(similarity_data_sample)} key-value pairs.")

            # Find top comparable keys
            comparable_keys_by_module = find_comparable_keys_by_module(similarity_data_sample, self.threshold)
            top_keys = get_top_comparable_keys_by_module(comparable_keys_by_module, top_n=5)

            logger.info("✅ Sample profile matching step completed successfully.")
            return top_keys

        except Exception as e:
            logger.error(f"❌ Error during Sample Profile Matching: {e}", exc_info=True)
            return {}
