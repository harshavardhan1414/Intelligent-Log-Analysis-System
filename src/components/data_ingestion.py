import os
import shutil

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.utils.logger import logger
from src.utils.exception import CustomException

import sys


class DataIngestion:

    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def initiate_data_ingestion(self):

        logger.info("Data Ingestion Started")

        try:

            # Create artifact directories
            os.makedirs(self.config.artifact_dir, exist_ok=True)

            os.makedirs(self.config.raw_data_dir, exist_ok=True)

            os.makedirs(self.config.processed_data_dir, exist_ok=True)

            logger.info("Artifact directories created successfully")

            source_file = self.config.dataset_path

            if not os.path.exists(source_file):

                raise FileNotFoundError(
                    f"Dataset not found : {source_file}"
                )

            logger.info(f"Dataset Found : {source_file}")

            destination_file = os.path.join(

                self.config.raw_data_dir,

                "HDFS.log"

            )

            logger.info("Copying Dataset to Artifacts")

            shutil.copy2(

                source_file,

                destination_file

            )

            logger.info("Dataset Copied Successfully")

            processed_file = os.path.join(

                self.config.processed_data_dir,

                "processed_logs.csv"

            )

            logger.info("Starting Line By Line Reading")

            total_lines = 0

            with open(destination_file, "r", encoding="utf-8", errors="ignore") as file:

                for line in file:

                    total_lines += 1

                    if total_lines % 100000 == 0:

                        logger.info(
                            f"{total_lines} Lines Processed"
                        )

            logger.info(f"Total Lines : {total_lines}")

            logger.info("Data Ingestion Completed Successfully")
            data_ingestion_artifact = DataIngestionArtifact(

                raw_file_path=destination_file,

                processed_file_path=processed_file,

                status=True,

                message=f"Successfully copied dataset. Total Lines : {total_lines}"

            )

            logger.info("Returning Data Ingestion Artifact")

            return data_ingestion_artifact

        except Exception as e:

            logger.error("Exception occurred during Data Ingestion")

            raise CustomException(e, sys)