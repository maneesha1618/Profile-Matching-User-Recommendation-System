# Skill RAG Clustering

The previous code before converting into template method (as per instructions given in the last review) is in the branch (maneesha_user)

## Overview

Skill RAG Clustering is designed to analyze user data, calculate similarity scores between users based on selected attributes, and store the results in a MongoDB database. These similarity results are then retrieved from MongoDB, and candidates are clustered within modules based on their similarity scores. The system leverages advanced text vectorization techniques for embeddings andcompute similarity scores, enabling effective recommendations based on user characteristics. Additionally, clustering techniques are applied to group similar candidates for further analysis.

## Features
- Data extraction and preprocessing from MongoDB.
- Text vectorization using SpaCy and Sentence-BERT.
- Similarity analysis using cosine similarity and other NLP techniques.
- Ranking and clustering using KMeans.
- Results storage.

## Technologies Used
- Python
- MongoDB (for data storage)
- SpaCy & Sentence-BERT (for text embeddings)
- KMeans Clustering (for grouping users within the module)
- JSON (for output storage)
- Dask (for parallel computing)
- Logging module
- dotenv (for environment variable management)

## Installation
  
  1. Clone the repository:
        git clone https://gitlab.com/anseljanson/skill-rag-clustering.git
        cd <repository-directory>
        git remote add origin https://gitlab.com/anseljanson/skill-rag-clustering.git
        git branch -M main
        git push -uf origin main

2. Create a virtual environment (optional but recommended):

        python -m venv env
        source env/bin/activate  
        # On Windows use venv\Scripts\activate

3. Inatall required packages
        pip install -r requirements.txt

4. Set up your MongoDB database

        To use this application, you need a MongoDB instance running. Follow these steps to set it up:
        Install MongoDB:
            If you don't have MongoDB installed, download and install it from the MongoDB Download Center. Follow the installation instructions for your operating system.
        
        Start the MongoDB Server:
            After installation, start the MongoDB server. Open a terminal (or command prompt) and run:

                mongodb

5. Create a .envfile:
        MONGO_URI=mongodb+srv://freego:freego%2322Monkey@freego-c0.y47x2e3.mongodb.net/user_recommendation?retryWrites=true&w=majority
        DB_NAME=skill_rag_clustering
        COLLECTION_NAME=modified_data
        COLLECTION_NAME_OUT=modified_out
        VECTOR_COLLECTION=vector_1
        OUTPUT_FILENAME=sample.json
        THRESHOLD=0.6
        SAMPLE_SIZE=10
        NUM_CLUSTERS=6
        FULL_SIMILARITY_OUTPUT=final.json


## Usage
To run the skill rag clustering, execute the following command:

```bash
python main.py
```
This script will:
1. Connect to MongoDB and fetch users data.
2. Perform similarity calculations between profiles.
3. Store results in MongoDB
3. Rank and cluster the profiles.
4. Store results in MongoDB and output to a JSON file.

### Output Files
- `clusters.json`: Contains the clustering results.

- `sample.json`: Stores sample similarity results.
- mongodb : stores similarity results of full users


## File Structure
```
skill-rag-clustering/
│-- main.py                     # Main execution script
│-- SkillRAGPipeline.py         # Skill-based retrieval and generation pipeline
│-- PipelineTemplate.py         # Base template for pipeline execution
│-- SampleProfileMatching.py    # Sample profile matching logic
│-- FullProfileMatching.py      # Full-scale profile matching module
│-- RankingClustering.py        # Ranking and clustering module
│-- config.py                   # Configuration settings
│-- SkillRAGPipeline/           # SkillRAGPipeline module directory
│-- PipelineTemplate/           # Pipeline template module directory
│-- db.py                       # MongoDB connection handling
│-- data_processor.py           # Data extraction and preprocessing
│-- embedding.py                # Text vectorization module
│-- user_similarity_analyzer.py  # Similarity computation
│-- key_comparator.py           # Finds the top comparable keys
│-- user2.py                    # Full similarity analysis module
│-- ranking_and_clustering.py    # KMeans ranking and clustering
│-- file_writer.py              # Handles writing output files
│-- mongodb_writer.py           # Writes results to MongoDB
│-- .env                        # Environment variables
│-- requirements.txt            # Python dependencies
│-- README.md                   # Project documentation

```

## Environment Variables (.env)
Ensure that the `.env` file includes the following:
```
MONGO_URI=mongodb://your-mongodb-uri
DB_NAME=your-database-name
COLLECTION_NAME=modified_data
COLLECTION_NAME_OUT=modified_data
COLLECTION_OUT=vector_1
OUTPUT_FILENAME=sample.json
FULL_SIMILARITY_OUTPUT=final.json
THRESHOLD=0.6
SAMPLE_SIZE=5
```

## Contributing
1. Fork the repository.
2. Create a new branch (`feature-branch`).
3. Commit your changes.
4. Push to the branch and create a pull request.

## License
This project is licensed under the MIT License.

## Contact
For queries, reach out to `your-email@example.com` or open an issue on GitHub.

# Skill RAG Clustering

## Overview

Skill RAG Clustering is designed to analyze user data, calculate similarity scores between users based on selected attributes, and store the results in a MongoDB database. These similarity results are then retrieved from MongoDB, and candidates are clustered within modules based on their similarity scores. The system leverages advanced text vectorization techniques for embeddings andcompute similarity scores, enabling effective recommendations based on user characteristics. Additionally, clustering techniques are applied to group similar candidates for further analysis.

## Features
- Data extraction and preprocessing from MongoDB.
- Text vectorization using SpaCy and Sentence-BERT.
- Similarity analysis using cosine similarity and other NLP techniques.
- Ranking and clustering using KMeans.
- Results storage and visualization.

## Technologies Used
- Python
- MongoDB (for data storage)
- SpaCy & Sentence-BERT (for text embeddings)
- KMeans Clustering (for grouping users within the module)
- JSON (for output storage)
- Dask (for parallel computing)
- Logging module
- dotenv (for environment variable management)

## Installation
  
  1. Clone the repository:
        git clone https://gitlab.com/anseljanson/skill-rag-clustering.git
        cd <repository-directory>
        git remote add origin https://gitlab.com/anseljanson/skill-rag-clustering.git
        git branch -M main
        git push -uf origin main

2. Create a virtual environment (optional but recommended):

        python -m venv env
        source env/bin/activate  
        # On Windows use venv\Scripts\activate

3. Inatall required packages
        pip install -r requirements.txt

4. Set up your MongoDB database

        To use this application, you need a MongoDB instance running. Follow these steps to set it up:
        Install MongoDB:
            If you don't have MongoDB installed, download and install it from the MongoDB Download Center. Follow the installation instructions for your operating system.
        
        Start the MongoDB Server:
            After installation, start the MongoDB server. Open a terminal (or command prompt) and run:

                mongodb

5. Create a .envfile:
        MONGO_URI=mongodb+srv://freego:freego%2322Monkey@freego-c0.y47x2e3.mongodb.net/user_recommendation?retryWrites=true&w=majority
        DB_NAME=skill_rag_clustering
        COLLECTION_NAME=modified_data
        COLLECTION_NAME_OUT=modified_out
        VECTOR_COLLECTION=vector_1
        OUTPUT_FILENAME=sample.json
        THRESHOLD=0.6
        SAMPLE_SIZE=10
        NUM_CLUSTERS=6
        FULL_SIMILARITY_OUTPUT=final.json


## Usage
To run the skill rag clustering, execute the following command:

```bash
python main.py
```
This script will:
1. Connect to MongoDB and fetch users data.
2. Perform similarity calculations between profiles.
3. Store results in MongoDB
3. Rank and cluster the profiles.
4. Store results in MongoDB and output to a JSON file.

### Output Files
- `clusters.json`: Contains the clustering results.
- `sample.json`: Stores sample similarity results.
- mongodb : stores similarity results of full users


## File Structure
```
skill-rag-clustering/
│-- main.py                 # Main execution script
│-- db.py                   # MongoDB connection handling
│-- data_processor.py       # Data extraction and preprocessing
│-- embedding.py            # Text vectorization module
│-- user_similarity_analyzer.py  # Similarity computation
│-- user2.py                # Full similarity analysis module
│-- ranking_and_clustering.py  # KMeans ranking and clustering
│-- file_writer.py          # Handles writing output files
│-- mongodb_writer.py       # Writes results to MongoDB
│-- .env                    # Environment variables
│-- requirements.txt        # Python dependencies
│-- README.md               # Project documentation
```

## Environment Variables (.env)
Ensure that the `.env` file includes the following:
```
MONGO_URI=mongodb://your-mongodb-uri
DB_NAME=your-database-name
COLLECTION_NAME=modified_data
COLLECTION_NAME_OUT=modified_data
COLLECTION_OUT=vector_1
OUTPUT_FILENAME=sample.json
FULL_SIMILARITY_OUTPUT=final.json
THRESHOLD=0.6
SAMPLE_SIZE=5
```

## Contributing
1. Fork the repository.
2. Create a new branch (`feature-branch`).
3. Commit your changes.
4. Push to the branch and create a pull request.

## License
This project is licensed under the MIT License.

## Contact
For queries, reach out to `your-email@example.com` or open an issue on GitHub.

# Skill RAG Clustering

## Overview

Skill RAG Clustering is designed to analyze user data, calculate similarity scores between users based on selected attributes, and store the results in a MongoDB database. These similarity results are then retrieved from MongoDB, and candidates are clustered within modules based on their similarity scores. The system leverages advanced text vectorization techniques for embeddings andcompute similarity scores, enabling effective recommendations based on user characteristics. Additionally, clustering techniques are applied to group similar candidates for further analysis.

## Features
- Data extraction and preprocessing from MongoDB.
- Text vectorization using SpaCy and Sentence-BERT.
- Similarity analysis using cosine similarity and other NLP techniques.
- Ranking and clustering using KMeans.
- Results storage and visualization.

## Technologies Used
- Python
- MongoDB (for data storage)
- SpaCy & Sentence-BERT (for text embeddings)
- KMeans Clustering (for grouping users within the module)
- JSON (for output storage)
- Dask (for parallel computing)
- Logging module
- dotenv (for environment variable management)

## Installation
  
  1. Clone the repository:
        git clone https://gitlab.com/anseljanson/skill-rag-clustering.git
        cd <repository-directory>
        git remote add origin https://gitlab.com/anseljanson/skill-rag-clustering.git
        git branch -M main
        git push -uf origin main

2. Create a virtual environment (optional but recommended):

        python -m venv env
        source env/bin/activate  
        # On Windows use venv\Scripts\activate

3. Inatall required packages
        pip install -r requirements.txt

4. Set up your MongoDB database

        To use this application, you need a MongoDB instance running. Follow these steps to set it up:
        Install MongoDB:
            If you don't have MongoDB installed, download and install it from the MongoDB Download Center. Follow the installation instructions for your operating system.
        
        Start the MongoDB Server:
            After installation, start the MongoDB server. Open a terminal (or command prompt) and run:

                mongodb

5. Create a .envfile:
        MONGO_URI=mongodb+srv://freego:freego%2322Monkey@freego-c0.y47x2e3.mongodb.net/user_recommendation?retryWrites=true&w=majority
        DB_NAME=skill_rag_clustering
        COLLECTION_NAME=modified_data
        COLLECTION_NAME_OUT=modified_out
        VECTOR_COLLECTION=vector_1
        OUTPUT_FILENAME=sample.json
        THRESHOLD=0.6
        SAMPLE_SIZE=10
        NUM_CLUSTERS=6
        FULL_SIMILARITY_OUTPUT=final.json


## Usage
To run the skill rag clustering, execute the following command:

```bash
python main.py
```
This script will:
1. Connect to MongoDB and fetch users data.
2. Perform similarity calculations between profiles.
3. Store results in MongoDB
3. Rank and cluster the profiles.
4. Store results in MongoDB and output to a JSON file.

### Output Files
- `clusters.json`: Contains the clustering results.
- `sample.json`: Stores sample similarity results.
- mongodb : stores similarity results of full users


## File Structure
```
skill-rag-clustering/
│-- main.py                 # Main execution script
│-- db.py                   # MongoDB connection handling
│-- data_processor.py       # Data extraction and preprocessing
│-- embedding.py            # Text vectorization module
│-- user_similarity_analyzer.py  # Similarity computation
│-- user2.py                # Full similarity analysis module
│-- ranking_and_clustering.py  # KMeans ranking and clustering
│-- file_writer.py          # Handles writing output files
│-- mongodb_writer.py       # Writes results to MongoDB
│-- .env                    # Environment variables
│-- requirements.txt        # Python dependencies
│-- README.md               # Project documentation
```

## Environment Variables (.env)
Ensure that the `.env` file includes the following:
```
MONGO_URI=mongodb://your-mongodb-uri
DB_NAME=your-database-name
COLLECTION_NAME=modified_data
COLLECTION_NAME_OUT=modified_data
COLLECTION_OUT=vector_1
OUTPUT_FILENAME=sample.json
FULL_SIMILARITY_OUTPUT=final.json
THRESHOLD=0.6
SAMPLE_SIZE=5
```

## Contributing
1. Fork the repository.
2. Create a new branch (`feature-branch`).
3. Commit your changes.
4. Push to the branch and create a pull request.

## Logging

The application uses Python's built-in logging module to log the progress and any errors encountered during execution. Logs will be printed to the console, making it easier to monitor the system's operation.

## Errorr Handling
The application includes basic error handling to manage exceptions that may arise during data fetching, processing, or writing to MongoDB. Errors will be logged appropriately.

## Contribution
Feel free to contribute to the project by submitting issues or pull requests. Your feedback and enhancements are welcome!

