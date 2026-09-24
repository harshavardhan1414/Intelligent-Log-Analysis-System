import re
import sys

import pandas as pd

from src.utils.logger import logger
from src.utils.exception import CustomException


class DataTransformation:

    LOG_PATTERN = re.compile(
        r"^(?P<timestamp>.*?)\s+-\s+"
        r"(?P<logger_name>.*?)\s+-\s+"
        r"(?P<level>INFO|WARNING|ERROR|CRITICAL|DEBUG)\s+-\s+"
        r"(?P<message>.*)$"
    )

    def __init__(self, data_ingestion_artifact):

        self.data_ingestion_artifact = data_ingestion_artifact

    def initiate_data_transformation(self) -> str:

        logger.info("Data Transformation Started")

        try:

            
            source_path = (
                self.data_ingestion_artifact.raw_file_path
            )

            
            destination_path = (
                self.data_ingestion_artifact.processed_file_path
            )

            records = []

            skipped_records = 0

            
            with open(
                source_path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as file:

                for line_number, line in enumerate(
                    file,
                    start=1
                ):

                    line = line.strip()

                    if not line:
                        continue

                    match = self.LOG_PATTERN.match(line)

                    if not match:

                        skipped_records += 1

                        logger.warning(
                            f"Unable to parse line "
                            f"{line_number}"
                        )

                        continue

                    records.append(
                        match.groupdict()
                    )

            #
            df = pd.DataFrame(
                records,
                columns=[
                    "timestamp",
                    "logger_name",
                    "level",
                    "message"
                ]
            )

            if df.empty:

                raise ValueError(
                    "No valid log records were parsed"
                )

          
            df.to_csv(
                destination_path,
                index=False
            )

            logger.info(
                f"Parsed records: {len(df)}"
            )

            logger.info(
                f"Skipped records: {skipped_records}"
            )

            logger.info(
                f"Structured dataset saved to: "
                f"{destination_path}"
            )

            logger.info(
                "Data Transformation Completed Successfully"
            )

            return destination_path

        except Exception as e:

            logger.error(
                "Exception occurred during Data Transformation"
            )

            raise CustomException(e, sys)