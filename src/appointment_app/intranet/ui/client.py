"""
NiceGUI screen for managing client information using FastAPI endpoints.
"""
from nicegui import ui
import httpx
from appointment_app.intranet.conf.settings import config

API_URL = config.fastapi_url

client_fields = {}

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
    client_fields['client_id'] = ui.input('Client ID')
    client_fields['first_name'] = ui.input('First Name')
    client_fields['last_name'] = ui.input('Last Name')
    client_fields['phone'] = ui.input('Phone')
    client_fields['email'] = ui.input('Email')
    ui.button('Save', on_click=submit_client)

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(port=8080)
