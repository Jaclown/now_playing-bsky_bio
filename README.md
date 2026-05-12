# Bluesky Now Playing Bot (Linux + MPRIS)

Bot sencillo para actualizar automáticamente la bio de Bluesky con la música que esté sonando en tiempo real usando MPRIS en Linux. Funciona con reproductores como Cider, Spotify, MPV, VLC, Chromium, Firefox, etc.

# IMPORTANTE

Se recomienda usar un entorno virtual (`venv`) para evitar conflictos con paquetes del sistema. Este proyecto necesita `python-dbus`, que en Manjaro/Arch (donde se ha creado) se instala con pacman porque depende de librerías del sistema.

sudo pacman -S python-dbus

python -m venv venv --system-site-packages

source venv/bin/activate

pip install -r requirements.txt

configurar .env (ver tercer punto: configuración de bluesky)

python run.py

# CONFIGURACIÓN DEL REPRODUCTOR

La función get_now_playing() es la que decide qué reproductor se escucha. Por defecto está pensado para Cider (Apple Music) y MPV. Para ver qué reproductores tienes disponibles en tu sistema ejecuta:

python mpris.py

Te devolverá algo tipo org.mpris.MediaPlayer2.spotify o org.mpris.MediaPlayer2.chromium.instanceXXXX. Ese identificador es el que tienes que usar dentro del código para filtrar el reproductor correcto.

# CONFIGURACIÓN DE BLUESKY

Crea un archivo .env en la carpeta raíz (esta misma) y añade tus credenciales:

BLUESKY_HANDLE=usuario.bsky.social

BLUESKY_PASSWORD=tu_password

BLUESKY_URL=https://bsky.social (o https://eurosky.social si es lo que usas)

# PERSONALIZACIÓN DE LA BIO

En run.py puedes cambiar cómo se muestra la canción. Por defecto es:

prefix_bio = "la descripción que quieras previo al Now Playing"

bio = f"🎵 {title} — {artist}"

Pero puedes poner lo que quieras, por ejemplo:

bio = f"Escuchando: {artist} - {title}"

o cualquier formato que prefieras.

# FUNCIONAMIENTO

El script se conecta a DBus, detecta el reproductor activo vía MPRIS, obtiene la canción actual, y actualiza la bio de Bluesky cada 10 segundos. Si no hay música, muestra un estado inactivo.

# PARAR EL BOT

CTRL + C
