from flask import Flask, request, jsonify
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Float, inspect
import os
import logging

# initializing Flask app
app = Flask(__name__)

# setting up logging for troubleshooting
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# configuring the database
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@postgres:5433/postgres')
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# setting up the upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Check if file is part of the request
        if 'file' not in request.files:
            logger.error("No file  in the request")
            return jsonify({"error": "No file present"}), 400

        file = request.files['file']

        # Checking if file is selected
        if file.filename == '':
            logger.error("No selected file")
            return jsonify({"error": "No file selected"}), 400

        if file:
            # Read the csv into a dataframe
            df = pd.read_csv(file)
            logger.info(f"CSV file read successfully: {file.filename}")

            # Infer schema and create the table
            table = create_table_from_df(df)
            logger.info(f"Table schema inferred and table created: {table}")

            # Detect and handle outliers
            if detect_outliers(df):
                logger.warning("Outliers have been detected in data")
                return jsonify({"error": "Outliers detected"}), 400

            # Insert data into the table
            insert_data(df, table)
            logger.info("Data inserted into the table successfully")

            return jsonify({"message": "File processing successfully"}), 200

    except Exception as e:
        logger.error(f"Error processing file: {e}")
        return jsonify({"error": "Internal server error"}), 500

def create_table_from_df(df):
    try:
        # Infer schema from DataFrame
        columns = []
        for column in df.columns:
            if pd.api.types.is_integer_dtype(df[column]):
                columns.append(Column(column, Integer))
            elif pd.api.types.is_float_dtype(df[column]):
                columns.append(Column(column, Float))
            else:
                columns.append(Column(column, String))

        # Define a new table or get the existing table
        table = Table('data', metadata, *columns, extend_existing=True)

        # Use inspect module to check if the table exists
        inspector = inspect(engine)
        if not inspector.has_table('data'):
            metadata.create_all(engine, tables=[table])

        return table

    except Exception as e:
        logger.error(f"Error when creating table from DataFrame: {e}")
        raise

def detect_outliers(df):
    try:
        # Simple outlier detection using interquatile range
        Q1 = df['value'].quantile(0.25)
        Q3 = df['value'].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df['value'] < (Q1 - 1.5 * IQR)) | (df['value'] > (Q3 + 1.5 * IQR))]

        return not outliers.empty

    except Exception as e:
        logger.error(f"Error detecting outliers: {e}")
        raise

def insert_data(df, table):
    try:
        # Insert DataFrame into the SQL table
        with engine.connect() as conn:
            df.to_sql(table.name, conn, if_exists='append', index=False)

    except Exception as e:
        logger.error(f"Error inserting data into table: {e}")
        raise

# Running the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
