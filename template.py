import os
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Project structure for ML with AWS deployment
project_name = "luxottica_churn"
current_date = datetime.now().strftime("%Y-%m-%d")

list_of_files = [
    # Infrastructure
    "Dockerfile",
    "requirements.txt",
    ".dockerignore",
    ".gitignore",
    
    # Core ML structure
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/components/data_ingestion.py",
    f"src/{project_name}/components/data_transformation.py",
    f"src/{project_name}/components/model_trainer.py",
    f"src/{project_name}/components/model_evaluation.py",
    
    # AWS specific
    f"src/{project_name}/lambda/__init__.py",
    f"src/{project_name}/lambda/handler.py",
    "infra/terraform/main.tf",
    
    # Configuration
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    "config/config.yaml",
    "config/aws_config.yaml",
    "params.yaml",
    "schema.yaml",
    
    # Utilities
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/utils/aws_utils.py",
    
    # Pipeline
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/pipeline/training_pipeline.py",
    f"src/{project_name}/pipeline/prediction_pipeline.py",
    
    # Entities
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/entity/artifact_entity.py",
    
    # Constants
    f"src/{project_name}/constants/__init__.py",
    
    # Application
    "main.py",
    "app.py",
    "setup.py",
    
    # Research
    f"research/{current_date}_trials.ipynb",
    f"research/{current_date}_eda.ipynb",
    
    # API templates
    "templates/index.html",
    "static/css/main.css",
    
    # Tests
    "tests/__init__.py",
    "tests/test_data_validation.py",
    
    # Documentation
    "docs/api_spec.yaml"
]

def create_project_structure():
    try:
        for filepath in list_of_files:
            filepath = Path(filepath)
            filedir = filepath.parent
            
            # Create directory if needed
            if not filedir.exists():
                filedir.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {filedir}")
            
            # Create empty file if it doesn't exist
            if not filepath.exists() or os.path.getsize(filepath) == 0:
                with open(filepath, 'w') as f:
                    if filepath.suffix == '.py':
                        f.write(f'# {project_name}\n# Created on {current_date}\n\n"""\nModule docstring\n"""\n')
                    elif filepath.name == 'Dockerfile':
                        f.write(f'# {project_name} Dockerfile\nFROM python:3.9-slim\n\nWORKDIR /app\n\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\n\nCOPY . .\n\nCMD ["python", "app.py"]')
                logger.info(f"Created file: {filepath}")
            else:
                logger.info(f"File exists: {filepath}")
                
        logger.info("Project structure created successfully!")
        
    except Exception as e:
        logger.error(f"Error creating project structure: {str(e)}")
        raise

if __name__ == "__main__":
    create_project_structure()