
import time
import spacy
from dotenv import load_dotenv
import os
from data_processor import DataProcessor
from user_similarity_analyzer import UserSimilarityAnalyzer
from user2 import UserSimilarityAnalyzerFull
from key_comparator import find_comparable_keys_by_module, get_top_comparable_keys_by_module

def main():
    load_dotenv()

    start_time = time.time()

    # MongoDB connection details from environment variables
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME")
    collection_name = os.getenv("COLLECTION_NAME", "user_match")
    collection_name_out = os.getenv("COLLECTION_NAME_OUT", "user_match_out")
    output_filename_sample = os.getenv("OUTPUT_FILENAME", "outputmatchfinal_sample.json")
    output_filename_full = os.getenv("FULL_SIMILARITY_OUTPUT", "final_similarity_results.json")
    threshold = float(os.getenv("THRESHOLD", 0.6))
    sample_size = int(os.getenv("SAMPLE_SIZE", 5))

    # Initialize the DataProcessor with the connection details
    data_processor = DataProcessor(mongo_uri, db_name, collection_name)
    user_similarity_analyzer = UserSimilarityAnalyzer()
    user_similarity_analyzer_full = UserSimilarityAnalyzerFull()

    try:
        # Fetch data from MongoDB
        data = data_processor.fetch_data()
        nlp_model = spacy.load("en_core_web_md")

        ### Step 1: Sample Data and Perform Key Comparison ###

        sampled_key_value_pairs = user_similarity_analyzer.generate_key_value_pairs(data, sample_size=sample_size)
        embeddings_cache = {}
        
        # Calculate similarity scores for the sampled data
        similarity_data_sample = user_similarity_analyzer.calculate_similarity_scores(
            sampled_key_value_pairs, embeddings_cache, nlp_model, output_filename_sample, threshold
        )
        
        # Perform key comparison
        comparable_keys_by_module = find_comparable_keys_by_module(similarity_data_sample, threshold)
        top_comparable_keys = get_top_comparable_keys_by_module(comparable_keys_by_module, top_n=5)

        ### Step 2: Load Allowed Keys and Perform Full Similarity Analysis ###

        user_similarity_analyzer_full.initialize_allowed_keys(top_comparable_keys)
        all_key_value_pairs = user_similarity_analyzer_full.generate_key_value_pairs_full(data)

        # Calculate similarity scores for the full data using the allowed keys
        user_similarity_analyzer_full.calculate_similarity_scores_full(
            all_key_value_pairs, embeddings_cache, nlp_model, mongo_uri, db_name, collection_name_out, threshold
        )

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        data_processor.close_connection()
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Total Execution Time: {execution_time:.2f} seconds")

if __name__ == "__main__":
    main()


