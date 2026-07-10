from src.configuration.configuration import ConfigurationManager

config=ConfigurationManager()

print(config.get_data_ingestion_config())

print(config.get_artifact_config())

print(config.get_logging_config())