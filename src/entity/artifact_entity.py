from dataclasses import dataclass


@dataclass(frozen=True)
class DataIngestionArtifact:

    raw_file_path: str

    processed_file_path: str

    status: bool

    message: str