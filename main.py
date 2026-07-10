from pipeline.training_pipeline import TrainingPipeline

from src.utils.logger import logger
from src.utils.exception import CustomException

import sys


if __name__ == "__main__":

    try:

        logger.info("Project Execution Started")

        pipeline = TrainingPipeline()

        artifact = pipeline.start_training_pipeline()

        print(artifact)

        logger.info("Project Execution Completed")

    except Exception as e:

        raise CustomException(e, sys)