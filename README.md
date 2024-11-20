# User Recommendation System

## Overview

This User Recommendation System is designed to analyze user data, calculate similarity scores between users based on selected attributes, and store the results in a MongoDB database. It leverages Natural Language Processing (NLP) techniques to compute similarity scores, allowing for effective recommendations based on user characteristics.

## Features

- Fetches user data from a MongoDB database.
- Calculates similarity scores using word embeddings.
- Performs sampling for efficient processing.
- Writes similarity scores and counts back to the MongoDB database.
- Configurable through environment variables for flexibility.

## Technologies Used

- Python
- MongoDB
- SpaCy (for NLP)
- Dask (for parallel computing)
- Logging module
- dotenv (for environment variable management)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://gitlab.com/anseljanson/candidate_interviewer_recommendation.git
   cd <repository-directory>
   git remote add origin https://gitlab.com/anseljanson/candidate_interviewer_recommendation.git
   git branch -M main
   git push -uf origin main
   ```
2. **Create a virtual environment (optional but recommended):**

    python -m venv env
    source env/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Inatall required packages**

    pip install -r requirements.txt

4. **Set up your MongoDB database**

To use this application, you need a MongoDB instance running. Follow these steps to set it up:

**Install MongoDB:**

   If you don't have MongoDB installed, download and install it from the [MongoDB Download Center](https://www.mongodb.com/try/download/community). Follow the installation instructions for your operating system.

**Start the MongoDB Server:**

   After installation, start the MongoDB server. Open a terminal (or command prompt) and run:

   ```bash
   mongodb
   ```

5. **Create a .envfile:**
    
    MONGO_URI=mongodb+srv://freego:freego%2322Monkey@freego-c0.y47x2e3.mongodb.net/user_recommendation?retryWrites=true&w=majority
    DB_NAME=freego
    COLLECTION_NAME=user_match
    COLLECTION_NAME_OUT=user_match
    OUTPUT_FILENAME=outputmatchfinal_sample.json
    FULL_SIMILARITY_OUTPUT=final_similarity_results.json
    THRESHOLD=0.6
    SAMPLE_SIZE=5

## Usage 
 
To run the recommendation system, execute the following command:

    python main.py

## Logging
The application uses Python's built-in logging module to log the progress and any errors encountered during execution. Logs will be printed to the console, making it easier to monitor the system's operation.

## Error Handling

The application includes basic error handling to manage exceptions that may arise during data fetching, processing, or writing to MongoDB. Errors will be logged appropriately.

## Contribution

Feel free to contribute to the project by submitting issues or pull requests. Your feedback and enhancements are welcome!

