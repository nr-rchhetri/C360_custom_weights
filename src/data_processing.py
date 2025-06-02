# src/data_processing.py
import sys
import os

# # Add the parent directory to the system path
sys.path.append('/Users/rchhetri/Downloads/CSAT_NPS/src')
sys.path.append('/Users/rchhetri/Downloads/CSAT_NPS/config')



from config import SnowflakeConfig
from snowflake_connector import SnowflakeConnector

def establish_connection():
    config = SnowflakeConfig()
    connector = SnowflakeConnector(config)
    connector.connect()
    return connector
   

def fetch_data(query, connector):
    data = connector.execute_query(query)
    # connector.close()
    return data




