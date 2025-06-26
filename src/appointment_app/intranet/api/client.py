"""
API endpoints for client management.
"""
from fastapi import APIRouter, HTTPException
from appointment_app.intranet.models.client import Client

router = APIRouter(prefix="/clients", tags=["clients"])

# In-memory store for demonstration (replace with DB in production)
clients_db = {}

@router.post("/", response_model=Client)
def create_client(client: Client) -> Client:
    """Create a new client."""
    if client.client_id in clients_db:
        raise HTTPException(status_code=400, detail="Client ID already exists.")
    clients_db[client.client_id] = client
    return client

@router.get("/{client_id}", response_model=Client)
def get_client(client_id: str) -> Client:
    """Retrieve client information by ID."""
    client = clients_db.get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found.")
    return client
