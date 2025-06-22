"""Configuration settings using Box."""
from box import Box
import os

config = Box({
    'firestore_project': os.getenv('FIRESTORE_PROJECT'),
    'gcp_storage_bucket': os.getenv('GCP_STORAGE_BUCKET'),
    'api_key': os.getenv('API_KEY'),
    'db_url': os.getenv('DB_URL'),
    'fastapi_url': os.getenv("FASTAPI_URL", "http://localhost:6500/clients/"),
})
