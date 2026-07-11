import os
import sys
import joblib
import pandas as pd

from src.utils.logger import logger
from src.utils.exception import CustomException


class ModelEvaluation:

    def __init__(self,
                 model_path,
                 feature_path):

        self.model_path = model_path
        self.feature_path = feature_path

    def initiate_model_evaluation(self):

        try:

            logger.info("Model Evaluation Started")

            model = joblib.load(self.model_path)

            features = joblib.load(self.feature_path)

            predictions = model.predict(features)

            os.makedirs(
                "artifacts/evaluation",
                exist_ok=True
            )

            prediction_file = os.path.join(
                "artifacts/evaluation",
                "predictions.csv"
            )

            df = pd.DataFrame()

            df["Prediction"] = predictions

            df.to_csv(
                prediction_file,
                index=False
            )

            anomaly_count = (predictions == -1).sum()

            normal_count = (predictions == 1).sum()

            logger.info(
                f"Normal Logs : {normal_count}"
            )

            logger.info(
                f"Anomaly Logs : {anomaly_count}"
            )

            logger.info(
                "Model Evaluation Completed"
            )

            return prediction_file

        except Exception as e:

            raise CustomException(e, sys)