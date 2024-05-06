from sqlalchemy import create_engine, text
import pandas as pd
import psycopg2

from config.settings import BaseConfig

#---------------------------------------------------------------------------------------

def create_database_if_not_exist():
    # get base config instance
    baseconfig_instance = BaseConfig()

    # Connect to PostGreSQL
    conn = psycopg2.connect(
        host=baseconfig_instance.db_host,
        port=baseconfig_instance.db_port,
        user=baseconfig_instance.db_user,
        password=baseconfig_instance.db_password
    )

    # Objet cursor object to execute SQL queries
    cursor = conn.cursor()

    # Verifying if DB exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname=%s;", (baseconfig_instance.db_name,))
    database_exists = cursor.fetchone()

    # Create DB if it doesn't exist
    if not database_exists:
        cursor.execute(f"CREATE DATABASE {baseconfig_instance.db_name};")
        print(f"Database '{baseconfig_instance.db_name}' created successfully.")
    else:
        print(f"Database '{baseconfig_instance.db_name}' already exists.")

    #Close cursor+connection
    cursor.close()
    conn.close()




#---------------------------------------------------------------------------------------
# Function to create tables if they do not exist
def create_tables():
    # get base config instance
    baseconfig_instance = BaseConfig()

    # connect to the database
    engine = create_engine(baseconfig_instance.sqlalchemy_connection)

    # SQL query to create table bixi_stations_status
    create_table_query_1 = """
    CREATE TABLE IF NOT EXISTS bixi_stations_status (
                station_id VARCHAR(20) PRIMARY KEY,
                num_bikes_available SMALLINT,
                num_ebikes_available SMALLINT,
                num_docks_available SMALLINT,
                is_installed BOOLEAN,
                is_renting BOOLEAN,
                is_returning BOOLEAN,
                last_reported INT
    );
    """

    create_table_query_2 = """
    CREATE TABLE IF NOT EXISTS bixi_stations_info (
        station_id VARCHAR(20) PRIMARY KEY,
        name VARCHAR(255),
        lat FLOAT(10),
        lon FLOAT(10),
        capacity SMALLINT
    );
    """

    # defining log messages
    def log_message(message, error=None):
        print(message)
        if error:
            print(error)

    # Begin a transaction
    with engine.begin() as connection:
        try:
            # Creation of the first table
            log_message("Creating table 'bixi_stations_status'...")
            connection.execute(text(create_table_query_1))
            log_message("Table 'bixi_stations_status' created successfully.")
            
            # Creation of the second table
            log_message("Creating table 'bixi_stations_info'...")
            connection.execute(text(create_table_query_2))
            log_message("Table 'bixi_stations_info' created successfully.")
            
            # Commit the transaction
            connection.commit()
        except Exception as e:
            connection.rollback()
            log_message("An error occurred during transaction:", e)
#---------------------------------------------------------------------------------------

# fetch all data from the tables and put them in a merged dataframe (info+status)
def fetch_data():
    # get base config instance
    baseconfig_instance = BaseConfig()

    # create the database engine
    engine = create_engine(baseconfig_instance.sqlalchemy_connection)

    # fetch data from the tables
    with engine.connect() as connection:
        # Fetch data from bixi_stations_status table
        query_status = "SELECT * FROM bixi_stations_status;"
        df_status = pd.read_sql(query_status, connection)

        # fetch data from bixi_stations_info table
        query_info = "SELECT * FROM bixi_stations_info;"
        df_info = pd.read_sql(query_info, connection)

    # Merge the dataframes on the column 'station_id'
    df = pd.merge(df_info, df_status, on="station_id")

    return df
#--------------------------------------------------------------------------------------


# Usage
# create_database_if_not_exist()
# create_tables()
# df = fetch_data()
# print(df.head(5))
