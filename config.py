"""
===============================================================================  
                             GoFreeLab Proprietary  
-------------------------------------------------------------------------------  

Project Name    : Skill Rag Clustering  
File Name       : config.py  
Author          : <Author Name>  
Created Date    : <Date>  
Version         : <Version>  
Description     : This script loads environment variables from a .env file and  
                  provides a utility function to retrieve configuration values  
                  with optional default handling.  

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

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def get_env_variable(name: str, default=None, required=True):
    """Fetches an environment variable with an optional default value.
    
    Args:
        name (str): The name of the environment variable.
        default (str | None): The default value if the variable is not found.
        required (bool): Whether the variable is mandatory.

    Returns:
        str: The value of the environment variable.

    Raises:
        ValueError: If the required variable is missing.
    """
    value = os.getenv(name, default)
    if required and value is None:
        raise ValueError(f"❌ Missing required environment variable: {name}")
    return value

# Load database configurations
MONGO_URI = get_env_variable("MONGO_URI")
DB_NAME = get_env_variable("DB_NAME")
COLLECTION_NAME = get_env_variable("COLLECTION_NAME", "modified_data", required=False)
COLLECTION_NAME_OUT = get_env_variable("COLLECTION_NAME_OUT", "sample_001", required=False)
VECTOR_COLLECTION = get_env_variable("vECTOR_COLLECTION", "sample_002", required=False)

# Load processing settings
THRESHOLD = float(get_env_variable("THRESHOLD", "0.6", required=False))
SAMPLE_SIZE = int(get_env_variable("SAMPLE_SIZE", "5", required=False))
NUM_CLUSTERS = int(get_env_variable("NUM_CLUSTERS", "6", required=False))
