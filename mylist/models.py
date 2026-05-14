# =============================================================================
# models.py – Datenbankstruktur der Anwendung
# =============================================================================
# In Django beschreibt jedes „Model" eine Tabelle in der Datenbank.
# Jede Klasse entspricht einer Tabelle, jedes Attribut einer Spalte.
# Django erstellt und verwaltet diese Tabellen automatisch über Migrationen.
# =============================================================================

from django.db import models
from django.contrib.auth.models import User  # Djangos eingebautes Benutzermodell
from datetime import date


# -----------------------------------------------------------------------------
# ShoppingList – eine einzelne Liste (z. B. „Besorgungen")
# -----------------------------------------------------------------------------
class ShoppingList(models.Model):

    # Jede Liste gehört zu einem bestimmten Benutzer.
    # ForeignKey bedeutet: „Viele Listen können zu einem Benutzer gehören."
    # on_delete=CASCADE: Wird der Benutzer gelöscht, werden auch seine Listen gelöscht.
    # null=True, blank=True: Das Feld darf leer sein (für ältere Datensätze ohne Benutzer).
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lists', null=True, blank=True)

    # Der Name der Liste, z. B. „Besorgungen". Maximal 200 Zeichen.
    name = models.CharField(max_length=200)

    # Erstellungsdatum – wird automatisch auf das heutige Datum gesetzt.
    created_at = models.DateField(default=date.today)

    # Bestimmt, wie ein Objekt als Text dargestellt wird (z. B. im Admin-Bereich).
    def __str__(self):
        return self.name


# -----------------------------------------------------------------------------
# ShoppingItem – ein einzelner Eintrag innerhalb einer Liste
# -----------------------------------------------------------------------------
class ShoppingItem(models.Model):

    # Jeder Eintrag gehört zu einer Liste.
    # related_name='items' erlaubt es, über liste.items.all() alle Einträge zu laden.
    # null=True, blank=True: Einträge ohne Liste sind erlaubt (für Altdaten).
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name='items', null=True, blank=True)

    # Erstellungsdatum des Eintrags.
    created_at = models.DateField(default=date.today)

    # Der Text des Eintrags, z. B. „Milch kaufen".
    name = models.CharField(max_length=200)

    # Ob der Eintrag abgehakt ist. Standard: False (nicht erledigt).
    done = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + ' ' + self.name


# -----------------------------------------------------------------------------
# CalendarEvent – ein Termin im Kalender
# -----------------------------------------------------------------------------
class CalendarEvent(models.Model):

    # Jeder Termin gehört zu einem Benutzer.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events', null=True, blank=True)

    # Das Datum des Termins (nur Tag, kein Uhrzeit).
    date = models.DateField()

    # Die Bezeichnung des Termins, z. B. „Zahnarzt".
    title = models.CharField(max_length=200)

    class Meta:
        # Termine werden standardmäßig nach Datum und dann nach ID sortiert.
        ordering = ['date', 'id']

    def __str__(self):
        return f"{self.date}: {self.title}"


# -----------------------------------------------------------------------------
# Note – eine Notiz
# -----------------------------------------------------------------------------
class Note(models.Model):

    # Jede Notiz gehört zu einem Benutzer.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes', null=True, blank=True)

    # Der Inhalt der Notiz. TextField erlaubt beliebig langen Text.
    text = models.TextField()

    # Zeitstempel der Erstellung – wird automatisch gesetzt und nie geändert.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Neueste Notizen zuerst (Minuszeichen = absteigende Reihenfolge).
        ordering = ['-created_at']

    def __str__(self):
        # Zeigt nur die ersten 50 Zeichen der Notiz als Vorschau.
        return self.text[:50]
