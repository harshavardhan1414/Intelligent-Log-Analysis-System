import yaml

from src.constants import CONFIG_FILE_PATH

from src.entity.config_entity import DataIngestionConfig


class ConfigurationManager:

    def __init__(self):

        with open(CONFIG_FILE_PATH, "r") as yaml_file:

            self.config = yaml.safe_load(yaml_file)

    def get_data_ingestion_config(self):

        config = self.config["data_ingestion"]

        return DataIngestionConfig(

            dataset_path=config["dataset_path"],

            artifact_dir=config["artifact_dir"],

            raw_data_dir=config["raw_data_dir"],

            processed_data_dir=config["processed_data_dir"]

        )