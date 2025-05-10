import pandas as pd
from pymongo import MongoClient
from pymongo.collection import Collection
import os
import shutil



def get_mongo_collection():
    try:
        # MongoDB connection details
        MONGO_HOST = os.getenv("MONGO_HOST", "mongo" if os.getenv("DOCKER_ENV") else "localhost")
        MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
        MONGO_DB = os.getenv("MONGO_DB", "sensor_data")  # Match docker-compose.yml

        # Connect to MongoDB without authentication
        client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")
        db = client[MONGO_DB]
        return db["sensors"]
    
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise
    


def process_csv_file(file_path: str, collection: Collection):
    # List of required columns in the CSV
    required_columns = ["ts", "device", "co", "humidity", "light", "lpg", "motion", "smoke", "temp"]
    
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Check if all required columns are present
        if not all(col in df.columns for col in required_columns):
            print(f"Missing required columns in {os.path.basename(file_path)}. Skipping this file.")
            return False  # Skip processing if columns are missing

    except Exception as e:
        print(f"Error reading {os.path.basename(file_path)}: {e}")
        return False

    # Convert CSV rows to dictionary format
    raw_data = df.to_dict(orient="records")
    
    # Insert data into MongoDB
    if raw_data:
        collection.insert_many(raw_data)
        print(f"Inserted {len(raw_data)} records from {os.path.basename(file_path)} into MongoDB.")
        return True
    else:
        print(f"No data found in {os.path.basename(file_path)}, skipping insertion.")
        return False
    

def move_file_to_folder(file_path, target_folder):
    # Ensure Inserted_data folder exists
    try:
        os.makedirs(target_folder, exist_ok=True)
        shutil.move(file_path, os.path.join(target_folder, os.path.basename(file_path)))
        print(f"Moved {os.path.basename(file_path)} to {target_folder}.")
    except Exception as e:
        print(f"Failed to move file {os.path.basename(file_path)}: {e}")


def process_all_files(new_data_folder="new_data", inserted_data_folder="Inserted_data"):
    try:
        collection = get_mongo_collection()
    except Exception:
        print("Terminating due to database connection issue.")
        return

    for filename in os.listdir(new_data_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(new_data_folder, filename)
            if process_csv_file(file_path, collection):
                move_file_to_folder(file_path, inserted_data_folder)


def main():
    process_all_files()
    print("All files processed.")


if __name__ == "__main__":
    main()



