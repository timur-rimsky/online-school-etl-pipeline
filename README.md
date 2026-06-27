# Online School ETL Pipeline

This project demonstrates a complete ETL pipeline for an online school using Python, pandas, SQLite and SQL.

The pipeline extracts raw CSV data, applies data cleaning and validation rules, loads the cleaned data into a SQLite database, and runs analytical SQL queries to calculate business metrics such as revenue, course demand, lead-to-payment conversion and attendance rate.

## Project Overview

The project simulates an online education platform with users, courses, leads, payments and lessons.

The main goal is to show how raw data can be transformed into a structured database and then used for analytical reporting.

## Tech Stack

* Python
* pandas
* NumPy
* SQLite
* SQL
* pathlib
* sqlite3

## Project Structure

```text
online-school-etl-pipeline/
│
├── data/
│   └── raw/
│       ├── users.csv
│       ├── courses.csv
│       ├── leads.csv
│       ├── payments.csv
│       └── lessons.csv
│
├── sql/
│   └── analytical_queries.sql
│
├── src/
│   ├── generate_users.py
│   ├── generate_courses.py
│   ├── generate_leads.py
│   ├── generate_payments.py
│   ├── generate_lessons.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── pipeline.py
│   └── run_sql_queries.py
│
├── notebooks/
├── README.md
├── requirements.txt
└── .gitignore
```

The `database/` folder is generated automatically when the ETL pipeline runs and is excluded from Git.

## Data Model

The project uses five main tables:

### users

Contains user registration and profile information.

Main columns:

* `user_id`
* `registration_date`
* `country`
* `city`
* `age`
* `traffic_source`
* `device`
* `is_active`

### courses

Contains course reference data.

Main columns:

* `course_id`
* `course_name`
* `category`
* `course_price`
* `duration_weeks`

### leads

Contains course applications submitted by users.

Main columns:

* `lead_id`
* `user_id`
* `course_id`
* `lead_date`
* `lead_status`

### payments

Contains payment information for converted leads.

Main columns:

* `payment_id`
* `user_id`
* `course_id`
* `payment_date`
* `amount`
* `payment_status`

### lessons

Contains lesson attendance events.

Main columns:

* `lesson_id`
* `user_id`
* `course_id`
* `lesson_date`
* `lesson_type`
* `attendance_status`

## ETL Pipeline

The ETL pipeline consists of three main stages.

### 1. Extract

The `extract.py` module reads raw CSV files from `data/raw/` and returns them as pandas DataFrames.

### 2. Transform

The `transform.py` module applies data cleaning and validation rules:

* removes duplicates by primary keys
* validates required columns
* converts ID columns to integers
* converts date columns to datetime
* converts numeric columns safely
* normalizes text status values
* filters invalid statuses
* filters invalid numeric values
* resets DataFrame indexes after cleaning

### 3. Load

The `load.py` module loads cleaned tables into a SQLite database:

```text
database/online_school.db
```

Tables are recreated on each pipeline run using `if_exists="replace"`.

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/timur-rimsky/online-school-etl-pipeline.git
cd online-school-etl-pipeline
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the full ETL pipeline

```bash
python src/pipeline.py
```

This command will:

* extract raw CSV data
* clean and transform the data
* create the SQLite database
* load all cleaned tables into the database

After successful execution, the database will be created here:

```text
database/online_school.db
```

### 4. Run analytical SQL queries from Python

```bash
python src/run_sql_queries.py
```

This script executes key analytical queries and prints the results to the console.

## SQL Analysis

The file `sql/analytical_queries.sql` contains SQL queries for business analysis.

Main query sections:

### Data Overview

* count rows by table
* leads by status
* payments by status
* lessons by attendance status
* lessons by lesson type

### Revenue Analysis

* total paid revenue
* revenue by course

### Course Demand Analysis

* leads by course
* leads by course and status

### Conversion Analysis

* lead-to-payment conversion by course

### Attendance Analysis

* attendance rate by course

## Key Metrics

The project calculates several important business metrics:

* total paid revenue
* revenue by course
* number of leads by course
* lead-to-payment conversion rate
* attendance rate by course
* payment status distribution
* lesson attendance distribution

## Example Workflow

```text
Raw CSV files
   ↓
extract.py
   ↓
transform.py
   ↓
load.py
   ↓
SQLite database
   ↓
analytical_queries.sql
   ↓
run_sql_queries.py
```

## Why This Project Is Useful

This project demonstrates practical skills required for junior Data Engineer, ETL Developer and SQL-focused data roles:

* building a modular ETL pipeline
* working with raw CSV data
* cleaning and validating data with pandas
* loading structured data into SQLite
* writing analytical SQL queries
* calculating business metrics
* organizing a data project for GitHub

## Project Status

Completed as a portfolio ETL project.

Possible future improvements:

* add PostgreSQL support
* add automated data quality checks
* add logging
* add unit tests
* add SQL views
* add a dashboard layer
* schedule the pipeline with Airflow or Prefect
