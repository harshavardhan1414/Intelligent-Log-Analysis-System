from src.configuration.configuration import ConfigurationManager

config = ConfigurationManager()

data = config.get_data_ingestion_config()

print(data)