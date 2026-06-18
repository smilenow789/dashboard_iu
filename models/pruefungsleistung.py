"""Model-Definition für Prüfungsleistungen."""

import datetime


class Pruefungsleistung:
    """Kapselt eine erbrachte Prüfungsleistung inklusive Validierung nach APO."""

    def __init__(self, note: float, pruefungsdatum: datetime.date, versuch: int):
        self.note = note
        self._pruefungsdatum = pruefungsdatum
        self.versuch = versuch

    @property
    def note(self) -> float:
        """Gibt die erzielte Note zurück."""
        return self._note

    @note.setter
    def note(self, value: float) -> None:
        """Validiert und setzt die Note (muss zwischen 1.0 und 5.0 liegen)."""
        if not (1.0 <= value <= 5.0):
            raise ValueError("Die Note muss gemäss APO zwischen 1.0 und 5.0 liegen.")
        self._note = value

    @property
    def versuch(self) -> int:
        """Gibt den Prüfungsversuch zurück."""
        return self._versuch

    @versuch.setter
    def versuch(self, value: int) -> None:
        """Validiert und setzt den Versuch (maximal 3 gemäss APO)."""
        if value < 1 or value > 3:
            raise ValueError("Ungültiger Versuch. Gemäss APO sind maximal 3 Versuche zulässig.")
        self._versuch = value

    @property
    def pruefungsdatum(self) -> datetime.date:
        """Gibt das Datum der Prüfung zurück."""
        return self._pruefungsdatum

    def is_bestanden(self) -> bool:
        """Prüft, ob die Leistung mit 4.0 oder besser bestanden wurde."""
        return self._note <= 4.0