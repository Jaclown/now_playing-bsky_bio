import re
import dbus

# Leer todos las fuentes de mpris activas
bus = dbus.SessionBus()

names = bus.list_names()
players = []

for n in names:
    if re.match(r"org\.mpris\.MediaPlayer2\.", str(n)):
        players.append(str(n))

print ("Reproductores encontrados:", players)

# Filtrar para coger solo Cider/APM
cider = None

for player in players:
    if "chromium" in player:
        cider = player
        break

if cider is None:
    print("Cider no está reproduciendo")
else:
    print("Cider reproduciendo:", cider)
    # Sacar los datos que muestra Cider, manejando los metadatos que expone mpris. La ruta es siempre la misma, donde expone todo lo que detecta
    obj = bus.get_object(cider, "/org/mpris/MediaPlayer2")
    props = dbus.Interface(obj, "org.freedesktop.DBus.Properties")
    # Pillar los datos que nos interesan, el estado de reproducción (pause, playing...) y el artista, o artistas si son varios, iterando la lista con un bucle
    status = props.Get("org.mpris.MediaPlayer2.Player", "PlaybackStatus")
    metadata = props.Get("org.mpris.MediaPlayer2.Player", "Metadata")
    song = metadata.get("xesam:title", [])
    artist_list = metadata.get("xesam:artist", [])
    artist = ", ".join(str(a) for a in artist_list)
    # Mostrar los datos
    print("Estado:", status)
    print("Canción:", song)
    print("Artista:", artist)


