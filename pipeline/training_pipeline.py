def start_training_pipeline(self):

    try:

        logger.info("Training Pipeline Started")

       
        config = ConfigurationManager()

        data_ingestion_config = (
            config.get_data_ingestion_config()
        )

        
        data_ingestion = DataIngestion(
            data_ingestion_config
        )

        ingestion_artifact = (
            data_ingestion.initiate_data_ingestion()
        )

       
        validator = DataValidation(
            ingestion_artifact
        )

        validation_status = (
            validator.initiate_data_validation()
        )

        if not validation_status:

            raise ValueError(
                "Data validation failed"
            )

        
        transformation = DataTransformation(
            ingestion_artifact
        )

        transformed_file = (
            transformation.initiate_data_transformation()
        )

        logger.info(
            f"Transformed file: {transformed_file}"
        )

        
        preprocessing = DataPreprocessing(
            transformed_file
        )

        preprocessed_file = (
            preprocessing.initiate_data_preprocessing()
        )

        logger.info(
            f"Preprocessed file: {preprocessed_file}"
        )

       
        feature_engineering = FeatureEngineering(
            preprocessed_file
        )

        feature_path, vectorizer_path = (
            feature_engineering
            .initiate_feature_engineering()
        )

        logger.info(
            f"Feature file: {feature_path}"
        )

        logger.info(
            f"Vectorizer file: {vectorizer_path}"
        )

       
        trainer = ModelTrainer(
            feature_path
        )

        model_path = (
            trainer.initiate_model_training()
        )

        logger.info(
            f"Model saved at: {model_path}"
        )

       
        evaluation = ModelEvaluation(
            model_path,
            feature_path,
            preprocessed_file
        )

        prediction_file = (
            evaluation.initiate_model_evaluation()
        )

        logger.info(
            f"Prediction file: {prediction_file}"
        )

       
        logger.info(
            "Training Pipeline Completed"
        )

        return ingestion_artifact

    except Exception as e:

        raise CustomException(e, sys)