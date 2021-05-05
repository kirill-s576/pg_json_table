import os
from dotenv import load_dotenv
from pathlib import Path


ENV_FILE_PATH = 'variables.env'

# Load environments
env_path = Path(ENV_FILE_PATH)
load_dotenv(dotenv_path=env_path)
##

POSTGRES_USER = os.environ.get("POSTGRES_USER", None)
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", None)
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", None)
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", None)
POSTGRES_DB = os.environ.get("POSTGRES_DB", None)
