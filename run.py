import re
import time
import os
import dbus
from dotenv import load_dotenv
from atproto import Client

# Cargar los datos del .env que contiene nuestras credenciales, por seguridad. Y almacenarlas como variables para usarlas
load_dotenv()

HANDLE = os.environ.get("BLUESKY_HANDLE")
PASSWORD = os.environ.get("BLUESKY_PASSWORD")
URL = os.environ.get("BLUESKY_URL")

# Leer lo que estamos escuchando en este momento en mpris
def get_now_playing(bus):
    names = bus.list_names()
    players = []

    for n in names:
        if re.match(r"org\.mpris\.MediaPlayer2\.", str(n)):
            players.append(str(n))

    cider = None

    for player in players:
        if "chromium" in player:
            cider = player
            break

    if cider is None:
        return None

    obj = bus.get_object(cider, "/org/mpris/MediaPlayer2")
    props = dbus.Interface(obj, "org.freedesktop.DBus.Properties")

    status = str(props.Get("org.mpris.MediaPlayer2.Player", "PlaybackStatus"))

    if status != "Playing":
        return None

    metadata = props.Get("org.mpris.MediaPlayer2.Player", "Metadata")

    artist_list = metadata.get("xesam:artist", [])
    artist = ", ".join(str(a) for a in artist_list)
    title = str(metadata.get("xesam:title", ""))

    if title:
        return artist, title

    return None

# Definir la función para que, recibiendo datos del usuario (client) y la nueva bio, vaya actualizando el perfil sin romper el avatar ni el banner
def update_bio(client, bio):
    current = client.com.atproto.repo.get_record({
        "repo": client.me.did,
        "collection": "app.bsky.actor.profile",
        "rkey": "self",
    })

    record = current.value.model_dump(by_alias=True)

    record["description"] = bio

    client.com.atproto.repo.put_record({
        "repo": client.me.did,
        "collection": "app.bsky.actor.profile",
        "rkey": "self",
        "record": record,
    })


# Inicializar
bus = dbus.SessionBus()

client = Client(base_url=URL)
client.login(HANDLE, PASSWORD)

last_bio = None

# Poner lo que precede al Now Playing
prefix_bio = "Antes tenía una bio muy cortita así que me pongo esta que es más larga\n\n"

# Iterar para cambiar según lo que estemos escuchando y que el Now Playing vaya acorde a cada cosa que lea mpris (por defecto cada 10 secs)
while True:
    now = get_now_playing(bus)

    if now:
        artist, title = now
        bio = f"{prefix_bio}🎵 Now Playing: {artist} — {title}"
    else:
        bio = f"{prefix_bio}🎵 No estoy escuchando nada"

    if bio != last_bio:
        update_bio(client, bio)
        print("Bio actualizada:", bio)
        last_bio = bio

    time.sleep(10)