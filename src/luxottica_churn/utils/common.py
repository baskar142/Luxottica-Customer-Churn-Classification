import os
import sys
import yaml
import json
import joblib
import pandas as pd
from box import ConfigBox
from box.exceptions import BoxValueError
from pathlib import Path
from typing import Any, Optional, List
from ensure import ensure_annotations
from datetime import datetime
import logging

# Initialize logger (assuming your logger.py is in the same utils folder)
from .logger import logger  # Relative import

# -----------------------------------------------------------
# CORE FILE & DIRECTORY OPERATIONS
# -----------------------------------------------------------

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Read a YAML file and return a ConfigBox for dot notation access.
    Raises:
        ValueError: If YAML is empty or invalid.
    """
    try:
        with open(path_to_yaml, 'r') as yaml_file:
            content = yaml.safe_load(yaml_file)
            if not content:
                raise BoxValueError("YAML file is empty")
            logger.info(f"YAML loaded: {path_to_yaml}")
            return ConfigBox(content)
    except Exception as e:
        logger.error(f"Error reading YAML at {path_to_yaml}: {e}")
        raise

@ensure_annotations
def create_directories(path_to_directories: List[Path], verbose: bool = True):
    """
    Create directories if they don't exist.
    Args:
        path_to_directories: List of directory paths
        verbose: Log creation events (default: True)
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory: {path}")

# -----------------------------------------------------------
# DATA SERIALIZATION
# -----------------------------------------------------------

@ensure_annotations
def save_json(path: Path, data: dict, indent: int = 4):
    """Save dictionary as JSON with pretty printing."""
    with open(path, 'w') as f:
        json.dump(data, f, indent=indent)
    logger.info(f"JSON saved: {path} (~{get_size(path)})")

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """Load JSON file into ConfigBox for dot notation access."""
    with open(path, 'r') as f:
        content = json.load(f)
    logger.info(f"JSON loaded: {path}")
    return ConfigBox(content)

@ensure_annotations
def save_bin(data: Any, path: Path):
    """Save binary data (e.g., models) using joblib."""
    joblib.dump(data, path)
    logger.info(f"Binary saved: {path} (~{get_size(path)})")

@ensure_annotations
def load_bin(path: Path) -> Any:
    """Load binary file (e.g., models)."""
    data = joblib.load(path)
    logger.info(f"Binary loaded: {path}")
    return data

# -----------------------------------------------------------
# DATA-SPECIFIC UTILITIES (FOR CHURN PROJECT)
# -----------------------------------------------------------

@ensure_annotations
def load_csv(path: Path, **kwargs) -> pd.DataFrame:
    """
    Load CSV with pandas and log shape.
    kwargs: Additional args for pd.read_csv()
    """
    df = pd.read_csv(path, **kwargs)
    logger.info(f"CSV loaded: {path} | Shape: {df.shape}")
    return df

@ensure_annotations
def save_csv(data: pd.DataFrame, path: Path, **kwargs):
    """Save DataFrame to CSV with validation."""
    data.to_csv(path, **kwargs)
    logger.info(f"CSV saved: {path} | Size: {get_size(path)}")

@ensure_annotations
def validate_data_schema(df: pd.DataFrame, schema_path: Path) -> bool:
    """
    Validate DataFrame against a schema YAML.
    Schema Example:
        required_columns: [customer_id, last_purchase_date]
        dtypes:
            customer_id: str
            churn: int
    """
    schema = read_yaml(schema_path)
    
    # Check required columns
    missing_cols = set(schema.required_columns) - set(df.columns)
    if missing_cols:
        logger.error(f"Missing columns: {missing_cols}")
        raise ValueError(f"Schema validation failed. Missing: {missing_cols}")
    
    # Check dtypes (optional)
    for col, dtype in schema.dtypes.items():
        if col in df.columns and not pd.api.types.is_dtype_equal(df[col].dtype, dtype):
            logger.warning(f"Column '{col}' has dtype {df[col].dtype}, expected {dtype}")
    
    logger.info("Data schema validation passed")
    return True

# -----------------------------------------------------------
# MODEL-SPECIFIC UTILITIES
# -----------------------------------------------------------

@ensure_annotations
def save_model(model: Any, path: Path, metadata: Optional[dict] = None):
    """
    Save model with optional metadata.
    Example metadata:
        {"algorithm": "XGBoost", "training_date": "2023-10-05"}
    """
    save_bin(model, path)
    if metadata:
        metadata_path = Path(f"{path}.metadata.json")
        save_json(metadata_path, metadata)
        logger.info(f"Model metadata saved: {metadata_path}")

@ensure_annotations
def load_model(path: Path) -> Any:
    """Load model and its metadata if available."""
    model = load_bin(path)
    metadata_path = Path(f"{path}.metadata.json")
    if metadata_path.exists():
        metadata = load_json(metadata_path)
        logger.info(f"Model metadata: {metadata}")
    return model

# -----------------------------------------------------------
# MISC UTILITIES
# -----------------------------------------------------------

@ensure_annotations
def get_size(path: Path) -> str:
    """Get file size in human-readable format (KB/MB)."""
    size_bytes = os.path.getsize(path)
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes / (1024**2):.2f} MB"

# -----------------------------------------------------------
# EXAMPLE USAGE (FOR TESTING)
# -----------------------------------------------------------
if __name__ == "__main__":
    # Test directory creation
    test_dir = Path("test_dir")
    create_directories([test_dir])
    
    # Test YAML operations
    test_yaml = Path("test_config.yaml")
    save_json(test_yaml, {"test_key": "test_value"})
    yaml_content = read_yaml(test_yaml)
    print(f"YAML Content: {yaml_content}")
    
    # Cleanup
    os.remove(test_yaml)
    os.rmdir(test_dir)