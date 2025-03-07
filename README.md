# IoT Sensor Data Processing System

This project is designed to store environmental sensor data into a **MongoDB** database running inside a **Docker container**. The system processes CSV files placed in the `new_data` folder, inserts the data into the database, and moves the processed files into the `Inserted_data` folder.

## Setup Guide

### 1. Download the Files from GitHub
Clone the repository to your local machine:
```bash
git clone https://github.com/your-username/IU-Project-Data-Engineering.git
cd IU-Project-Data-Engineering
```

---

### 2. Create the Docker Container
Start a **MongoDB container** using Docker:
```bash
docker-compose up -d
```
This will create a MongoDB container running on port **27017**.

---

### 3. Create a Virtual Environment for the Python Script
Inside the project folder, create a ** Virtual environment**:
```bash
python -m venv venv
```
Activate the virtual environment:
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux**:
  ```bash
  source venv/bin/activate
  ```

---

### 4. Install Requirements for the Python Script
After activating the virtual environment, install the required dependencies:
```bash
pip install -r requirements.txt
```

---

### 5. Execute the Python Script
Run the Python script to process and insert data into MongoDB:
```bash
python main.py
```

---

### 6. Check if the Data Was Saved to the Container
Enter the MongoDB container shell:
```bash
docker exec -it mongodb-container mongosh
```
Once inside MongoDB, check the database:
```javascript
show dbs
use sensor_data
show collections
db.sensors.countDocuments()
db.sensors.findOne()
```
If you see records, the data has been successfully stored!

---

## Notes
- Ensure Docker Desktop is installed and running before starting.
- If the Python script fails, check for missing dependencies in `requirements.txt`.
- Ensure that any new CSV files are placed inside the new_data folder before running main.py.

