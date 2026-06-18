"""Geschäftslogik-Schicht der Anwendung."""

import datetime

from dtos.student_dto import StudentDTO, StudiengangDTO, ModulDTO, PruefungsleistungDTO
from models.modul import Modul
from models.pruefungsart import Pruefungsart
from models.pruefungsleistung import Pruefungsleistung
from models.student import Student
from models.studiengang import Studiengang
from repositories.student_repository import StudentRepository


class StudiumService:
    """Kapselt die Geschäftslogik für die Verwaltung von Studenten, Studiengängen und Noten."""

    def __init__(self, repository: StudentRepository):
        self._repository = repository

    def lade_student(self) -> StudentDTO | None:
        """Lädt das gespeicherte Studentenprofil und gibt es als DTO zurück."""
        student = self._repository.load()
        if student:
            return self._map_to_dto(student)
        return None

    def erstelle_student(self, student_name: str, matrikelnummer: int) -> StudentDTO:
        """Erstellt ein neues Profil, löscht dabei alte Daten und speichert."""
        self._repository.delete_all()
        neuer_student = Student(student_name=student_name, matrikelnummer=matrikelnummer)
        self._repository.save(neuer_student)
        return self._map_to_dto(neuer_student)

    def schreibe_ein(self, studiengang_name: str, regelstudienzeit_monate: int, gesamt_ects_studiengang: int, startdatum: datetime.date) -> StudentDTO:
        """Schreibt den Studenten in einen neuen Studiengang ein."""
        student = self._lade_fachobjekt()
        neuer_studiengang = Studiengang(studiengang_name, regelstudienzeit_monate, gesamt_ects_studiengang, startdatum)
        student.einschreiben(neuer_studiengang)
        self._repository.save(student)
        return self._map_to_dto(student)

    def exmatrikulieren(self) -> StudentDTO:
        """Exmatrikuliert den Studenten vom aktuellen Studiengang."""
        student = self._lade_fachobjekt()
        student.exmatrikulieren()
        self._repository.save(student)
        return self._map_to_dto(student)

    def fuege_modul_hinzu(self, modulcode: str, modul_name: str, ects: int, pruefungsart_eingabe: str) -> StudentDTO:
        """Fügt dem Studiengang ein neues Modul hinzu. Wirft ValueError bei ungültiger Prüfungsart."""
        student = self._lade_fachobjekt()
        if not student.studiengang:
            raise ValueError("Student ist in keinen Studiengang eingeschrieben.")

        gewaehlte_art = next((art for art in Pruefungsart if art.value.lower() == pruefungsart_eingabe.lower()), None)
        if not gewaehlte_art:
            raise ValueError(f"Ungültige Prüfungsart: {pruefungsart_eingabe}")

        neues_modul = Modul(modulcode, modul_name, ects, gewaehlte_art)
        student.studiengang.add_modul(neues_modul)
        self._repository.save(student)
        return self._map_to_dto(student)

    def loesche_modul(self, modul_name: str) -> StudentDTO:
        """Entfernt ein Modul. Wirft ValueError, wenn es nicht existiert."""
        student = self._lade_fachobjekt()
        if not student.studiengang or not student.studiengang.remove_modul(modul_name):
            raise ValueError(f"Modul '{modul_name}' nicht gefunden.")
        self._repository.save(student)
        return self._map_to_dto(student)

    def fuege_leistung_hinzu(self, modul_name: str, note: float, pruefungsdatum: datetime.date, versuch: int) -> StudentDTO:
        """Trägt eine neue Note für einen Prüfungsversuch in ein bestehendes Modul ein."""
        student = self._lade_fachobjekt()
        modul = self._finde_modul(student, modul_name)
        neue_leistung = Pruefungsleistung(note, pruefungsdatum, versuch)
        modul.add_pruefungsleistung(neue_leistung)
        self._repository.save(student)
        return self._map_to_dto(student)

    def loesche_leistung(self, modul_name: str, versuch: int) -> StudentDTO:
        """Entfernt eine Prüfungsleistung anhand des Versuchs."""
        student = self._lade_fachobjekt()
        modul = self._finde_modul(student, modul_name)
        if not modul.remove_pruefungsleistung(versuch):
            raise ValueError(f"Leistung für Versuch {versuch} nicht gefunden.")
        self._repository.save(student)
        return self._map_to_dto(student)

    def _lade_fachobjekt(self) -> Student:
        """Lädt das interne Student-Objekt aus dem Repository oder wirft einen Fehler."""
        student = self._repository.load()
        if student is None:
            raise ValueError("Kein aktives Profil gefunden.")
        return student

    def _finde_modul(self, student: Student, modul_name: str) -> Modul:
        """Sucht ein Modul anhand des Namens im aktuellen Studiengang."""
        if student.studiengang is None:
            raise ValueError("Nicht eingeschrieben.")
        for modul in student.studiengang.module:
            if modul.modul_name.lower() == modul_name.lower():
                return modul
        raise ValueError(f"Modul '{modul_name}' nicht gefunden.")

    def _map_to_dto(self, student: Student) -> StudentDTO:
        """Wandelt das interne Student-Fachobjekt in ein rein lesbares DTO für die View um."""
        studiengang_dto = None
        if student.studiengang:
            module_dtos = []
            for modul in student.studiengang.module:
                leistung_dtos = [
                    PruefungsleistungDTO(
                        leistung.note,
                        leistung.versuch,
                        leistung.is_bestanden(),
                        leistung.pruefungsdatum
                    )
                    for leistung in modul.pruefungsleistungen
                ]
                module_dtos.append(ModulDTO(modul.modulcode, modul.modul_name, modul.ects, modul.pruefungsart.value, leistung_dtos))

            studiengang_dto = StudiengangDTO(
                studiengang_name=student.studiengang.studiengang_name,
                regelstudienzeit_monate=student.studiengang.regelstudienzeit_monate,
                gesamt_ects_studiengang=student.studiengang.gesamt_ects_studiengang,
                startdatum=student.studiengang.startdatum,
                module=module_dtos
            )

        return StudentDTO(
            student_name=student.student_name,
            matrikelnummer=student.matrikelnummer,
            fortschritt_prozent=student.get_fortschritt_prozent(),
            total_ects=student.get_total_erreichte_ects(),
            notendurchschnitt=student.berechne_notendurchschnitt(),
            studiengang=studiengang_dto
        )
