import os
import sys
import joblib

from sklearn.ensemble import IsolationForest

from src.utils.logger import logger
from src.utils.exception import CustomException


class ModelTrainer:

    def __init__(self, feature_path):

        self.feature_path = feature_path

    def initiate_model_training(self):

        try:

            logger.info("Model Training Started")

            features = joblib.load(self.feature_path)

            model = IsolationForest(

                contamination=0.05,

                random_state=42

            )

            model.fit(features)

            os.makedirs(

                "artifacts/model",

                exist_ok=True

            )

            model_path = os.path.join(

                "artifacts/model",

                "model.pkl"

            )

            joblib.dump(

                model,

                model_path

            )

            logger.info("Model Saved Successfully")

            return model_path

        except Exception as e:

            raise CustomException(e, sys)