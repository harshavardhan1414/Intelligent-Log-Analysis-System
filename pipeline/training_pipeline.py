from src.configuration.configuration import ConfigurationManager
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.data_preprocessing import DataPreprocessing
from src.components.feature_engineering import FeatureEngineering

from src.utils.logger import logger
from src.utils.exception import CustomException

import sys


class TrainingPipeline:

    def __init__(self):
        pass

    def start_training_pipeline(self):

        try:

            logger.info("Training Pipeline Started")

            config = ConfigurationManager()

            data_ingestion_config = config.get_data_ingestion_config()

            data_ingestion = DataIngestion(data_ingestion_config)

            ingestion_artifact = data_ingestion.initiate_data_ingestion()

            validator = DataValidation(ingestion_artifact)

            validator.initiate_data_validation()
            transform = DataTransformation(ingestion_artifact)

            processed_path = transform.initiate_data_transformation()

            logger.info(f"Processed File Saved At : {processed_path}")
            preprocessing = DataPreprocessing(
                ingestion_artifact
            )

            cleaned_file = (
                preprocessing.initiate_data_preprocessing()
            )

            logger.info(
                f"Cleaned File Saved At : {cleaned_file}"
            )
            feature_engineering = FeatureEngineering(
    cleaned_file
)

            feature_path, vectorizer_path = (
    feature_engineering.initiate_feature_engineering()
)

            logger.info(
    f"Feature File : {feature_path}"
)

            logger.info(
    f"Vectorizer File : {vectorizer_path}"
)

            logger.info("Training Pipeline Completed")

            return ingestion_artifact

        except Exception as e:

            raise CustomException(e, sys)