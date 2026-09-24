import os
import re
import sys

import pandas as pd

from src.utils.logger import logger
from src.utils.exception import CustomException


class DataPreprocessing:

    def __init__(self, transformed_file):

        self.transformed_file = transformed_file

    def initiate_data_preprocessing(self) -> str:

        logger.info("Data Preprocessing Started")

        try:

            
            df = pd.read_csv(
                self.transformed_file
            )

            logger.info(
                f"Input records: {len(df)}"
            )

            
            required_columns = [
                "timestamp",
                "logger_name",
                "level",
                "message"
            ]

            missing_columns = [
                column
                for column in required_columns
                if column not in df.columns
            ]

            if missing_columns:

                raise ValueError(
                    f"Missing required columns: "
                    f"{missing_columns}"
                )

           
            df = df.dropna(
                subset=["message"]
            ).copy()

            
            df["message"] = (
                df["message"]
                .astype(str)
                .str.strip()
            )

            
            df = df[
                df["message"] != ""
            ].copy()

         
            df["cleaned_message"] = (
                df["message"]
                .str.lower()
                .str.replace(
                    r"\s+",
                    " ",
                    regex=True
                )
                .str.strip()
            )

            
            df["cleaned_message"] = (
                df["cleaned_message"]
                .str.replace(
                    r"[^\w\s]",
                    " ",
                    regex=True
                )
                .str.replace(
                    r"\s+",
                    " ",
                    regex=True
                )
                .str.strip()
            )

           
            output_file = os.path.join(
                "artifacts",
                "processed_data",
                "preprocessed_logs.csv"
            )

            os.makedirs(
                os.path.dirname(output_file),
                exist_ok=True
            )

            df.to_csv(
                output_file,
                index=False
            )

            logger.info(
                f"Output records: {len(df)}"
            )

            logger.info(
                f"Preprocessed dataset saved to: "
                f"{output_file}"
            )

            logger.info(
                "Data Preprocessing Completed Successfully"
            )

            return output_file

        except Exception as e:

            logger.error(
                "Exception occurred during Data Preprocessing"
            )

            raise CustomException(e, sys)