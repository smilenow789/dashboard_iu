"""Data Transfer Objects für den sicheren Datenaustausch zwischen Schichten."""

import datetime
from dataclasses import dataclass, field


@dataclass
class PruefungsleistungDTO:
    """DTO für Prüfungsleistungen."""
    note: float
    versuch: int
    bestanden: bool
    pruefungsdatum: datetime.date


@dataclass
class ModulDTO:
    """DTO für Module und deren Leistungen."""
    modulcode: str
    modul_name: str
    ects: int
    pruefungsart: str
    leistungen: list[PruefungsleistungDTO] = field(default_factory=list)


@dataclass
class StudiengangDTO:
    """DTO für den Studiengang und dessen Module."""
    studiengang_name: str
    regelstudienzeit_monate: int
    gesamt_ects_studiengang: int
    startdatum: datetime.date
    module: list[ModulDTO] = field(default_factory=list)


@dataclass
class StudentDTO:
    """Haupt-DTO zur Repräsentation des Studentenprofils."""
    student_name: str
    matrikelnummer: int
    fortschritt_prozent: float
    total_ects: int
    notendurchschnitt: float
    studiengang: StudiengangDTO | None = None