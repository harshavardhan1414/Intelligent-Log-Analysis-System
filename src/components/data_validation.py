import os
import sys

from src.utils.logger import logger
from src.utils.exception import CustomException


class DataValidation:

    def __init__(self, data_ingestion_artifact):
        self.data_ingestion_artifact = data_ingestion_artifact

    def initiate_data_validation(self):

        try:

            logger.info("Data Validation Started")

            file_path = self.data_ingestion_artifact.raw_file_path

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"{file_path} not found")

            file_size = os.path.getsize(file_path)

            if file_size == 0:
                raise Exception("Dataset is Empty")

            logger.info(f"Dataset Size : {file_size} bytes")

            logger.info("Data Validation Completed Successfully")

            return True

        except Exception as e:

            raise CustomException(e, sys)