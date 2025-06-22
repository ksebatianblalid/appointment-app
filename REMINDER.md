# Implementación de Recordatorios de Citas con Python en GCP

Esta guía detalla cómo crear un sistema automatizado de recordatorios de citas por email y WhatsApp utilizando servicios de Google Cloud Platform. La lógica se implementará en Python.

## Arquitectura General

El sistema se compone de las siguientes piezas clave que trabajan en conjunto:

*   **Firestore:** Base de datos NoSQL para almacenar la información de las citas.
*   **Cloud Function o Cloud Run:** La lógica de backend escrita en Python que se encarga de procesar las citas.
*   **Cloud Scheduler:** El servicio de cron que activa nuestra lógica una vez al día.
*   **SendGrid:** Servicio externo para el envío fiable de emails.
*   **Twilio:** Servicio externo con una API para enviar mensajes de WhatsApp.

### Flujo de Datos

```
                  ┌──────────────────┐
                  │ Cloud Scheduler  │ (Ej: "Todos los días a las 9 AM")
                  └─────────┬────────┘
                            │ 1. Invoca (vía HTTP)
                            ▼
      ┌───────────────────────────────────────────┐
      │ GCP Serverless (Cloud Function / Cloud Run) │
      └──────────────────┬────────────────────────┘
                         │ 2. Lee las citas de "mañana"
                         ▼
               ┌──────────────────┐
               │    Firestore     │
               └─────────┬────────┘
                         │ 3. Para cada cita encontrada...
     ┌───────────────────┴───────────────────┐
     │ 4a. Llama a la API de SendGrid       │ 4b. Llama a la API de Twilio
     ▼                                      ▼
┌───────────────┐                      ┌────────────────┐
│      Email    │                      │    WhatsApp    │
└───────────────┘                      └────────────────┘
```

---

## Paso 1: Configurar Firestore

La base de tu sistema es una base de datos bien estructurada.

1.  Asegúrate de tener una base de datos Firestore creada en tu proyecto de GCP.
2.  Crea una colección llamada `citas`.
3.  Cada documento dentro de `citas` debe tener una estructura similar a esta.

**Ejemplo de documento en la colección `citas`:**

```json
{
  "nombreCliente": "Ana Pérez",
  "emailCliente": "ana.perez@email.com",
  "telefonoCliente": "+34600123456",
  "fechaCita": "2023-10-27T17:00:00.000Z",
  "descripcion": "Revisión Anual",
  "recordatorioEnviado": false
}
```

> **Nota Importante:** Es **crucial** guardar `fechaCita` como un objeto **Timestamp** de Firestore y siempre en **UTC**. Esto previene cualquier confusión con las zonas horarias. El campo `recordatorioEnviado` es vital para evitar el envío de recordatorios duplicados.

---

## Paso 2: Configurar Servicios de Terceros

Necesitarás cuentas y credenciales de API para enviar los mensajes.

1.  **SendGrid (Email):**
    *   Crea una cuenta en [SendGrid](https://sendgrid.com/).
    *   Verifica un dominio o un email de remitente.
    *   Ve a `Settings` -> `API Keys` y crea una nueva **API Key**. Guárdala en un lugar seguro.

2.  **Twilio (WhatsApp):**
    *   Crea una cuenta en [Twilio](https://www.twilio.com/).
    *   Desde tu consola, anota tu **Account SID** y tu **Auth Token**.
    *   Para pruebas, configura el [Twilio Sandbox for WhatsApp](https://www.twilio.com/console/sms/whatsapp/sandbox). Esto te permite enviar mensajes a números verificados sin un perfil de WhatsApp Business completo.
    *   **Para producción**, necesitarás crear y obtener la aprobación de **plantillas de mensajes** en Twilio.

---

## Paso 3: Implementar la Lógica de Backend (Python)

Aquí tienes dos opciones excelentes. Elige la que mejor se adapte a tu proyecto.

### Opción A: Cloud Function (Recomendado por su simplicidad)

Ideal si esta es una tarea aislada.

1.  En la consola de GCP, ve a **Cloud Functions** y haz clic en **Crear Función**.
2.  **Configuración:**
    *   **Entorno:** `2ª gen`.
    *   **Nombre de la función:** `enviar-recordatorios-citas-py`.
    *   **Activador:** `HTTP`.
    *   **Autenticación:** `Requerir autenticación`.
3.  **Código Fuente:**
    *   **Entorno de ejecución:** `Python 3.11` (o la versión más reciente).
    *   **Punto de entrada:** `send_reminders`.
    *   Crea los siguientes dos archivos.

**`requirements.txt`**

```txt
functions-framework==3.*
google-cloud-firestore==2.*
sendgrid==6.*
twilio==8.*
pytz==2023.3
```

**`main.py`**

```python
import os
import functions_framework
from datetime import datetime, timedelta, timezone
import pytz

from google.cloud import firestore
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client

# --- Inicializar Clientes ---
# Las credenciales de GCP (para Firestore) se infieren automáticamente.
db = firestore.Client()

# Cargar API keys de las variables de entorno
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')

sg_client = SendGridAPIClient(SENDGRID_API_KEY)
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@functions_framework.http
def send_reminders(request):
    """Cloud Function activada por HTTP para enviar recordatorios de citas."""
    # 1. Calcular el rango de fechas para "mañana" en UTC
    now_utc = datetime.now(timezone.utc)
    start_of_tomorrow_utc = (now_utc + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_tomorrow_utc = start_of_tomorrow_utc + timedelta(days=1)

    print(f"Buscando citas entre {start_of_tomorrow_utc.isoformat()} y {end_of_tomorrow_utc.isoformat()}")

    try:
        # 2. Consultar Firestore
        citas_ref = db.collection('citas')
        query = citas_ref \
            .where(field_path='fechaCita', op_string='>=', value=start_of_tomorrow_utc) \
            .where(field_path='fechaCita', op_string='<', value=end_of_tomorrow_utc) \
            .where(field_path='recordatorioEnviado', op_string='==', value=False)

        for doc in query.stream():
            cita = doc.to_dict()
            print(f"Procesando cita ID: {doc.id} para: {cita.get('nombreCliente')}")

            # Convertir fecha a zona horaria local para el mensaje (ej. Madrid)
            madrid_tz = pytz.timezone("Europe/Madrid")
            hora_local_str = cita['fechaCita'].astimezone(madrid_tz).strftime('%H:%M')

            # 3. Enviar notificaciones
            if cita.get('emailCliente'):
                send_email(cita, hora_local_str)
            if cita.get('telefonoCliente'):
                send_whatsapp(cita, hora_local_str)
            
            # 4. Marcar como enviado
            doc.reference.update({'recordatorioEnviado': True})
        
        return "Proceso completado.", 200

    except Exception as e:
        print(f"Error al enviar recordatorios: {e}")
        return "Error interno del servidor.", 500

def send_email(cita, hora_local):
    """Función auxiliar para enviar email."""
    message = Mail(
        from_email=('tu-email@verificado.com', 'Nombre de tu Empresa'),
        to_emails=cita['emailCliente'],
        subject=f"Recordatorio de tu cita: {cita.get('descripcion', '')}",
        html_content=f"<h1>¡Hola {cita['nombreCliente']}!</h1><p>Te recordamos tu cita de mañana a las <strong>{hora_local}</strong>.</p><p>¡Te esperamos!</p>"
    )
    try:
        sg_client.send(message)
        print(f"Email enviado a {cita['emailCliente']}")
    except Exception as e:
        print(f"Error enviando email: {e}")

def send_whatsapp(cita, hora_local):
    """Función auxiliar para enviar WhatsApp."""
    message_body = f"Hola {cita['nombreCliente']}, te recordamos tu cita de \"{cita.get('descripcion', '')}\" para mañana a las {hora_local}. ¡Te esperamos!"
    try:
        message = twilio_client.messages.create(
            body=message_body,
            from_='whatsapp:+14155238886',  # Número del Sandbox de Twilio
            to=f"whatsapp:{cita['telefonoCliente']}"
        )
        print(f"WhatsApp enviado a {cita['telefonoCliente']} (SID: {message.sid})")
    except Exception as e:
        print(f"Error enviando WhatsApp: {e}")

```

4.  **Variables de Entorno:**
    *   En la configuración de la función, ve a la pestaña `Variables, redes y secretos`.
    *   En **Variables de entorno de tiempo de ejecución**, añade tus secretos.
        *   `SENDGRID_API_KEY` = `SG.xxxxxxxx...`
        *   `TWILIO_ACCOUNT_SID` = `ACxxxxxxxx...`
        *   `TWILIO_AUTH_TOKEN` = `your_auth_token`
    *   **Despliega** la función.

