import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

# ---------------- LOGGING SETUP ----------------
# Create logs directory if not exists
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

# ---------------- DATABASE CONNECTION ----------------
# SQLite database will be created in project directory
engine = create_engine('sqlite:///inventory.db')


# ---------------- DATA INGESTION FUNCTION ----------------
def ingest_db(df, table_name, engine):
    """
    Inserts a pandas DataFrame into a SQLite database table.

    Parameters:
    df (DataFrame): Input data
    table_name (str): Name of the table in DB
    engine: SQLAlchemy engine
    """
    df.to_sql(
        table_name,
        con=engine,
        if_exists='replace',
        index=False,
        chunksize=50000,   # Improves performance for large datasets
        method='multi'
    )


# ---------------- LOAD & PROCESS DATA ----------------
def load_raw_data():
    """
    Reads all CSV files from the data folder and loads them into SQLite database.
    """

    start = time.time()

    # Absolute path to data folder (update if needed)
    data_path = r"C:\Users\farru\OneDrive\Desktop\sales inventory\data"

    loaded_files = []

    for file in os.listdir(data_path):
        if file.endswith('.csv'):

            file_path = os.path.join(data_path, file)

            try:
                # Read CSV file
                df = pd.read_csv(file_path)

                logging.info(f"Loaded {file} with shape {df.shape}")

                # Ingest into database
                ingest_db(df, file[:-4], engine)

                logging.info(f"Ingested {file} into database")

                loaded_files.append(file)

            except Exception as e:
                logging.error(f"Error processing {file}: {e}")

    end = time.time()
    total_time = (end - start) / 60

    # Log summary
    logging.info("----------- Ingestion Complete -----------")
    logging.info(f"Total files loaded: {len(loaded_files)}")
    logging.info(f"Files: {loaded_files}")
    logging.info(f"Total Time Taken: {total_time:.2f} minutes")


# ---------------- ENTRY POINT ----------------
if __name__ == "__main__":
    load_raw_data()