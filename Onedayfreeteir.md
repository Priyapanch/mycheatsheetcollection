Great! Here's a **1-Day Free Tier Hands-on Lab Plan** for both **Data Engineer** and **ML Engineer** roles using AWS Free Tier:

---

## 🟦 **1-Day Data Engineer Hands-on Lab (AWS Free Tier)**

### ✅ Objective:

Ingest, transform, and query data using AWS Glue, S3, and Athena.

### 🕘 3-Hour Plan:

| Time                | Task                                                                                                                                          | Services Used           |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| 9:00 AM - 10:00 AM  | **Data Ingestion**: Upload CSV file to S3 (use AWS Open Data Registry sample dataset).                                                        | S3                      |
| 10:00 AM - 11:00 AM | **Data Cataloging & ETL**: Create Glue Crawler to catalog S3 data. Run a Glue Job (Python shell job or Spark script) to clean/transform data. | Glue, Glue Data Catalog |
| 11:00 AM - 12:00 PM | **Query & Validation**: Use Athena to query the transformed data from S3. Validate schema & data quality.                                     | Athena, S3              |

### ✅ Deliverables:

* Transformed dataset in S3 (Parquet format)
* Athena table for ad-hoc queries

---

## 🟩 **1-Day ML Engineer Hands-on Lab (AWS Free Tier)**

### ✅ Objective:

Train, deploy, and monitor a simple ML model using Amazon SageMaker.

### 🕘 3-Hour Plan:

| Time              | Task                                                                                                                         | Services Used                       |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| 2:00 PM - 3:00 PM | **Model Development**: Launch SageMaker Notebook (t2.micro). Load Titanic or Iris dataset. Train a basic XGBoost classifier. | SageMaker Notebook                  |
| 3:00 PM - 4:00 PM | **Model Deployment**: Deploy the trained model to a SageMaker endpoint (m4.xlarge free tier). Perform real-time inference.   | SageMaker Endpoint                  |
| 4:00 PM - 5:00 PM | **Monitoring & Optimization**: Enable Model Monitor to detect data drift. View metrics in CloudWatch.                        | SageMaker Model Monitor, CloudWatch |

### ✅ Deliverables:

* Deployed SageMaker endpoint
* Inference results & monitoring metrics

---

## 🟢 Estimated Total Free Tier Usage:

| Service    | Estimated Free Usage                  |
| ---------- | ------------------------------------- |
| S3         | <1 GB storage                         |
| Glue       | <5 DPU hours                          |
| Athena     | <1 GB data scanned                    |
| SageMaker  | <10 notebook hours, <5 endpoint hours |
| CloudWatch | Minimal custom metrics                |

---

### ✅ Bonus:

* Use AWS Skill Builder free labs for extra practice: [https://skillbuilder.aws](https://skillbuilder.aws)

---

### Would you like me to give you a **20-Day Free Tier Machine Learning Specialty Hands-on Challenge Plan** (progressive difficulty, real exam scenarios)?

Reply **"Yes - 20-Day Challenge Plan"** if interested.
