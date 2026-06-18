"""Model-Definition für den Studenten."""

from models.studiengang import Studiengang


class Student:
    """Repräsentiert den Studenten."""

    def __init__(self, student_name: str, matrikelnummer: int):
        self._student_name = student_name
        self._matrikelnummer = matrikelnummer
        self.studiengang: Studiengang | None = None

    @property
    def student_name(self) -> str:
        """Gibt den Namen des Studenten zurück."""
        return self._student_name

    @property
    def matrikelnummer(self) -> int:
        """Gibt die Matrikelnummer zurück."""
        return self._matrikelnummer

    def einschreiben(self, studiengang: Studiengang) -> bool:
        """Schreibt den Studenten in einen Studiengang ein, falls er nicht schon eingeschrieben ist."""
        if self.studiengang is None:
            self.studiengang = studiengang
            return True
        raise ValueError("Bereits in einem Studiengang eingeschrieben.")

    def exmatrikulieren(self) -> None:
        """Löscht die Zuordnung zum aktuellen Studiengang."""
        self.studiengang = None

    def get_total_erreichte_ects(self) -> int:
        """Summiert die ECTS aller Module mit einer bestandenen Prüfungsleistung."""
        if not self.studiengang: return 0
        total_ects = 0
        for modul in self.studiengang.module:
            if any(leistung.is_bestanden() for leistung in modul.pruefungsleistungen):
                total_ects += modul.ects
        return total_ects

    def get_fortschritt_prozent(self) -> float:
        """Berechnet den prozentualen Anteil der erreichten ECTS an den Gesamt-ECTS."""
        if not self.studiengang or self.studiengang.gesamt_ects_studiengang == 0:
            return 0.0
        return (self.get_total_erreichte_ects() / self.studiengang.gesamt_ects_studiengang) * 100

    def berechne_notendurchschnitt(self) -> float:
        """Berechnet den nach ECTS gewichteten Notendurchschnitt aller bestandenen Module."""
        if not self.studiengang: return 0.0
        summe_gewichtet = 0.0
        summe_ects = 0
        for modul in self.studiengang.module:
            bestandene_leistung = next((leistung for leistung in modul.pruefungsleistungen if leistung.is_bestanden()),
                                       None)
            if bestandene_leistung:
                summe_gewichtet += bestandene_leistung.note * modul.ects
                summe_ects += modul.ects
        if summe_ects == 0: return 0.0
        return round(summe_gewichtet / summe_ects, 2)