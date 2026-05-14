# =============================================================================
# views.py – Logik der Anwendung (was passiert bei welcher Anfrage?)
# =============================================================================
# Eine „View" ist eine Python-Funktion, die eine HTTP-Anfrage entgegennimmt
# und eine HTTP-Antwort zurückgibt. Django leitet jede URL an die passende
# View weiter (definiert in urls.py).
#
# Zwei Arten von Antworten werden hier verwendet:
#   - render()       → gibt eine HTML-Seite zurück (für den Browser)
#   - JsonResponse() → gibt JSON-Daten zurück (für JavaScript im Browser)
# =============================================================================

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required  # Schützt Views vor nicht-angemeldeten Nutzern
from django.contrib.auth.forms import UserCreationForm     # Djangos eingebautes Registrierungsformular
from django.contrib.auth import login                      # Meldet einen Nutzer programmatisch an
from .models import ShoppingItem, ShoppingList, CalendarEvent, Note


# -----------------------------------------------------------------------------
# register – Registrierung eines neuen Benutzers
# -----------------------------------------------------------------------------
def register(request):
    # Ist der Benutzer bereits eingeloggt, wird er direkt zur App weitergeleitet.
    if request.user.is_authenticated:
        return redirect('/mylist/')

    if request.method == 'POST':
        # Das Formular wird mit den eingesendeten Daten befüllt.
        form = UserCreationForm(request.POST)

        if form.is_valid():
            # Benutzer wird in der Datenbank gespeichert.
            user = form.save()

            # Zwei Standardlisten werden automatisch für den neuen Benutzer erstellt.
            ShoppingList.objects.create(name='Besorgungen', user=user)
            ShoppingList.objects.create(name='Erledigungen', user=user)

            # Benutzer wird sofort eingeloggt (keine erneute Anmeldung nötig).
            login(request, user)
            return redirect('/mylist/')
    else:
        # Bei einem normalen Seitenaufruf (GET) wird ein leeres Formular erstellt.
        form = UserCreationForm()

    # Das Registrierungs-Template wird mit dem Formular gerendert.
    return render(request, 'register.html', {'form': form})


# -----------------------------------------------------------------------------
# mylist – Hauptseite: zeigt alle Listen des eingeloggten Benutzers
# -----------------------------------------------------------------------------
# @login_required leitet nicht-eingeloggte Benutzer automatisch zur Login-Seite um.
@login_required
def mylist(request):
    if request.method == 'POST':
        # Ein neuer Eintrag soll hinzugefügt werden.
        # list_id gibt an, zu welcher Liste der Eintrag gehört.
        list_id = request.POST.get('list_id')

        # get_object_or_404: Sucht die Liste in der Datenbank.
        # Falls sie nicht existiert oder einem anderen Benutzer gehört → Fehler 404.
        shopping_list = get_object_or_404(ShoppingList, id=list_id, user=request.user)

        # Neuer Eintrag wird in der Datenbank angelegt.
        ShoppingItem.objects.create(name=request.POST['itemName'], shopping_list=shopping_list)

    # Alle Listen des eingeloggten Benutzers werden geladen.
    # prefetch_related('items') lädt gleichzeitig alle Einträge jeder Liste –
    # das spart Datenbankabfragen (statt N+1 nur 2 Abfragen).
    all_lists = ShoppingList.objects.prefetch_related('items').filter(user=request.user)

    # Das Template wird gerendert und die Listen werden übergeben.
    return render(request, 'shoppinglist.html', {'all_lists': all_lists})


# -----------------------------------------------------------------------------
# toggle_item – Eintrag abhaken oder wieder aufheben
# -----------------------------------------------------------------------------
@login_required
def toggle_item(request, item_id):
    if request.method == 'POST':
        # Eintrag wird gesucht – nur wenn er dem eingeloggten Benutzer gehört.
        # shopping_list__user ist ein „Lookup über eine Beziehung":
        # Prüft, ob die Liste des Eintrags dem aktuellen Benutzer gehört.
        item = get_object_or_404(ShoppingItem, id=item_id, shopping_list__user=request.user)

        # done wird umgekehrt: True → False, False → True.
        item.done = not item.done
        item.save()

        # Gibt den neuen Zustand als JSON zurück, damit JavaScript reagieren kann.
        return JsonResponse({'success': True, 'done': item.done})

    # Nur POST-Anfragen sind erlaubt. Status 405 = „Methode nicht erlaubt".
    return JsonResponse({'success': False}, status=405)


# -----------------------------------------------------------------------------
# delete_item – einen Eintrag löschen
# -----------------------------------------------------------------------------
@login_required
def delete_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(ShoppingItem, id=item_id, shopping_list__user=request.user)
        item.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=405)


# -----------------------------------------------------------------------------
# edit_item – einen Eintrag umbenennen
# -----------------------------------------------------------------------------
@login_required
def edit_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(ShoppingItem, id=item_id, shopping_list__user=request.user)

        # strip() entfernt überflüssige Leerzeichen am Anfang und Ende.
        new_name = request.POST.get('newName', '').strip()

        if new_name:
            item.name = new_name
            item.save()
            return JsonResponse({'success': True})

    # Status 400 = „Ungültige Anfrage" (z. B. leerer Name).
    return JsonResponse({'success': False}, status=400)


# -----------------------------------------------------------------------------
# create_list – eine neue Liste erstellen
# -----------------------------------------------------------------------------
@login_required
def create_list(request):
    if request.method == 'POST':
        name = request.POST.get('listName', '').strip()
        if name:
            # Die neue Liste wird dem eingeloggten Benutzer zugeordnet.
            ShoppingList.objects.create(name=name, user=request.user)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


# -----------------------------------------------------------------------------
# events – Kalendertermine abrufen oder hinzufügen
# -----------------------------------------------------------------------------
@login_required
def events(request):
    if request.method == 'POST':
        # Neuen Termin anlegen.
        date_str = request.POST.get('date', '').strip()
        title = request.POST.get('title', '').strip()

        if date_str and title:
            CalendarEvent.objects.create(date=date_str, title=title, user=request.user)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False}, status=400)

    # GET-Anfrage: Alle Termine des Benutzers als JSON zurückgeben.
    # .values() gibt nur die angegebenen Felder zurück (kein komplettes Objekt).
    all_events = list(CalendarEvent.objects.filter(user=request.user).values('id', 'date', 'title'))

    # Das Datum wird in einen String umgewandelt, damit JSON es korrekt überträgt.
    for e in all_events:
        e['date'] = str(e['date'])

    return JsonResponse({'events': all_events})


# -----------------------------------------------------------------------------
# delete_event – einen Kalendertermin löschen
# -----------------------------------------------------------------------------
@login_required
def delete_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(CalendarEvent, id=event_id, user=request.user)
        event.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=405)


# -----------------------------------------------------------------------------
# notes – Notizen abrufen oder hinzufügen
# -----------------------------------------------------------------------------
@login_required
def notes(request):
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            note = Note.objects.create(text=text, user=request.user)
            # Die ID der neuen Notiz wird zurückgegeben, damit JavaScript
            # die Notiz direkt ohne Seitenneuladen anzeigen kann.
            return JsonResponse({'success': True, 'id': note.id})
        return JsonResponse({'success': False}, status=400)

    # GET-Anfrage: Alle Notizen des Benutzers als JSON zurückgeben.
    all_notes = list(Note.objects.filter(user=request.user).values('id', 'text'))
    return JsonResponse({'notes': all_notes})


# -----------------------------------------------------------------------------
# delete_note – eine Notiz löschen
# -----------------------------------------------------------------------------
@login_required
def delete_note(request, note_id):
    if request.method == 'POST':
        note = get_object_or_404(Note, id=note_id, user=request.user)
        note.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=405)
