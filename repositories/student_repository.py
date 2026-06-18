"""Datenzugriffsschicht (Persistenz)."""

import os
import pickle
from abc import ABC, abstractmethod

from models.student import Student


class StudentRepository(ABC):
    """Abstrakte Basisklasse für den Datenzugriff."""

    @abstractmethod
    def save(self, student: Student) -> None:
        """Speichert das übergebene Studenten-Objekt."""
        pass

    @abstractmethod
    def load(self) -> Student | None:
        """Lädt das gespeicherte Studenten-Objekt oder gibt None zurück."""
        pass

    @abstractmethod
    def delete_all(self) -> None:
        """Löscht alle persistierten Daten."""
        pass


class PickleStudentRepository(StudentRepository):
    """Konkrete Implementierung des Repositories basierend auf Pickle-Datei."""

    def __init__(self, dateiname: str = "cmd_dashboard_daten.pickle"):
        self._dateiname = dateiname

    def save(self, student: Student) -> None:
        """Serialisiert das Objekt und speichert es in einer Binärdatei."""
        with open(self._dateiname, 'wb') as datei:
            pickle.dump(student, datei)

    def load(self) -> Student | None:
        """Lädt das deserialisierte Objekt aus der Binärdatei."""
        if not os.path.exists(self._dateiname):
            return None
        with open(self._dateiname, 'rb') as datei:
            return pickle.load(datei)

    def delete_all(self) -> None:
        """Löscht die Pickle-Datei vom Dateisystem."""
        if os.path.exists(self._dateiname):
            os.remove(self._dateiname)