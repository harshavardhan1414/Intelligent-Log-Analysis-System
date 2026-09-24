import os
import sys

import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

from src.utils.logger import logger
from src.utils.exception import CustomException


class FeatureEngineering:

    def __init__(self, preprocessed_file):

        self.preprocessed_file = preprocessed_file

    def initiate_feature_engineering(self):

        logger.info("Feature Engineering Started")

        try:

           
            df = pd.read_csv(
                self.preprocessed_file
            )

            
            if "cleaned_message" not in df.columns:

                raise ValueError(
                    "cleaned_message column not found"
                )

           
            logs = (
                df["cleaned_message"]
                .fillna("")
                .astype(str)
                .tolist()
            )

            
            vectorizer = TfidfVectorizer(
                max_features=500
            )

           
            features = vectorizer.fit_transform(
                logs
            )

           
            os.makedirs(
                "artifacts/features",
                exist_ok=True
            )

            
            feature_path = os.path.join(
                "artifacts",
                "features",
                "features.pkl"
            )

           
            vectorizer_path = os.path.join(
                "artifacts",
                "features",
                "vectorizer.pkl"
            )

          
            joblib.dump(
                features,
                feature_path
            )

           

            joblib.dump(
                vectorizer,
                vectorizer_path
            )

            logger.info(
                f"Feature matrix shape: {features.shape}"
            )

            logger.info(
                f"Features saved to: {feature_path}"
            )

            logger.info(
                f"Vectorizer saved to: {vectorizer_path}"
            )

            logger.info(
                "Feature Engineering Completed Successfully"
            )

            return (
                feature_path,
                vectorizer_path
            )

        except Exception as e:

            logger.error(
                "Exception occurred during Feature Engineering"
            )

            raise CustomException(e, sys)