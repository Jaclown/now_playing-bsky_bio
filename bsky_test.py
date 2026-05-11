from atproto import Client

# Conectar con bsky usando app de aplicación y los datos del .env del proyecto por seguridad
import os
from dotenv import load_dotenv

# Cargar las variables del .env y meterlos en entorno del sistema
load_dotenv()
HANDLE = os.environ.get("BLUESKY_HANDLE")
PASSWORD = os.environ.get("BLUESKY_PASSWORD")
URL = os.environ.get("BLUESKY_URL")

# Sacar y mostrar los datos
client = Client(base_url=URL)
client.login(HANDLE, PASSWORD)
profile = client.app.bsky.actor.get_profile({"actor": client.me.did})
print("Usuario:", profile.display_name)
print("Bio actual:", profile.description)