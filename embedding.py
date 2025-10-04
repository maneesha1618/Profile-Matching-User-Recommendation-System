"""
===============================================================================  
                             GoFreeLab Proprietary  
-------------------------------------------------------------------------------  

Project Name    : Skill Rag Clustering  
File Name       : embedding.py  
Author          : <Author Name>  
Created Date    : <Date>  
Version         : <Version>  
Description     : This script handles text vectorization using SpaCy and  
                  Sentence-BERT. It supports lazy loading of models, caching  
                  embeddings for efficiency, and includes error handling for  
                  embedding generation failures.  

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
import numpy as np
import spacy
from sentence_transformers import SentenceTransformer

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class EmbeddingHandler:
    _nlp = None
    _sentence_bert = None
    _embeddings_cache = {}

    @staticmethod
    def load_spacy_model():
        """Lazy load SpaCy model."""
        if EmbeddingHandler._nlp is None:
            try:
                EmbeddingHandler._nlp = spacy.load("en_core_web_md")
                logger.info("SpaCy model loaded successfully.")
            except Exception as e:
                logger.error(f"Error loading SpaCy model: {e}")

    @staticmethod
    def load_sentence_bert_model():
        """Lazy load Sentence-BERT model."""
        if EmbeddingHandler._sentence_bert is None:
            try:
                EmbeddingHandler._sentence_bert = SentenceTransformer("all-MiniLM-L6-v2")
                logger.info("Sentence-BERT model loaded successfully.")
            except Exception as e:
                logger.error(f"Error loading Sentence-BERT model: {e}")

    @staticmethod
    def get_word_embedding(text):
        """Retrieve word embeddings using SpaCy."""
        EmbeddingHandler.load_spacy_model()
        if not isinstance(text, str) or not text.strip():
            logger.warning("Invalid or empty text for word embedding.")
            return None
        if text in EmbeddingHandler._embeddings_cache:
            return EmbeddingHandler._embeddings_cache[text]
        try:
            vector = EmbeddingHandler._nlp(text).vector
            if np.isnan(vector).any():
                logger.error(f"NaN detected in word embedding for text: {text}")
                return None
            EmbeddingHandler._embeddings_cache[text] = vector
            return vector
        except Exception as e:
            logger.error(f"Error generating word embedding for text '{text}': {e}")
            return None

    @staticmethod
    def get_sentence_bert_embedding(text):
        """Retrieve sentence embeddings using Sentence-BERT."""
        EmbeddingHandler.load_sentence_bert_model()
        if not isinstance(text, str) or not text.strip():
            logger.warning("Invalid or empty text for sentence embedding.")
            return None
        if text in EmbeddingHandler._embeddings_cache:
            return EmbeddingHandler._embeddings_cache[text]
        try:
            vector = EmbeddingHandler._sentence_bert.encode(text, convert_to_numpy=True)
            if np.isnan(vector).any():
                logger.error(f"NaN detected in sentence embedding for text: {text}")
                return None
            EmbeddingHandler._embeddings_cache[text] = vector
            return vector
        except Exception as e:
            logger.error(f"Error generating sentence embedding for text '{text}': {e}")
            return None
