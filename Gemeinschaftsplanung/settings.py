# =============================================================================
# settings.py – Konfiguration des Django-Projekts
# =============================================================================
# Diese Datei steuert das gesamte Verhalten des Django-Projekts:
# Datenbank, Sicherheit, installierte Apps, Templates und mehr.
#
# Umgebungsvariablen (os.environ.get):
#   Sensible Werte wie Passwörter oder API-Schlüssel werden nicht direkt
#   in den Code geschrieben, sondern als Umgebungsvariablen gespeichert.
#   Lokal steht der Fallback-Wert im zweiten Argument, auf Railway werden
#   die echten Werte im Dashboard eingetragen.
# =============================================================================

import os
import dj_database_url  # Hilfsbibliothek: wandelt eine Datenbank-URL in Django-Format um
from pathlib import Path

# Absoluter Pfad zum Stammverzeichnis des Projekts.
# Wird verwendet, um andere Pfade relativ dazu zu bilden.
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------------------------------------------
# Sicherheit
# -----------------------------------------------------------------------------

# Geheimer Schlüssel – wird für Verschlüsselung und Signaturen verwendet.
# Im Produktivbetrieb muss er geheim bleiben und als Umgebungsvariable gesetzt sein.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-%xo7)9tr9!d2j2h)g097s#*8fv^lh79i-0ea%y**_k=ro$(hz(')

# Debug-Modus: Im Entwicklungsbetrieb True (zeigt detaillierte Fehler).
# Im Produktivbetrieb muss dieser Wert False sein.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Liste der erlaubten Domains, unter denen die App erreichbar ist.
# Anfragen von anderen Domains werden abgelehnt (Sicherheitsmaßnahme).
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost,192.168.178.50').split(',')

# Railway setzt die Variable RAILWAY_PUBLIC_DOMAIN automatisch.
# Die Railway-Domain wird zur Liste der erlaubten Hosts hinzugefügt.
# CSRF_TRUSTED_ORIGINS erlaubt POST-Anfragen von dieser HTTPS-Domain –
# ohne diesen Eintrag würde Django alle Formulare auf der Live-Seite blockieren.
if os.environ.get('RAILWAY_PUBLIC_DOMAIN'):
    ALLOWED_HOSTS.append(os.environ.get('RAILWAY_PUBLIC_DOMAIN'))
    CSRF_TRUSTED_ORIGINS = [f"https://{os.environ.get('RAILWAY_PUBLIC_DOMAIN')}"]

# -----------------------------------------------------------------------------
# Installierte Apps
# -----------------------------------------------------------------------------
# Django ist modular aufgebaut. Jede App hier bringt eigene Funktionen mit.
INSTALLED_APPS = [
    'django.contrib.admin',        # Automatischer Adminbereich unter /admin/
    'django.contrib.auth',         # Benutzerverwaltung (Login, Passwörter, Gruppen)
    'django.contrib.contenttypes', # Internes Django-System für generische Beziehungen
    'django.contrib.sessions',     # Sitzungsverwaltung (speichert Login-Status)
    'django.contrib.messages',     # Einmalige Nachrichten (z. B. „Erfolgreich gespeichert")
    'django.contrib.staticfiles',  # Verwaltet statische Dateien (CSS, JS, Bilder)
    'mylist'                       # Unsere eigene App mit Listen, Kalender und Notizen
]

# -----------------------------------------------------------------------------
# Middleware
# -----------------------------------------------------------------------------
# Middleware sind Schichten, die jede Anfrage und Antwort durchläuft –
# ähnlich wie Filter in einer Pipeline.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',          # Sicherheits-Header (HTTPS etc.)
    'whitenoise.middleware.WhiteNoiseMiddleware',             # Liefert statische Dateien direkt aus (ohne Webserver)
    'django.contrib.sessions.middleware.SessionMiddleware',   # Verwaltet Benutzersitzungen
    'django.middleware.common.CommonMiddleware',              # URL-Normalisierung (z. B. Trailing Slash)
    'django.middleware.csrf.CsrfViewMiddleware',              # Schutz vor CSRF-Angriffen (gefälschte Formulare)
    'django.contrib.auth.middleware.AuthenticationMiddleware',# Liest den eingeloggten Benutzer aus der Sitzung
    'django.contrib.messages.middleware.MessageMiddleware',   # Verarbeitet einmalige Nachrichten
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Schutz vor Clickjacking-Angriffen
]

# Wo Django die URL-Konfiguration findet.
ROOT_URLCONF = 'Gemeinschaftsplanung.urls'

# -----------------------------------------------------------------------------
# Templates
# -----------------------------------------------------------------------------
# Django sucht HTML-Dateien automatisch in den „templates"-Ordnern aller
# installierten Apps (APP_DIRS: True).
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],       # Zusätzliche Ordner für Templates (hier keine)
        'APP_DIRS': True, # Sucht automatisch in mylist/templates/
        'OPTIONS': {
            'context_processors': [
                # Stellen Variablen in jedem Template bereit:
                'django.template.context_processors.request', # request-Objekt
                'django.contrib.auth.context_processors.auth', # eingeloggter Benutzer
                'django.contrib.messages.context_processors.messages', # Nachrichten
            ],
        },
    },
]

# Wo Djangos WSGI-Server (Gunicorn) die App findet.
WSGI_APPLICATION = 'Gemeinschaftsplanung.wsgi.application'

# -----------------------------------------------------------------------------
# Datenbank
# -----------------------------------------------------------------------------
# Auf Railway ist die Umgebungsvariable DATABASE_URL gesetzt (PostgreSQL).
# Lokal wird SQLite verwendet – eine einfache Datei-Datenbank ohne Server.
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # dj_database_url.parse() wandelt die URL in das Django-Datenbankformat um.
    # conn_max_age=600: Datenbankverbindungen bleiben 10 Minuten offen (Performance).
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',  # Die Datenbankdatei liegt im Projektordner
        }
    }

# -----------------------------------------------------------------------------
# Passwortregeln
# -----------------------------------------------------------------------------
# Django prüft neue Passwörter automatisch gegen diese Regeln.
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},  # Nicht ähnlich wie der Benutzername
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},             # Mindestens 8 Zeichen
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},            # Keine häufigen Passwörter (z. B. „password")
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},           # Nicht nur Zahlen
]

# -----------------------------------------------------------------------------
# Sprache und Zeitzone
# -----------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True   # Internationalisierung aktiviert
USE_TZ = True     # Zeitzonen-Unterstützung aktiviert

# -----------------------------------------------------------------------------
# Weiterleitungen für Login/Logout
# -----------------------------------------------------------------------------
LOGIN_URL = '/login/'            # Nicht-eingeloggte Benutzer werden hierhin umgeleitet
LOGIN_REDIRECT_URL = '/mylist/'  # Nach erfolgreichem Login geht es hierhin
LOGOUT_REDIRECT_URL = '/login/'  # Nach dem Logout geht es hierhin

# -----------------------------------------------------------------------------
# Statische Dateien (CSS, JavaScript, Bilder)
# -----------------------------------------------------------------------------
STATIC_URL = 'static/'                          # URL-Präfix für statische Dateien
STATIC_ROOT = BASE_DIR / 'staticfiles'          # Ordner, in den Django alle statischen Dateien sammelt
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# WhiteNoise liefert statische Dateien direkt aus Python heraus (kein separater Webserver nötig)
# und komprimiert sie automatisch für schnellere Ladezeiten.
