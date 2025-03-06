import pandas as pd
from pymongo import MongoClient
import os
import shutil

# MongoDB connection details
MONGO_HOST = os.getenv("MONGO_HOST", "mongo" if os.getenv("DOCKER_ENV") else "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_DB = os.getenv("MONGO_DB", "sensor_data")  # Match docker-compose.yml

# Connect to MongoDB without authentication
client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")
db = client[MONGO_DB]
collection = db["sensors"]

# Define folder paths
new_data_folder = "new_data"
inserted_data_folder = "Inserted_data"

# Ensure Inserted_data folder exists
os.makedirs(inserted_data_folder, exist_ok=True)

# Process all CSV files in the new_data folder
for filename in os.listdir(new_data_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(new_data_folder, filename)
        
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Convert CSV rows to dictionary format
        data = df.to_dict(orient="records")
        
        # Insert data into MongoDB
        if data:
            collection.insert_many(data)
            print(f"Inserted {len(data)} records from {filename} into MongoDB.")
        else:
            print(f"No data found in {filename}, skipping insertion.")
        
        # Move the processed file to Inserted_data folder
        shutil.move(file_path, os.path.join(inserted_data_folder, filename))
        print(f"Moved {filename} to {inserted_data_folder}.")

print("All files processed.")


