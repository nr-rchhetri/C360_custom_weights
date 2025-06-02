from dataclasses import dataclass

@dataclass
class SnowflakeConfig:
    # user = 'rchhetri'
    # password = 'VAMOS_nadal10*'
    # account = 'PDA47359.us-east-1'
    # warehouse = 'TEAM_ENTERPRISE_ANALYTICS'
    # role = 'FR_ENTERPRISE_ANALYTICS_DEVOPS'
    # database = 'REPORTING'
    # schema = 'CONSUMPTION_METRICS'

    username: str = "rchhetri"
    account: str = "PDA47359.us-east-1"
    password: str = "VAMOS_nadal10*"
    warehouse: str = "TEAM_ENTERPRISE_ANALYTICS"
    database: str = "REPORTING"
    schema: str = "CONSUMPTION_METRICS"
    role: str = "FR_ENTERPRISE_ANALYTICS_DEVOPS"
    authenticator: str ="externalbrowser"
    # region_name: str = "us-east-1"
    # secret_name: str = "sagemaker_prod/snowflake/key"



    # username: str = "SVC_SAGEMAKER_PROD_RO"
    # account: str = "PDA47359.us-east-1"
    # warehouse: str = "SAGEMAKER_PROD"
    # database: str = "DEV"
    # schema: str = "EA_PRODUCT_ANALYTICS"
    # role: str = "APP_SAGEMAKER_PROD"
    # region_name: str = "us-east-1"
    # secret_name: str = "sagemaker_prod/snowflake/key"

    