# Vehicle Insurance MLOps Project

This repository contains a comprehensive template for a Machine Learning Operations (MLOps) pipeline for vehicle insurance applications. The template organizes the code into modular components to ensure scalability, maintainability, and ease of deployment.

## Project Structure

The project is structured as follows:

```
.
├── src
│   ├── components
│   │   ├── __init__.py
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │   ├── model_evaluation.py
│   │   └── model_pusher.py
│   ├── configuration
│   │   ├── __init__.py
│   │   ├── mongo_db_connection.py
│   │   └── aws_connection.py
│   ├── cloud_storage
│   │   ├── __init__.py
│   │   └── aws_storage.py
│   ├── data_access
│   │   ├── __init__.py
│   │   └── proj1_data.py
│   ├── constants
│   │   └── __init__.py
│   ├── entity
│   │   ├── __init__.py
│   │   ├── config_entity.py
│   │   ├── artifact_entity.py
│   │   ├── estimator.py
│   │   └── s3_estimator.py
│   ├── exception
│   │   └── __init__.py
│   ├── logger
│   │   └── __init__.py
│   ├── pipline
│   │   ├── __init__.py
│   │   ├── training_pipeline.py
│   │   └── prediction_pipeline.py
│   ├── utils
│   │   ├── __init__.py
│   │   └── main_utils.py
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── demo.py
├── setup.py
├── pyproject.toml
├── config
│   ├── model.yaml
│   └── schema.yaml
```

## Key Features

### Components
- **Data Ingestion:** Handles data collection from various sources.
- **Data Validation:** Ensures the integrity and quality of the input data.
- **Data Transformation:** Prepares the data for model training by applying transformations.
- **Model Trainer:** Trains machine learning models.
- **Model Evaluation:** Evaluates the performance of trained models.
- **Model Pusher:** Deploys the trained model to the appropriate environment.

### Configuration
- **MongoDB Connection:** Establishes a connection to the MongoDB database.
- **AWS Connection:** Provides connectivity to AWS services such as S3.

### Cloud Storage
- **AWS Storage:** Handles storage and retrieval of artifacts from AWS S3.

### Pipelines
- **Training Pipeline:** Orchestrates the end-to-end model training process.
- **Prediction Pipeline:** Handles the deployment and inference tasks.

### Utilities
- Common utility functions for tasks like logging, exception handling, and artifact management.

## Setup and Installation

1. Clone the repository:
   ```bash
   https://github.com/Rhythm05Roy/Vehicle-Insurance-MLOps-project.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Vehicle-Insurance-MLOps-project
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## Configuration Files

- `model.yaml`: Contains model-specific configurations.
- `schema.yaml`: Defines the schema for input data validation.

## Docker Support

Build and run the application using Docker:

1. Build the Docker image:
   ```bash
   docker build -t vehicle-insurance-mlops .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 8501:8501 vehicle-insurance-mlops
   ```

## Future Enhancements

- Add CI/CD pipelines for automated deployments.
- Integrate advanced monitoring and logging solutions.
- Extend support for additional cloud platforms.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

