# CSV_TO_SQL



## Setup

### Need to have the following
- Docker
- Docker Compose
- Python 3

This project is a pipeline that consumes data from a CSV file through a web API, infers the schema and data types, performs basic outlier detection, and inserts  data into an SQL database if no outliers are detected. The application is containerized using Docker.

Features

Accepts CSV file uploads via a RESTful web API.

Infers the schema of the CSV and maps to SQL table.

Performs basic outlier detection.

Inserts data into an SQL database if no outliers are detected.

Application is then containerized for quick setup.

Tools Required

Python, Flask

PostgreSQL: SQL database for storing processed data.

Docker: Containerization for the application and database.

Docker Compose



Build and run Docker containers:
docker-compose up --build

Use Postman to upload a CSV file to the API endpoint

Access the database using a PostgreSQL client to query the data.

Host: localhost

Port: 5432

Username: postgres

Password: postgres

Database: postgres
