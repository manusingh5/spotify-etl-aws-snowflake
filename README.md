# 🎧 Spotify ETL Pipeline

This project automates data extraction from the Spotify API, transforms it using AWS Glue (PySpark), and loads it into Snowflake using Snowpipe. The entire pipeline is event-driven and serverless.

---

## 🚀 Tech Stack

- **AWS Lambda** – Spotify API trigger
- **AWS S3** – Data lake (raw + transformed)
- **AWS Glue (PySpark)** – Data processing
- **Snowflake** – Data warehousing and ingestion via Snowpipe
- **GitHub** – Version control

---

## 📂 S3 Folder Structure
s3://spotify-etl-glue-project/
├── raw_data/
│ ├── to_processed/ ← Raw JSON files from Lambda
│ └── processed/ ← Moved here after Glue processing
│
├── transformed/
│ ├── songs_data/
│ ├── artist_data/
│ └── album_data/


📝 After Glue processing, files from `to_processed/` are archived to `processed/` to keep S3 clean.

---

## ⚙️ Workflow Overview

1. **Lambda function** fetches raw data and stores it in `raw_data/to_processed/`
2. **Glue job** transforms and writes it to `transformed/` in separate folders
3. **Snowpipe** auto-ingests each file to corresponding table in Snowflake

---

## 📁 Project Structure

spotify-etl-pipeline/
├── lambda_function/lambda_handler.py
├── glue_jobs/spotify_job.py
├── snowflake/spotify_etl_setup.sql
└── README.md



---

## 💡 Learnings

- PySpark transformations using AWS Glue
- Serverless automation with Lambda
- Real-time ingestion with Snowpipe
- Clean data lake design on S3

---

## 📬 Contact

Created by **Manu Singh**  
🔗 LinkedIn- https://www.linkedin.com/in/manu-singh-a68776ab/  
📧 your- sinhmanu0508@gmail.com










