import os
import re
import sys

from src.utils.logger import logger
from src.utils.exception import CustomException


class DataValidation:

    LOG_PATTERN = re.compile(
        r"^(?P<timestamp>.*?)\s+-\s+"
        r"(?P<logger_name>.*?)\s+-\s+"
        r"(?P<level>INFO|WARNING|ERROR|CRITICAL|DEBUG)\s+-\s+"
        r"(?P<message>.*)$"
    )

    def __init__(self, data_ingestion_artifact):

        self.data_ingestion_artifact = data_ingestion_artifact

    def initiate_data_validation(self) -> bool:

        logger.info("Data Validation Started")

        try:

            
            file_path = (
                self.data_ingestion_artifact.raw_file_path
            )

           
            if not os.path.isfile(file_path):

                raise FileNotFoundError(
                    f"Dataset not found: {file_path}"
                )

            
            file_size = os.path.getsize(file_path)

            if file_size == 0:

                raise ValueError(
                    "Dataset is empty"
                )

            logger.info(
                f"Dataset size: {file_size} bytes"
            )

            
            total_lines = 0
            valid_lines = 0

            with open(
                file_path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as file:

                for line in file:

                    line = line.strip()

                    if not line:
                        continue

                    total_lines += 1

                    if self.LOG_PATTERN.match(line):
                        valid_lines += 1

          
            if total_lines == 0:

                raise ValueError(
                    "Dataset contains no valid records"
                )

           
            validation_ratio = (
                valid_lines / total_lines
            )

            logger.info(
                f"Total records: {total_lines}"
            )

            logger.info(
                f"Valid records: {valid_lines}"
            )

            logger.info(
                f"Validation ratio: {validation_ratio:.2%}"
            )

            if validation_ratio < 0.95:

                raise ValueError(
                    "More than 5% of log records do not "
                    "match the expected log format"
                )

            logger.info(
                "Data Validation Completed Successfully"
            )

            return True

        except Exception as e:

            logger.error(
                "Exception occurred during Data Validation"
            )

            raise CustomException(e, sys)