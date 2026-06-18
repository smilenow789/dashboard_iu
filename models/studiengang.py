"""Model-Definition für den Studiengang."""

import datetime

from models.modul import Modul


class Studiengang:
    """Repräsentiert einen Studiengang mit zugehörigen Modulen."""

    def __init__(self, studiengang_name: str, regelstudienzeit_monate: int, gesamt_ects_studiengang: int, startdatum: datetime.date):
        self._studiengang_name = studiengang_name
        self._regelstudienzeit_monate = regelstudienzeit_monate
        self._gesamt_ects_studiengang = gesamt_ects_studiengang
        self._startdatum = startdatum
        self.module: list[Modul] = []

    @property
    def studiengang_name(self) -> str:
        """Gibt den Namen des Studiengangs zurück."""
        return self._studiengang_name

    @property
    def regelstudienzeit_monate(self) -> int:
        """Gibt die Regelstudienzeit in Monaten zurück."""
        return self._regelstudienzeit_monate

    @property
    def gesamt_ects_studiengang(self) -> int:
        """Gibt die zu erreichenden Gesamt-ECTS zurück."""
        return self._gesamt_ects_studiengang

    @property
    def startdatum(self) -> datetime.date:
        """Gibt das Startdatum des Studiums zurück."""
        return self._startdatum

    def add_modul(self, modul: Modul) -> None:
        """Fügt dem Studiengang ein neues Modul hinzu, sofern der Code nicht existiert."""
        for bestehendes_modul in self.module:
            if bestehendes_modul.modulcode.lower() == modul.modulcode.lower():
                raise ValueError(f"Modul mit Code {modul.modulcode} existiert bereits.")
        self.module.append(modul)

    def remove_modul(self, modul_name: str) -> bool:
        """Entfernt ein Modul anhand des Namens und gibt True bei Erfolg zurück."""
        for modul in self.module:
            if modul.modul_name.lower() == modul_name.lower():
                self.module.remove(modul)
                return True
        return False
