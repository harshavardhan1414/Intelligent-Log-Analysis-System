import os
import shutil
import sys

from src.utils.logger import logger
from src.utils.exception import CustomException


class DataTransformation:

    def __init__(self, data_ingestion_artifact):
        self.data_ingestion_artifact = data_ingestion_artifact

    def initiate_data_transformation(self):

        try:

            logger.info("Data Transformation Started")

            source_path = self.data_ingestion_artifact.raw_file_path

            destination_path = self.data_ingestion_artifact.processed_file_path

            shutil.copy2(
                source_path,
                destination_path
            )

            logger.info("Data Transformation Completed")

            return destination_path

        except Exception as e:

            raise CustomException(e, sys)