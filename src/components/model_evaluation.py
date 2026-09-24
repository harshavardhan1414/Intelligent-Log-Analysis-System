import os
import sys
import joblib
import pandas as pd

from src.utils.logger import logger
from src.utils.exception import CustomException


class ModelEvaluation:

    def __init__(
        self,
        model_path,
        feature_path,
        preprocessed_file
    ):

        self.model_path = model_path
        self.feature_path = feature_path
        self.preprocessed_file = preprocessed_file

    def initiate_model_evaluation(self):

        try:

            logger.info(
                "Model Evaluation Started"
            )


            model = joblib.load(
                self.model_path
            )

            logger.info(
                "Trained model loaded successfully"
            )


            features = joblib.load(
                self.feature_path
            )

            logger.info(
                f"Feature matrix shape: {features.shape}"
            )

           
            df = pd.read_csv(
                self.preprocessed_file
            )

            logger.info(
                f"Preprocessed data shape: {df.shape}"
            )

            predictions = model.predict(
                features
            )

           
            anomaly_scores = model.decision_function(
                features
            )

         
            if len(df) != len(predictions):

                raise ValueError(
                    "Number of log records and "
                    "predictions do not match."
                )


            df["prediction"] = predictions

            df["anomaly_score"] = anomaly_scores

          
            df["prediction_label"] = (
                df["prediction"]
                .map(
                    {
                        1: "Normal",
                        -1: "Anomaly"
                    }
                )
            )


            evaluation_dir = (
                "artifacts/evaluation"
            )

            os.makedirs(
                evaluation_dir,
                exist_ok=True
            )

            prediction_file = os.path.join(
                evaluation_dir,
                "predictions.csv"
            )

            df.to_csv(
                prediction_file,
                index=False
            )

            
            total_logs = len(
                predictions
            )

            anomaly_count = (
                predictions == -1
            ).sum()

            normal_count = (
                predictions == 1
            ).sum()

            anomaly_percentage = (
                anomaly_count / total_logs
            ) * 100

            normal_percentage = (
                normal_count / total_logs
            ) * 100

           
            logger.info(
                f"Total Logs: {total_logs}"
            )

            logger.info(
                f"Normal Logs: {normal_count}"
            )

            logger.info(
                f"Anomaly Logs: {anomaly_count}"
            )

            logger.info(
                f"Normal Percentage: "
                f"{normal_percentage:.2f}%"
            )

            logger.info(
                f"Anomaly Percentage: "
                f"{anomaly_percentage:.2f}%"
            )

            logger.info(
                f"Prediction file saved at: "
                f"{prediction_file}"
            )

            logger.info(
                "Model Evaluation Completed"
            )

            return prediction_file

        except Exception as e:

            raise CustomException(e, sys)