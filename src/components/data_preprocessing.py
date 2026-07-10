import os
import sys

from src.utils.logger import logger
from src.utils.exception import CustomException


class DataPreprocessing:

    def __init__(self, data_ingestion_artifact):

        self.data_ingestion_artifact = data_ingestion_artifact

    def initiate_data_preprocessing(self):

        try:

            logger.info("Data Preprocessing Started")

            input_file = self.data_ingestion_artifact.raw_file_path

            output_file = os.path.join(
                "artifacts",
                "processed_data",
                "cleaned_logs.txt"
            )

            os.makedirs(
                os.path.dirname(output_file),
                exist_ok=True
            )

            unique_logs = set()

            total_lines = 0

            cleaned_lines = 0

            with open(
                input_file,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as infile, open(
                output_file,
                "w",
                encoding="utf-8"
            ) as outfile:

                for line in infile:

                    total_lines += 1

                    line = line.strip()

                    if line == "":
                        continue

                    if line not in unique_logs:

                        unique_logs.add(line)

                        outfile.write(line + "\n")

                        cleaned_lines += 1

                    if total_lines % 100000 == 0:

                        logger.info(
                            f"{total_lines} lines processed..."
                        )

            logger.info(f"Total Lines : {total_lines}")

            logger.info(f"Cleaned Lines : {cleaned_lines}")

            logger.info("Data Preprocessing Completed Successfully")

            return output_file

        except Exception as e:

            raise CustomException(e, sys)