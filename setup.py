from setuptools import setup, find_packages
import pathlib

# Read the long description from README
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

# Core project metadata
PROJECT_NAME = "Luxottica-Customer-Churn-Classification"
VERSION = "0.1.0"
AUTHOR = "Baskaran Pandiyan"
AUTHOR_EMAIL = "baskaranpandiyan14@gmail.com"
REPO_URL = "https://github.com/baskar142/Luxottica-Customer-Churn-Classification"
SHORT_DESCRIPTION = "Machine learning pipeline for predicting customer churn in Luxottica eyewear business"

# Package requirements
CORE_REQUIREMENTS = [
    "scikit-learn==1.0.2",
    "pandas==1.5.3",
    "numpy==1.23.5",
    "xgboost==1.6.2",
    "imbalanced-learn==0.10.1"
]

AWS_REQUIREMENTS = [
    "boto3==1.26.142",
    "awscli==1.27.142",
    "sagemaker==2.162.0"
]

DEV_REQUIREMENTS = [
    "pytest==7.4.0",
    "pytest-cov==4.1.0",
    "mypy==1.5.1",
    "black==23.7.0",
    "jupyter==1.0.0"
]

API_REQUIREMENTS = [
    "fastapi==0.95.2",
    "uvicorn==0.22.0",
    "python-multipart==0.0.6"
]

setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=SHORT_DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=REPO_URL,
    project_urls={
        "Bug Tracker": f"{REPO_URL}/issues",
        "Documentation": f"{REPO_URL}/wiki",
        "Source Code": REPO_URL,
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9, <3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Data Science Team",
        "Topic :: Software Development :: Machine Learning",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    install_requires=CORE_REQUIREMENTS,
    extras_require={
        "dev": DEV_REQUIREMENTS,
        "aws": AWS_REQUIREMENTS,
        "api": API_REQUIREMENTS,
        "all": CORE_REQUIREMENTS + AWS_REQUIREMENTS + API_REQUIREMENTS + DEV_REQUIREMENTS
    },
    entry_points={
        "console_scripts": [
            "luxottica-train=luxottica_churn.pipeline.training_pipeline:main",
            "luxottica-predict=luxottica_churn.pipeline.prediction_pipeline:main",
        ],
    },
    include_package_data=True,
    package_data={
        "luxottica_churn": ["config/*.yaml", "schemas/*.yaml"]
    },
)