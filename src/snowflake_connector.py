# src/snowflake_connector.py
import sys
import os

# # Add the parent directory to the system path
sys.path.append('/Users/rchhetri/Downloads/CSAT_NPS/config')



from config import SnowflakeConfig


import snowflake.connector
import pandas as pd


class SnowflakeConnector:
    def __init__(self, config: SnowflakeConfig):
        self.config = config
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = snowflake.connector.connect(
            user=self.config.username,
            account=self.config.account,
            role=self.config.role,
            warehouse=self.config.warehouse,
            database=self.config.database,
            schema=self.config.schema,
            authenticator = self.config.authenticator
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query: str):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        column_names = [col[0] for col in self.cursor.description]
        return pd.DataFrame(result, columns=column_names)

        
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()