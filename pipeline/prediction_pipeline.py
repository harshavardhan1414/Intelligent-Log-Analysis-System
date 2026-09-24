import os
import sys
import joblib
import pandas as pd

from src.utils.logger import logger
from src.utils.exception import CustomException

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.data_preprocessing import DataPreprocessing


class PredictionPipeline:

    def __init__(
        self,
        input_file,
        model_path="artifacts/model/model.pkl",
        vectorizer_path="artifacts/features/vectorizer.pkl"
    ):

        self.input_file = input_file
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path

    def predict(self):

        try:

            logger.info(
                "Prediction Pipeline Started"
            )

          
            logger.info(
                "Starting data ingestion for new log file"
            )

            ingestion_config = type(
                "PredictionIngestionConfig",
                (),
                {
                    "dataset_path": self.input_file,
                    "artifact_dir": "artifacts",
                    "raw_data_dir": "artifacts/raw_data",
                    "processed_data_dir": "artifacts/processed_data"
                }
            )()

            ingestion = DataIngestion(
                ingestion_config
            )

            ingestion_artifact = (
                ingestion.initiate_data_ingestion()
            )

            logger.info(
                "New log file ingested successfully"
            )

           
            logger.info(
                "Starting data validation"
            )

            validator = DataValidation(
                ingestion_artifact
            )

            validation_status = (
                validator.initiate_data_validation()
            )

            if not validation_status:

                raise ValueError(
                    "Data validation failed"
                )

            logger.info(
                "Data validation completed successfully"
            )

          
            logger.info(
                "Starting data transformation"
            )

            transformation = DataTransformation(
                ingestion_artifact
            )

            transformed_file = (
                transformation.initiate_data_transformation()
            )

            logger.info(
                f"Transformed file: {transformed_file}"
            )

           
            logger.info(
                "Starting data preprocessing"
            )

            preprocessing = DataPreprocessing(
                transformed_file
            )

            preprocessed_file = (
                preprocessing.initiate_data_preprocessing()
            )

            logger.info(
                f"Preprocessed file: {preprocessed_file}"
            )

           
            df = pd.read_csv(
                preprocessed_file
            )

            logger.info(
                f"New logs loaded: {len(df)}"
            )

            if df.empty:

                raise ValueError(
                    "No log records found after preprocessing."
                )

            if "cleaned_message" not in df.columns:

                raise ValueError(
                    "cleaned_message column is missing "
                    "from preprocessed data."
                )

            
            if not os.path.exists(
                self.vectorizer_path
            ):

                raise FileNotFoundError(
                    "Saved TF-IDF vectorizer not found at: "
                    f"{self.vectorizer_path}"
                )

            vectorizer = joblib.load(
                self.vectorizer_path
            )

            logger.info(
                "Saved TF-IDF vectorizer loaded successfully"
            )

           
            features = vectorizer.transform(
                df["cleaned_message"]
            )

            logger.info(
                f"New feature matrix shape: "
                f"{features.shape}"
            )

           
            if not os.path.exists(
                self.model_path
            ):

                raise FileNotFoundError(
                    "Saved trained model not found at: "
                    f"{self.model_path}"
                )

            model = joblib.load(
                self.model_path
            )

            logger.info(
                "Saved Isolation Forest model loaded successfully"
            )

           
            predictions = model.predict(
                features
            )

            anomaly_scores = (
                model.decision_function(
                    features
                )
            )

            logger.info(
                "All new logs classified successfully"
            )

            
            if len(df) != len(predictions):

                raise ValueError(
                    "Number of logs and predictions "
                    "do not match."
                )

            
            df["prediction"] = predictions

            df["anomaly_score"] = (
                anomaly_scores
            )

            df["prediction_label"] = (
                df["prediction"]
                .map(
                    {
                        1: "Normal",
                        -1: "Anomaly"
                    }
                )
            )

           
            prediction_dir = (
                "artifacts/predictions"
            )

            os.makedirs(
                prediction_dir,
                exist_ok=True
            )

            prediction_file = os.path.join(
                prediction_dir,
                "predictions.csv"
            )

            df.to_csv(
                prediction_file,
                index=False
            )

           
            total_logs = len(df)

            normal_logs = (
                df["prediction"] == 1
            ).sum()

            anomaly_logs = (
                df["prediction"] == -1
            ).sum()

           
            info_logs = (
                df["level"] == "INFO"
            ).sum()

            warning_logs = (
                df["level"] == "WARNING"
            ).sum()

            error_logs = (
                df["level"] == "ERROR"
            ).sum()

            critical_logs = (
                df["level"] == "CRITICAL"
            ).sum()

            
            anomaly_df = df[
                df["prediction"] == -1
            ]

            anomaly_info = (
                anomaly_df["level"] == "INFO"
            ).sum()

            anomaly_warning = (
                anomaly_df["level"] == "WARNING"
            ).sum()

            anomaly_error = (
                anomaly_df["level"] == "ERROR"
            ).sum()

            anomaly_critical = (
                anomaly_df["level"] == "CRITICAL"
            ).sum()

            
            logger.info(
                f"Total Logs: {total_logs}"
            )

            logger.info(
                f"Normal Logs: {normal_logs}"
            )

            logger.info(
                f"Anomaly Logs: {anomaly_logs}"
            )

            logger.info(
                f"INFO Logs: {info_logs}"
            )

            logger.info(
                f"WARNING Logs: {warning_logs}"
            )

            logger.info(
                f"ERROR Logs: {error_logs}"
            )

            logger.info(
                f"CRITICAL Logs: {critical_logs}"
            )

            logger.info(
                f"INFO Anomalies: {anomaly_info}"
            )

            logger.info(
                f"WARNING Anomalies: {anomaly_warning}"
            )

            logger.info(
                f"ERROR Anomalies: {anomaly_error}"
            )

            logger.info(
                f"CRITICAL Anomalies: {anomaly_critical}"
            )

            logger.info(
                f"Prediction file saved at: "
                f"{prediction_file}"
            )

            logger.info(
                "Prediction Pipeline Completed"
            )

           
            return {
                "total_logs": total_logs,
                "normal_logs": normal_logs,
                "anomaly_logs": anomaly_logs,

                "info_logs": info_logs,
                "warning_logs": warning_logs,
                "error_logs": error_logs,
                "critical_logs": critical_logs,

                "anomaly_info": anomaly_info,
                "anomaly_warning": anomaly_warning,
                "anomaly_error": anomaly_error,
                "anomaly_critical": anomaly_critical,

                "prediction_file": prediction_file
            }

        except Exception as e:

            raise CustomException(
                e,
                sys
            )