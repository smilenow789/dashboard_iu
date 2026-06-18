"""Enum-Definition für Prüfungsarten."""

from enum import Enum


class Pruefungsart(Enum):
    """Definiert alle zugelassenen Prüfungsarten als Enum."""
    KLAUSUR = "Klausur"
    MUENDLICHE_PRUEFUNG = "Mündliche Prüfung"
    FORSCHUNGSARBEIT = "Forschungsarbeit"
    SEMINARARBEIT = "Seminararbeit"
    HAUSARBEIT = "Hausarbeit"
    REFERAT = "Referat"
    PROJEKTBERICHT = "Projektbericht"
    PRAESENTATION = "Präsentation"
    ONLINE_PRAESENTATION = "Online Präsentation"
    ENTWURF = "Entwurf"
    FALLSTUDIE = "Fallstudie"
    PROJEKTARBEIT = "Projektarbeit"
    PRAXISREFLEXION = "Praxisreflexion"
    ALTERNATIVE_PRUEFUNGSLEISTUNGEN = "Alternative Prüfungsleistungen"
    SCHRIFTLICHE_AUSARBEITUNG = "Schriftliche Ausarbeitung"
    ANWENDUNGSORIENTIERTE_PRUEFUNGSLEISTUNG = "Anwendungsorientierte Prüfungsleistung"