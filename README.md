# 🎧 Spotify Data Pipeline using AWS & Snowflake

## 📌 Project Overview
This project demonstrates an end-to-end cloud-based data pipeline to extract, transform, and load Spotify data using AWS services and Snowflake.  
It automates data flow from Spotify API to Snowflake via S3, AWS Glue, and Snowpipe.

---

## 🧰 Tools & Technologies Used

- **AWS S3** – Raw and transformed data storage  
- **AWS Lambda** – Data extraction using Spotify API  
- **AWS Glue** – Data transformation with PySpark  
- **Amazon CloudWatch** – Scheduled triggers for Lambda  
- **Snowflake** – Cloud data warehouse  
- **Snowpipe** – Real-time ingestion from S3 to Snowflake  
- 

---## 📂 S3 Folder Structure
s3://spotify-etl-glue-project/
├── raw_data/
│ ├── to_processed/ ← Raw JSON files from Lambda (initial)
│ └── processed/ ← Moved after transformation (archived)
│
├── transformed/
│ ├── songs_data/ ← Cleaned song data
│ ├── artist_data/ ← Cleaned artist data
│ └── album_data/ ← Cleaned album data

### 📋 Folder Descriptions

| S3 Folder Path                          | Description                                      |
|----------------------------------------|--------------------------------------------------|
| `raw_data/to_processed/`               | Raw JSON from Lambda (before Glue processes it)  |
| `raw_data/processed/`                  | Archived after Glue processing (safe backup)     |
| `transformed/songs_data/`              | Transformed songs data (ready for Snowpipe)      |
| `transformed/artist_data/`             | Transformed artist metadata                      |
| `transformed/album_data/`              | Transformed album metadata                       |




📝 After Glue processing, raw files are archived from `to_processed/` to `processed/` for future reference and debugging.

---

## 📈 Architecture Diagram

Architecture---(architecture.png)

---

## 🧠 Workflow

1. **CloudWatch** triggers Lambda daily  
2. **Lambda** extracts raw Spotify data → saves in `s3://spotify-etl-glue-project/raw_data/processed/`
3. **AWS Glue** transforms raw data → writes cleaned data to:
 s3://spotify-etl-glue-project/transformed/
├── songs_data/
├── artist_data/
└── album_data/

4. **Snowpipe** automatically ingests data from `transformed/` into Snowflake staging tables
5. Final tables are updated via SQL in Snowflake


---

## 📂 Folder Structure in GitHub Repo

spotify-etl-aws-snowflake/
│
├── lambda_function/
│ └── lambda_handler.py
│
├── glue_jobs/
│ └── spotify_etl_glue_job.py
│
├── snowflake/
│ ├── create_tables.sql
│ ├── create_pipes.sql
│ └── stage_and_integration.sql
│
├── architecture.png
└── README.md


---

## 🙋‍♀️ Role & Contribution

I independently built this entire pipeline:
- Developed Lambda function to call Spotify API
- Designed S3 folder structure and raw-to-clean data flow
- Created PySpark Glue jobs for transformation
- Configured Snowpipe for real-time loading into Snowflake
- Managed full AWS → Snowflake 

---

## 📬 Contact

Created by **Manu Singh**  
🔗 LinkedIn- https://www.linkedin.com/in/manu-singh-a68776ab/  
📧 your- sinhmanu0508@gmail.com










