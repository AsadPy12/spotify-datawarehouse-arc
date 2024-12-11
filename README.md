# Spotify Data ETL Pipeline using AWS

This project implements an ETL pipeline for Spotify data using AWS services.

# Data Flow:

### 1. Extract:

* <b>Spotify API:</b> Retrieves data from the Spotify API through a Python script.
* <b>Amazon CloudWatch:</b> Triggers the data extraction process daily.
* <b>AWS Lambda:</b> Extracts data from the Spotify API and stores it in Amazon S3.

### 2. Transform:

* <b>AWS Lambda:</b> Transforms the data extracted from S3, performing operations like cleaning, enriching, and formatting.
* <b>Amazon S3:</b> Stores the transformed data.

### 3. Load:

* <b>Crawler:</b> Infers the schema of the transformed data in S3.
* <b>AWS Glue Data Catalog:</b> Stores the inferred schema.
* <b>Amazon Athena:</b> Analyzes the data stored in S3 using SQL queries.

### 4. Architecture Diagram:
![arc](./spotify-data-architecture.png)

#  Technologies Used:

1. AWS Services: Amazon S3, AWS Lambda, Amazon CloudWatch, AWS Glue Data Catalog, Amazon Athena
2. Python: Scripting language for data extraction and transformation.

# Usage:

* Configure the AWS services and credentials.
* Run the Python scripts in the extract and transform folders.
* Use Amazon Athena to query and analyze the data in S3

# Benefits:

* <b>Scalability:</b>> The use of serverless AWS services allows for easy scaling of the pipeline.
* <b>Cost-Effectiveness:</b> Serverless architecture eliminates the need for dedicated servers.
* <b>Flexibility:</b> The pipeline can be easily modified to adapt to changing data requirements.

# Future Improvements:

* Implement data validation and quality checks.
* Integrate with other AWS services for data visualization and reporting.
* Optimize the data extraction and transformation processes.

