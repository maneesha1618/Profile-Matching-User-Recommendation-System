from user2 import UserSimilarityAnalyzerFull
from mongodb_writer import MongoDBWriter
from embedding import EmbeddingHandler
from config import get_env_variable  

class FullProfileMatching:
    """Handles Step 2: Full dataset profile matching."""

    def __init__(self, database, collection_name_out, top_comparable_keys, threshold):
        """Initialize FullProfileMatching with necessary configurations."""
        self.database = database
        self.collection_name_out = collection_name_out  # Now passed as an argument
        self.vector_collection = get_env_variable("VECTOR_COLLECTION", "vector_1")
        self.threshold = threshold  # Now passed as an argument
        self.top_comparable_keys = top_comparable_keys
        self.user_similarity_analyzer_full = UserSimilarityAnalyzerFull()
        self.mongo_writer = MongoDBWriter()
        self.embedding_handler = EmbeddingHandler()

    def execute(self):
        """Perform full profile matching."""
        print("Executing Step 2: Full Profile Matching...")
        self.user_similarity_analyzer_full.initialize_allowed_keys(self.top_comparable_keys)
        
        data = list(self.database[get_env_variable("COLLECTION_NAME", "modified_data")].find({}))
        all_key_value_pairs = self.user_similarity_analyzer_full.generate_key_value_pairs_full(data)

        self.user_similarity_analyzer_full.calculate_similarity_scores_full(
            all_key_value_pairs, {}, None, self.collection_name_out, self.threshold,
            self.mongo_writer, self.embedding_handler, self.database, self.vector_collection
        )
