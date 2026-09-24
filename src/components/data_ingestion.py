import os
import shutil
import sys

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.utils.logger import logger
from src.utils.exception import CustomException


class DataIngestion:

    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def initiate_data_ingestion(self) -> DataIngestionArtifact:

        logger.info("Data ingestion started")

        try:

           
            os.makedirs(
                self.config.artifact_dir,
                exist_ok=True
            )

            os.makedirs(
                self.config.raw_data_dir,
                exist_ok=True
            )

            os.makedirs(
                self.config.processed_data_dir,
                exist_ok=True
            )

            logger.info("Artifact directories created successfully")

           
            source_file = self.config.dataset_path

            if not os.path.isfile(source_file):
                raise FileNotFoundError(
                    f"Dataset not found: {source_file}"
                )

            logger.info(
                f"Input log dataset found: {source_file}"
            )

            
            destination_file = os.path.join(
                self.config.raw_data_dir,
                os.path.basename(source_file)
            )

            
            shutil.copy2(
                source_file,
                destination_file
            )

            logger.info(
                f"Raw log artifact created: {destination_file}"
            )

           
            total_lines = 0

            with open(
                destination_file,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as file:

                for line in file:
                    if line.strip():
                        total_lines += 1

            logger.info(
                f"Total log records found: {total_lines}"
            )

          
            processed_file = os.path.join(
                self.config.processed_data_dir,
                "parsed_logs.csv"
            )

           
            data_ingestion_artifact = DataIngestionArtifact(

                raw_file_path=destination_file,

                processed_file_path=processed_file,

                status=True,

                message=(
                    f"Successfully ingested log dataset. "
                    f"Total records: {total_lines}"
                )
            )

            logger.info(
                "Data ingestion completed successfully"
            )

            return data_ingestion_artifact

        except Exception as e:

            logger.error(
                "Exception occurred during data ingestion"
            )

            raise CustomException(e, sys)