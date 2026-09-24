import os
import sys
import joblib
import mlflow
import mlflow.sklearn

from sklearn.ensemble import IsolationForest

from src.utils.logger import logger
from src.utils.exception import CustomException


class ModelTrainer:

    def __init__(self, feature_path):
        self.feature_path = feature_path

    def initiate_model_training(self):

        try:

            logger.info("Model Training Started")

  
            features = joblib.load(
                self.feature_path
            )

            logger.info(
                f"Feature Matrix Shape: {features.shape}"
            )

            contamination = 0.05
            random_state = 42

            model = IsolationForest(
                contamination=contamination,
                random_state=random_state
            )

            
            mlflow.set_tracking_uri(
                "sqlite:///mlflow.db"
            )

            mlflow.set_experiment(
                "Intelligent_Log_Analysis"
            )

            
            with mlflow.start_run():

                # Train Model
                model.fit(features)

                logger.info(
                    "Isolation Forest Training Completed"
                )

               
                mlflow.log_param(
                    "model",
                    "IsolationForest"
                )

                mlflow.log_param(
                    "contamination",
                    contamination
                )

                mlflow.log_param(
                    "random_state",
                    random_state
                )

                
                mlflow.log_metric(
                    "number_of_samples",
                    features.shape[0]
                )

                mlflow.log_metric(
                    "number_of_features",
                    features.shape[1]
                )

               
                model_dir = "artifacts/model"

                os.makedirs(
                    model_dir,
                    exist_ok=True
                )

               
                model_path = os.path.join(
                    model_dir,
                    "model.pkl"
                )

               
                joblib.dump(
                    model,
                    model_path
                )

                
                mlflow.sklearn.log_model(
                    sk_model=model,
                    name="IsolationForestModel"
                )

            logger.info(
                f"Model Saved Successfully: {model_path}"
            )

            return model_path

        except Exception as e:

            raise CustomException(
                e,
                sys
            )