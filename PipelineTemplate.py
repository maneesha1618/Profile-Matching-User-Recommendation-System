from abc import ABC, abstractmethod
import time
import logging

class PipelineTemplate(ABC):
    """Template Method Pattern for executing user profile matching and clustering."""

    def run_pipeline(self):
        """Template method that defines the pipeline execution steps."""
        start_time = time.time()
        print("Pipeline execution started...")

        try:
            self.step1_sample_profile_matching()
            self.step2_full_profile_matching()
            self.step3_ranking_and_clustering()
        except Exception as e:
            logging.error(f"An error occurred during execution: {e}", exc_info=True)
        finally:
            self.cleanup()
            end_time = time.time()
            print(f"Total Execution Time: {end_time - start_time:.2f} seconds")

    @abstractmethod
    def step1_sample_profile_matching(self):
        """Step 1: Perform sample profile matching."""
        pass

    @abstractmethod
    def step2_full_profile_matching(self):
        """Step 2: Perform full profile matching."""
        pass

    @abstractmethod
    def step3_ranking_and_clustering(self):
        """Step 3: Perform ranking and clustering."""
        pass

    @abstractmethod
    def cleanup(self):
        """Clean up resources like database connections."""
        pass
