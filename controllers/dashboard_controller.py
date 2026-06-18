"""Controllerschicht der Anwendung."""

import datetime

from dtos.student_dto import StudentDTO
from services.studium_service import StudiumService


class DashboardController:
    """Verteilt Anfragen der View an die Geschäftslogik (Service)."""

    def __init__(self, service: StudiumService):
        self._service = service

    def lade_profil(self) -> StudentDTO | None:
        """Leitet die Anfrage zum Laden des Profils weiter."""
        return self._service.lade_student()

    def erstelle_profil(self, student_name: str, matrikelnummer: int) -> StudentDTO:
        """Leitet die Anfrage zur Profilerstellung weiter."""
        return self._service.erstelle_student(student_name, matrikelnummer)

    def studiengang_einschreiben(self, studiengang_name: str, regelstudienzeit_monate: int, gesamt_ects_studiengang: int, startdatum: datetime.date) -> StudentDTO:
        """Leitet die Anfrage zur Einschreibung weiter."""
        return self._service.schreibe_ein(studiengang_name, regelstudienzeit_monate, gesamt_ects_studiengang, startdatum)

    def studiengang_exmatrikulieren(self) -> StudentDTO:
        """Leitet die Anfrage zur Exmatrikulation weiter."""
        return self._service.exmatrikulieren()

    def modul_hinzufuegen(self, modulcode: str, modul_name: str, ects: int, pruefungsart_eingabe: str) -> StudentDTO:
        """Leitet die Anfrage zum Hinzufügen eines Moduls weiter."""
        return self._service.fuege_modul_hinzu(modulcode, modul_name, ects, pruefungsart_eingabe)

    def modul_loeschen(self, modul_name: str) -> StudentDTO:
        """Leitet die Anfrage zum Löschen eines Moduls weiter."""
        return self._service.loesche_modul(modul_name)

    def leistung_hinzufuegen(self, modul_name: str, note: float, pruefungsdatum: datetime.date, versuch: int) -> StudentDTO:
        """Leitet die Anfrage zum Hinzufügen einer Prüfungsleistung weiter."""
        return self._service.fuege_leistung_hinzu(modul_name, note, pruefungsdatum, versuch)

    def leistung_loeschen(self, modul_name: str, versuch: int) -> StudentDTO:
        """Leitet die Anfrage zum Löschen einer Prüfungsleistung weiter."""
        return self._service.loesche_leistung(modul_name, versuch)