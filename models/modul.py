"""Model-Definition für Studienmodule."""

from models.pruefungsart import Pruefungsart
from models.pruefungsleistung import Pruefungsleistung


class Modul:
    """Repräsentiert ein Studienmodul, das Prüfungsleistungen enthält."""

    def __init__(self, modulcode: str, modul_name: str, ects: int, pruefungsart: Pruefungsart):
        self._modulcode = modulcode
        self._modul_name = modul_name
        self._ects = ects
        self.pruefungsart = pruefungsart
        self.pruefungsleistungen: list[Pruefungsleistung] = []

    @property
    def modulcode(self) -> str:
        """Gibt den Modulcode zurück."""
        return self._modulcode

    @property
    def modul_name(self) -> str:
        """Gibt den ausgeschriebenen Modulnamen zurück."""
        return self._modul_name

    @property
    def ects(self) -> int:
        """Gibt die ECTS-Punkte des Moduls zurück."""
        return self._ects

    def add_pruefungsleistung(self, pruefungsleistung: Pruefungsleistung) -> None:
        """Fügt eine Prüfungsleistung hinzu. ValueError ab mehr als 3 Versuchen."""
        if len(self.pruefungsleistungen) >= 3:
            raise ValueError("Maximal 3 Versuche pro Modul erlaubt.")
        self.pruefungsleistungen.append(pruefungsleistung)

    def remove_pruefungsleistung(self, versuch: int) -> bool:
        """Löscht eine bestimmte Prüfungsleistung anhand des Versuchs."""
        for leistung in self.pruefungsleistungen:
            if leistung.versuch == versuch:
                self.pruefungsleistungen.remove(leistung)
                return True
        return False