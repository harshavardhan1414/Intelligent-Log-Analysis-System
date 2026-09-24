from pipeline.prediction_pipeline import PredictionPipeline

from src.utils.logger import logger


if __name__ == "__main__":

    predictor = PredictionPipeline()

    log = input("Enter Log Message : ")

    prediction = predictor.predict(log)

    print("\nPrediction :", prediction)