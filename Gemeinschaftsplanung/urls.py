# =============================================================================
# urls.py – URL-Konfiguration der Anwendung
# =============================================================================
# Diese Datei verbindet URLs (Webadressen) mit den zugehörigen Views (Funktionen).
# Wenn ein Benutzer eine URL aufruft, sucht Django hier nach einem passenden
# Eintrag und führt die verknüpfte View-Funktion aus.
#
# Aufbau eines Eintrags:
#   path('url/', view_funktion)
#
# <int:item_id> ist ein Platzhalter: Django liest die Zahl aus der URL heraus
# und übergibt sie als Parameter an die View-Funktion.
# Beispiel: /mylist/delete/7/ → delete_item(request, item_id=7)
# =============================================================================

from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView              # Einfache Weiterleitung ohne eigene View
from django.contrib.auth.views import LoginView, LogoutView  # Djangos eingebaute Login/Logout-Views
from mylist.views import (
    mylist, delete_item, edit_item, toggle_item,
    create_list, events, delete_event,
    notes, delete_note, register
)

urlpatterns = [

    # Startseite → leitet direkt zur Login-Seite weiter.
    path('', RedirectView.as_view(url='/login/')),

    # Django-Adminbereich (für Entwickler, unter /admin/).
    path('admin/', admin.site.urls),

    # Anmelden: Djangos eingebaute LoginView verwendet das Template login.html.
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),

    # Abmelden: Nach dem Logout wird der Benutzer zur Login-Seite weitergeleitet.
    # Wichtig: Logout funktioniert nur per POST-Anfrage (Sicherheit in Django 5+).
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),

    # Registrierung: Eigene View, die neue Benutzerkonten anlegt.
    path('register/', register, name='register'),

    # Hauptseite der App: zeigt alle Listen des eingeloggten Benutzers.
    # Nimmt auch POST-Anfragen an (neuen Eintrag hinzufügen).
    path('mylist/', mylist),

    # Einen Listeneintrag löschen. Die ID des Eintrags steht in der URL.
    path('mylist/delete/<int:item_id>/', delete_item),

    # Einen Listeneintrag umbenennen.
    path('mylist/edit/<int:item_id>/', edit_item),

    # Einen Listeneintrag abhaken / Haken entfernen.
    path('mylist/toggle/<int:item_id>/', toggle_item),

    # Eine neue Liste erstellen.
    path('mylist/create-list/', create_list),

    # Kalendertermine abrufen (GET) oder hinzufügen (POST).
    path('mylist/events/', events),

    # Einen Kalendertermin löschen.
    path('mylist/events/delete/<int:event_id>/', delete_event),

    # Notizen abrufen (GET) oder hinzufügen (POST).
    path('mylist/notes/', notes),

    # Eine Notiz löschen.
    path('mylist/notes/delete/<int:note_id>/', delete_note),
]
