<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f0c29,50:302b63,100:24243e&height=180&section=header&text=Vehicle%20Insurance%20MLOps&fontSize=46&fontColor=ffffff&fontAlignY=38&desc=End-to-End%20ML%20Pipeline%20%7C%20MongoDB%20%C2%B7%20AWS%20S3%20%C2%B7%20Docker&descAlignY=58&descSize=18&descColor=a78bfa" width="100%"/>

<br/>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white)
![AWS S3](https://img.shields.io/badge/AWS%20S3-232F3E?style=flat-square&logo=amazonaws&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)

**A production-grade, modular MLOps pipeline that predicts vehicle insurance cross-sell likelihood — from raw MongoDB data to a trained, artifact-tracked RandomForest classifier.**

</div>

---

## Overview

This project implements a full ML lifecycle pipeline for predicting whether a health insurance customer is likely to purchase vehicle insurance (cross-sell prediction). Every stage — ingestion, validation, transformation, training, evaluation, and deployment — is implemented as a discrete, independently testable component connected via typed artifact dataclasses.

The pipeline is driven by **YAML-based schema and model configs**, uses **MongoDB Atlas** as the data source, **AWS S3** for model artifact storage, and is fully containerized with **Docker**.

---

## Pipeline Architecture

```
MongoDB Atlas
     │
     ▼
┌─────────────────┐
│  Data Ingestion │  ── Exports collection → feature store CSV → train/test split
└────────┬────────┘
         │ DataIngestionArtifact
         ▼
┌──────────────────┐
│ Data Validation  │  ── Schema checks: column count, numerical & categorical presence
└────────┬─────────┘
         │ DataValidationArtifact
         ▼
┌────────────────────────┐
│  Data Transformation   │  ── Gender mapping, dummy encoding, StandardScaler,
│                        │     MinMaxScaler, SMOTEENN class balancing → .npy arrays
└────────┬───────────────┘
         │ DataTransformationArtifact
         ▼
┌──────────────────┐
│  Model Trainer   │  ── RandomForestClassifier (YAML-configured hyperparams)
│                  │     Accuracy · F1 · Precision · Recall → MetricArtifact
└────────┬─────────┘
         │ ModelTrainerArtifact
         ▼
┌──────────────────┐
│ Model Evaluation │  ── Compares trained model vs. production model on S3
└────────┬─────────┘
         │ ModelEvaluationArtifact
         ▼
┌──────────────────┐
│  Model Pusher    │  ── Uploads accepted model to AWS S3 bucket
└──────────────────┘
         │
         ▼
  FastAPI Prediction Service
```

---

## Project Structure

```text
Vehicle-Insurance-MLOps-project/
├── src/
│   ├── components/
│   │   ├── data_ingestion.py        # MongoDB export → feature store → train/test split
│   │   ├── data_validation.py       # Schema-driven column & type validation
│   │   ├── data_transformation.py   # Preprocessing pipeline + SMOTEENN balancing
│   │   ├── model_trainer.py         # RandomForest training + metric evaluation
│   │   ├── model_evaluation.py      # S3 model comparison + acceptance gate
│   │   └── model_pusher.py          # Push accepted model artifact to AWS S3
│   ├── configuration/
│   │   ├── mongo_db_connection.py   # MongoDB Atlas connection manager
│   │   └── aws_connection.py        # Boto3 AWS session management
│   ├── cloud_storage/
│   │   └── aws_storage.py           # S3 upload / download helpers
│   ├── data_access/
│   │   └── proj1_data.py            # MongoDB collection → DataFrame exporter
│   ├── constants/
│   │   └── __init__.py              # All pipeline constants (paths, ratios, hyperparams)
│   ├── entity/
│   │   ├── config_entity.py         # Dataclass configs for each pipeline stage
│   │   ├── artifact_entity.py       # Typed artifact dataclasses (stage outputs)
│   │   ├── estimator.py             # MyModel wrapper (preprocessor + classifier)
│   │   └── s3_estimator.py          # S3-backed model loader/saver
│   ├── exception/
│   │   └── __init__.py              # Custom MyException with traceback context
│   ├── logger/
│   │   └── __init__.py              # Structured file + console logger
│   ├── pipline/
│   │   ├── training_pipeline.py     # TrainPipeline — orchestrates all 6 stages
│   │   └── prediction_pipeline.py   # PredictionPipeline — loads model, runs inference
│   └── utils/
│       └── main_utils.py            # YAML read, numpy save/load, object pickle helpers
├── config/
│   ├── schema.yaml                  # Column schema, numerical/categorical splits, scaling config
│   └── model.yaml                   # RandomForest hyperparameter config
├── app.py                           # FastAPI app — /train and /predict endpoints
├── demo.py                          # Standalone pipeline trigger script
├── Dockerfile                       # Container definition
├── .dockerignore
├── setup.py                         # Package install config
├── pyproject.toml                   # Project metadata
└── requirements.txt
```

---

## Component Details

### Data Ingestion
Connects to **MongoDB Atlas**, exports the insurance collection as a DataFrame via `Proj1Data`, saves it to a local feature store CSV, then performs a stratified train/test split. All paths are resolved from `DataIngestionConfig` (timestamp-scoped artifact directories).

```
MongoDB Atlas collection
        ↓
  feature_store/vehicle_data.csv
        ↓
  ingested/train.csv + test.csv
```

### Data Validation
Validates the ingested data against `config/schema.yaml`:
- Column count matches schema definition
- All expected numerical columns present (`Age`, `Driving_License`, `Region_Code`, `Previously_Insured`, `Annual_Premium`, `Policy_Sales_Channel`, `Vintage`, `Response`)
- All expected categorical columns present (`Gender`, `Vehicle_Age`, `Vehicle_Damage`)

Writes a validation report JSON artifact. Pipeline halts downstream if validation fails.

### Data Transformation
Applies a `sklearn.pipeline.Pipeline` + `ColumnTransformer` built from `schema.yaml`:

| Step | Detail |
|------|--------|
| Gender encoding | `Female → 0`, `Male → 1` |
| Dummy variables | `Vehicle_Age`, `Vehicle_Damage` one-hot encoded |
| StandardScaler | Applied to `Age`, `Vintage` |
| MinMaxScaler | Applied to `Annual_Premium` |
| SMOTEENN | Combined over/under-sampling for class imbalance |

Outputs serialized `.npy` arrays for train/test sets and a pickled preprocessor object.

### Model Trainer
Trains a **RandomForestClassifier** with hyperparameters loaded from `config/model.yaml` via `ModelTrainerConfig`:

| Hyperparameter | Config key |
|---|---|
| `n_estimators` | `MODEL_TRAINER_N_ESTIMATORS` |
| `min_samples_split` | `MODEL_TRAINER_MIN_SAMPLES_SPLIT` |
| `min_samples_leaf` | `MODEL_TRAINER_MIN_SAMPLES_LEAF` |
| `max_depth` | `MIN_SAMPLES_SPLIT_MAX_DEPTH` |
| `criterion` | `MIN_SAMPLES_SPLIT_CRITERION` |
| `random_state` | `MIN_SAMPLES_SPLIT_RANDOM_STATE` |

Evaluates on the held-out test set and produces a `ClassificationMetricArtifact` (F1, Precision, Recall). Model is accepted only if accuracy meets `MODEL_TRAINER_EXPECTED_SCORE`.

### Model Evaluation
Loads the current production model from **AWS S3** and compares it against the newly trained model. If the new model's F1 exceeds the threshold, `is_model_accepted = True` and the artifact is passed to the pusher.

### Model Pusher
Uploads the accepted model to the configured **AWS S3 bucket** using `S3Estimator`, making it available for the prediction pipeline to load at inference time.

---

## Entity & Artifact Design

Each pipeline stage consumes a typed **Config dataclass** and produces a typed **Artifact dataclass** — making stage boundaries explicit and inter-stage contracts enforceable at runtime.

```python
# Config dataclasses (inputs)
DataIngestionConfig       → paths, split ratio, collection name
DataValidationConfig      → validation report path
DataTransformationConfig  → transformed array paths, preprocessor path
ModelTrainerConfig        → model path, hyperparams, expected accuracy

# Artifact dataclasses (outputs / stage contracts)
DataIngestionArtifact     → trained_file_path, test_file_path
DataValidationArtifact    → validation_status, message, report_path
DataTransformationArtifact→ object_path, train_path, test_path
ClassificationMetricArtifact → f1_score, precision_score, recall_score
ModelTrainerArtifact      → trained_model_file_path, metric_artifact
```

---

## Dataset Schema

Defined in `config/schema.yaml`:

| Column | Type | Role |
|--------|------|------|
| `Gender` | category | Categorical → binary encoded |
| `Age` | int | Numerical → StandardScaler |
| `Driving_License` | int | Numerical |
| `Region_Code` | float | Numerical |
| `Previously_Insured` | int | Numerical |
| `Vehicle_Age` | category | Categorical → one-hot |
| `Vehicle_Damage` | category | Categorical → one-hot |
| `Annual_Premium` | float | Numerical → MinMaxScaler |
| `Policy_Sales_Channel` | float | Numerical |
| `Vintage` | int | Numerical → StandardScaler |
| `Response` | int | **Target** (0 = not interested, 1 = interested) |

---

## Getting Started

### Prerequisites

- Python 3.10+
- MongoDB Atlas cluster with the insurance dataset loaded
- AWS account with an S3 bucket for model artifacts

### Installation

```bash
git clone https://github.com/Rhythm05Roy/Vehicle-Insurance-MLOps-project.git
cd Vehicle-Insurance-MLOps-project

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file or export these before running:

```bash
MONGODB_URL_KEY="mongodb+srv://<user>:<password>@cluster.mongodb.net"
AWS_ACCESS_KEY_ID="..."
AWS_SECRET_ACCESS_KEY="..."
AWS_REGION="ap-southeast-1"
MODEL_BUCKET_NAME="your-s3-bucket-name"
```

### Run the Training Pipeline

```bash
# Via demo script
python demo.py

# Or via FastAPI training endpoint
uvicorn app:app --host 0.0.0.0 --port 8080
# POST http://localhost:8080/train
```

### Run Prediction

```bash
# POST http://localhost:8080/predict
# Body: JSON with feature fields matching schema.yaml
```

---

## Docker

```bash
# Build
docker build -t vehicle-insurance-mlops .

# Run
docker run -p 8080:8080 \
  -e MONGODB_URL_KEY=<your_mongo_url> \
  -e AWS_ACCESS_KEY_ID=<key> \
  -e AWS_SECRET_ACCESS_KEY=<secret> \
  vehicle-insurance-mlops
```

---

## Configuration Files

**`config/schema.yaml`** — Single source of truth for:
- Column names and types (used in validation)
- Numerical / categorical column splits (used in transformation)
- Scaling targets (`num_features` → StandardScaler, `mm_columns` → MinMaxScaler)

**`config/model.yaml`** — RandomForest hyperparameters. Edit this to retrain with different params without touching source code.

---

## Key Design Patterns

- **Artifact-driven pipeline** — each stage's output is a typed dataclass, not raw paths or dicts, making inter-stage contracts explicit and debuggable
- **Config-entity separation** — all path construction and hyperparameter resolution happens in `config_entity.py`; components stay free of hardcoded values
- **YAML-driven schema** — `schema.yaml` controls validation rules and transformation column selection; changes propagate automatically through the pipeline
- **Timestamp-scoped artifacts** — every run writes to `artifacts/<timestamp>/`, making reruns non-destructive and enabling easy experiment comparison
- **Custom exception propagation** — `MyException` wraps all exceptions with full traceback context, making production debugging faster

---

## License

MIT — see `LICENSE`.

<div align="center">

**Built by [Ridam Roy](https://github.com/Rhythm05Roy)**

[![GitHub](https://img.shields.io/badge/GitHub-Rhythm05Roy-181717?style=flat-square&logo=github)](https://github.com/Rhythm05Roy)
[![Email](https://img.shields.io/badge/Email-ridam15--4260%40diu.edu.bd-D44638?style=flat-square&logo=gmail&logoColor=white)](mailto:ridam15-4260@diu.edu.bd)

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f0c29,50:302b63,100:24243e&height=80&section=footer" width="100%"/>

</div>
