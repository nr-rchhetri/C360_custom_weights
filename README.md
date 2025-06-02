
# CSAT_Scores EDA

EDA on the data tables with CSAT scores.

## Project Structure
```
├── config/                    # Configuration management
│   ├── __init__.py           # Exports config classes
│   └── config.py             # Model, data, alerts configurations
├── pipeline/                  # SageMaker pipeline definition
│   ├── __init__.py           # Pipeline package initialization
│   └── definition.py         # Pipeline structure and configuration
├── processing_scripts/        # SageMaker processing scripts
│   ├── __init__.py
│   ├── process_data.py       # Data processing step
│   ├── predict.py            # Model prediction step
│   └── generate_alerts.py    # Alert generation step
├── src/                      # Core pipeline modules
│   ├── __init__.py          # Exports processor classes
│   ├── data.py              # Data processing and transformations
│   ├── model.py             # Model loading and predictions
│   ├── alerts.py            # Alert generation and storage
│   └── summarizer.py        # Summary generation
├── utils/                    # Utility modules
│   ├── __init__.py          # Exports utility classes
│   ├── snowflake_connection.py  # Snowflake client operations
│   └── s3_model_manager.py  # S3 model management
├── Dockerfile                # Container definition for SageMaker
└── requirements.txt          # Project dependencies
```

## Features
- Automated SageMaker pipeline with scheduled execution via EventBridge
- Data processing and feature engineering using SageMaker Processing jobs
- XGBoost model predictions with SHAP-based explainability
- Alert generation and storage in Snowflake
- S3-based model management with versioning
- Date-based organization of pipeline outputs

## Prerequisites
- AWS account with SageMaker access
- IAM roles for SageMaker execution
- Snowflake credentials and access
- Docker for local development and testing

## Container Setup
```bash
# Build Docker image
docker build --platform linux/amd64 -t ea-product-analytics .

# Tag for ECR
docker tag ea-product-analytics:ptc-churn-predictions-pipeline \
    702568842258.dkr.ecr.us-east-1.amazonaws.com/ea-product-analytics:ptc-churn-predictions-pipeline

# Push to ECR
docker push 702568842258.dkr.ecr.us-east-1.amazonaws.com/ea-product-analytics:ptc-churn-predictions-pipeline
```

## Pipeline Configuration
The pipeline uses several configuration classes:
- `DataConfig`: Data processing parameters and Snowflake settings
- `ModelConfig`: Model paths and S3 configurations
- `AlertConfig`: Alert generation settings

## Pipeline Steps
1. **Data Processing**
   - Fetches and processes data from Snowflake
   - Outputs processed data to S3

2. **Model Predictions**
   - Loads models from S3
   - Generates predictions and SHAP values
   - Saves results to S3

3. **Alert Generation**
   - Processes predictions and SHAP values
   - Generates alerts
   - Stores results in Snowflake

## S3 Organization
```
s3://ea-product-analytics/ptc-churn/
├── models/                    # Model storage
│   └── YYYY-MM-DD/           # Model version
│       ├── horizon_model_h=0_xgb.sav
│       ├── horizon_model_h=90_xgb.sav
│       └── horizon_model_h=180_xgb.sav
└── pipeline_runs/            # Pipeline outputs
    └── YYYY-MM-DD/          # Execution date
        ├── processed_data/
        └── predictions/
```

## Pipeline Deployment
```python
from pipeline import create_pipeline

# Create/update pipeline
pipeline = create_pipeline(
    role="your-sagemaker-role",
    image_uri="your-ecr-image-uri",
    bucket="your-bucket"
)
pipeline.upsert(role_arn="your-sagemaker-role")
```

## Automation
- Weekly execution via EventBridge schedule
- Automatic organization of outputs by date
- Logging and monitoring through CloudWatch

## Development
### Making Changes
1. Modify code (processing scripts, configs, etc.)
2. Build and push new Docker image with new tag
3. Update pipeline with new image URI
4. Test execution

### Monitoring
- CloudWatch logs for each processing step
- SageMaker Pipeline execution history
- Snowflake query monitoring

## Support
Contact the EA Product Analytics team for support and questions.

