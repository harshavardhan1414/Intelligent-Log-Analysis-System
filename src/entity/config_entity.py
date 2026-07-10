from dataclasses import dataclass


@dataclass(frozen=True)
class DataIngestionConfig:

    dataset_path: str

    artifact_dir: str

    raw_data_dir: str

    processed_data_dir: str