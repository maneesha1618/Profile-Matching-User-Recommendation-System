"""
===============================================================================  
                             GoFreeLab Proprietary  
-------------------------------------------------------------------------------  

Project Name    : Skill Rag Clustering  
File Name       : file_writer.py  
Author          : <Author Name>  
Created Date    : <Date>  
Version         : <Version>  
Description     : This script handles writing similarity scores and similarity  
                  counts to JSON files. It includes error handling for file  
                  operations and ensures proper data structure management.  

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
import json

class FileWriter:
    @staticmethod
    def write_similarity_scores(output_filename, results):
        try:
            with open(output_filename, "w") as file:
                json.dump(results, file, indent=4)
        except Exception as e:
            print(f"Error writing similarity scores to file {output_filename}: {e}")

    @staticmethod
    def write_similarity_count(output_filename, selected_similarity_count):
        try:
            # Try to read the existing JSON file, if it exists.
            try:
                with open(output_filename, "r") as file:
                    data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                # If the file doesn't exist or is empty, initialize an empty list.
                data = []

            # Add the similarity count.
            data.append({"selected_similarity_count": selected_similarity_count})

            # Write the updated JSON back to the file.
            with open(output_filename, "w") as file:
                json.dump(data, file, indent=4)

        except Exception as e:
            print(f"Error writing similarity count to file {output_filename}: {e}")
    
    @staticmethod
    def write_clusters(clusters, filename):
        """
        Write the clusters dictionary to a JSON file and print the cluster details.
        """
        try:
            with open(filename, "w") as f:
                json.dump(clusters, f, indent=4, default=str)
            print(f"Cluster details written to {filename}")
            
            # Optionally, print out the clusters.
            for module, cluster_dict in clusters.items():
                print(f"\nModule: {module}")
                for label, profiles in cluster_dict.items():
                    print(f"  Cluster {label} contains {len(profiles)} profiles:")
                    for profile in profiles:
                        print(f"    User pair: {profile['user1']} - {profile['user2']}, Score: {profile['similarity_score']}")
        except Exception as e:
            print(f"Error writing clusters to file {filename}: {e}")
