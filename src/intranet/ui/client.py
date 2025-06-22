"""
NiceGUI screen for managing client information using FastAPI endpoints.
"""
from nicegui import ui
import httpx
from src.intranet.conf.settings import config

API_URL = config.fastapi_url

def submit_client(e):
    payload = {
        'client_id': e['client_id'],
        'first_name': e['first_name'],
        'last_name': e['last_name'],
        'phone': e['phone'],
        'email': e['email']
    }
    try:
        response = httpx.post(API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        ui.notify(f"Client {data['first_name']} {data['last_name']} saved.")
    except httpx.HTTPStatusError as err:
        if err.response.status_code == 400:
            ui.notify("Client ID already exists.", color="negative")
        else:
            ui.notify(f"Error: {err.response.text}", color="negative")
    except Exception as ex:
        ui.notify(f"Unexpected error: {ex}", color="negative")

with ui.card():
    ui.label('Client Information').classes('text-h5')
    with ui.form(on_submit=submit_client):
        ui.input('Client ID', name='client_id', required=True)
        ui.input('First Name', name='first_name', required=True)
        ui.input('Last Name', name='last_name', required=True)
        ui.input('Phone', name='phone', required=True)
        ui.input('Email', name='email', required=True)
        ui.button('Save', type='submit')
