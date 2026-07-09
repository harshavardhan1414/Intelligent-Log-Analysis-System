import os

folders = [
".github/workflows",
"artifacts",
"config",
"data/raw",
"data/processed",
"data/external",
"docs",
"logs",
"mlruns",
"models",
"notebooks",
"pipeline",
"src/components",
"src/utils",
"src/entity",
"src/configuration",
"src/constants",
"app/templates",
"app/static",
"tests"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

files = [
"pipeline/__init__.py",
"pipeline/training_pipeline.py",
"pipeline/prediction_pipeline.py",

"src/__init__.py",

"src/components/__init__.py",
"src/components/data_ingestion.py",
"src/components/data_validation.py",
"src/components/data_transformation.py",
"src/components/model_trainer.py",
"src/components/model_evaluation.py",
"src/components/model_pusher.py",

"src/utils/__init__.py",
"src/utils/logger.py",
"src/utils/exception.py",
"src/utils/common.py",

"src/entity/config_entity.py",
"src/entity/artifact_entity.py",

"src/configuration/configuration.py",

"src/constants/__init__.py",

"app/main.py",
"app/prediction.py",

"requirements.txt",
"Dockerfile",
"docker-compose.yml",
"dvc.yaml",
"params.yaml",
"setup.py",
"pyproject.toml",
".gitignore",
"README.md",
"main.py",
"config/config.yaml"
]

for file in files:
    open(file,'a').close()

print("Project Structure Created Successfully")