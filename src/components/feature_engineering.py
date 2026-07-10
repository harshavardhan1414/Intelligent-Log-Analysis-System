import os
import sys
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer

from src.utils.logger import logger
from src.utils.exception import CustomException


class FeatureEngineering:

    def __init__(self, cleaned_file):

        self.cleaned_file = cleaned_file

    def initiate_feature_engineering(self):

        try:

            logger.info("Feature Engineering Started")

            with open(
                self.cleaned_file,
                "r",
                encoding="utf-8"
            ) as file:

                logs = file.readlines()

            logs = [line.strip() for line in logs]

            vectorizer = TfidfVectorizer(
                max_features=500
            )

            features = vectorizer.fit_transform(logs)

            os.makedirs(
                "artifacts/features",
                exist_ok=True
            )

            feature_path = os.path.join(
                "artifacts/features",
                "features.pkl"
            )

            vectorizer_path = os.path.join(
                "artifacts/features",
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

            logger.info("Feature Engineering Completed")

            return feature_path, vectorizer_path

        except Exception as e:

            raise CustomException(e, sys)