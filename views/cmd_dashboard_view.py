"""Präsentationsschicht für die Darstellung in der Kommandozeile."""

from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt

from controllers.dashboard_controller import DashboardController
from dtos.student_dto import StudentDTO
from models.pruefungsart import Pruefungsart


class CmdDashboardView:
    """Kapselt die gesamte Terminal-Ausgabe und nimmt Eingaben entgegen."""

    def __init__(self, controller: DashboardController):
        self._controller = controller
        self._console = Console()

    def start_routine(self) -> None:
        """Startet die App und prüft, ob bereits ein lokales Profil existiert."""
        self._console.print("[dim]Überprüfe lokale Daten...[/dim]")
        student_dto = self._controller.lade_profil()

        if student_dto is None:
            self._console.print("[yellow]Keine lokalen Daten gefunden.[/yellow]")
            self.neues_profil_erstellen()
        else:
            self._console.print(f"[green]Willkommen zurück, {student_dto.student_name}.[/green]")
            self.zeige_dashboard(student_dto)

    def neues_profil_erstellen(self) -> None:
        """Führt durch den Dialog zur Erstellung eines neuen Studentenprofils."""
        self._console.print("\n[bold cyan]--- Neues Profil anlegen ---[/bold cyan]")
        student_name = Prompt.ask("Bitte gib deinen [green]Namen[/green] ein")
        matrikelnummer = IntPrompt.ask("Bitte gib deine [green]Matrikelnummer[/green] ein")

        try:
            student_dto = self._controller.erstelle_profil(student_name, matrikelnummer)
            self._console.print(f"\n[bold green]Profil für {student_name} erstellt![/bold green]")
            student_dto = self.einschreiben(student_dto)
            self.zeige_dashboard(student_dto)
        except Exception as e:
            self._console.print(f"\n[bold red]Fehler:[/bold red] [yellow]{e}[/yellow]")

    def einschreiben(self, student_dto: StudentDTO) -> StudentDTO:
        """Sammelt die Daten für die Einschreibung in einen Studiengang."""
        if student_dto.studiengang is not None:
            self._console.print("[yellow]Du bist bereits eingeschrieben.[/yellow]")
            Prompt.ask("\n[dim]Drücke Enter um fortzufahren[/dim]")
            return student_dto

        studiengang_name = Prompt.ask("Bitte gib den [green]Studiengangnamen[/green] ein")
        regelstudienzeit_monate = IntPrompt.ask("Regelstudienzeit in [green]Monaten[/green]")
        gesamt_ects_studiengang = IntPrompt.ask("[green]Gesamt-ECTS[/green] des Studiengangs")

        while True:
            datum_str = Prompt.ask("Startdatum [green](TT.MM.JJJJ)[/green]")
            try:
                startdatum = datetime.strptime(datum_str, "%d.%m.%Y").date()
                break
            except ValueError:
                self._console.print("[red]Ungültiges Format![/red]")

        try:
            neues_dto = self._controller.studiengang_einschreiben(studiengang_name, regelstudienzeit_monate,
                                                                  gesamt_ects_studiengang, startdatum)
            self._console.print(f"\n[bold green]Eingeschrieben in {studiengang_name}![/bold green]")
            Prompt.ask("\n[dim]Drücke Enter um fortzufahren[/dim]")
            return neues_dto
        except Exception as e:
            self._console.print(f"[bold red]Fehler:[/bold red] {e}")
            Prompt.ask("\n[dim]Drücke Enter um fortzufahren[/dim]")
            return student_dto

    def neues_modul_erfassen(self, student_dto: StudentDTO) -> StudentDTO:
        """Dialog zur Erfassung eines neuen Moduls im Studiengang."""
        if not student_dto.studiengang: return student_dto

        self._console.print("\n[bold cyan]--- Neues Modul erfassen ---[/bold cyan]")
        modulcode = Prompt.ask("[green]Modulcode[/green] (z.B. DLBDE)")
        modul_name = Prompt.ask("[green]Modulname[/green]")
        ects = IntPrompt.ask("[green]ECTS-Punkte[/green]")

        moegliche_pruefungsarten = [art.value for art in Pruefungsart]
        gewaehlte_pruefungsart = Prompt.ask("[green]Prüfungsart[/green]", choices=moegliche_pruefungsarten, case_sensitive=False)

        try:
            return self._controller.modul_hinzufuegen(modulcode, modul_name, ects, gewaehlte_pruefungsart)
        except Exception as e:
            self._console.print(f"[bold red]Fehler:[/bold red] {e}")
            return student_dto

    def modul_loeschen_dialog(self, student_dto: StudentDTO) -> StudentDTO:
        """Dialog zum Auswählen und Löschen eines bestehenden Moduls."""
        if not student_dto.studiengang or not student_dto.studiengang.module:
            self._console.print("[yellow]Keine Module vorhanden.[/yellow]")
            Prompt.ask("\n[dim]Drücke Enter um fortzufahren[/dim]")
            return student_dto

        moegliche_module = [modul.modul_name for modul in student_dto.studiengang.module]
        for i, modul_name in enumerate(moegliche_module): self._console.print(f"[{i + 1}] {modul_name}")

        wahl_str = Prompt.ask("\nWähle ein Modul zum Löschen",
                              choices=[str(i + 1) for i in range(len(moegliche_module))])
        gewaehltes_modul_name = moegliche_module[int(wahl_str) - 1]

        bestaetigung = Prompt.ask(f"\n[red]'{gewaehltes_modul_name}' wirklich löschen? (j/n)[/red]", choices=["j", "n"])
        if bestaetigung == "j":
            try:
                return self._controller.modul_loeschen(gewaehltes_modul_name)
            except Exception as e:
                self._console.print(f"[bold red]Fehler:[/bold red] {e}")
        return student_dto

    def neue_pruefungsleistung_erfassen(self, student_dto: StudentDTO) -> StudentDTO:
        """Dialog zum Eintragen einer neuen Prüfungsleistung für ein Modul."""
        if not student_dto.studiengang or not student_dto.studiengang.module:
            self._console.print("[yellow]Füge zuerst ein Modul hinzu.[/yellow]")
            Prompt.ask("\n[dim]Drücke Enter um fortzufahren[/dim]")
            return student_dto

        moegliche_module = [modul.modul_name for modul in student_dto.studiengang.module]
        for i, modul_name in enumerate(moegliche_module): self._console.print(f"[{i + 1}] {modul_name}")
        wahl_str = Prompt.ask("\nWähle ein Modul", choices=[str(i + 1) for i in range(len(moegliche_module))])
        gewaehltes_modul_name = moegliche_module[int(wahl_str) - 1]

        while True:
            note_str = Prompt.ask("Note (z.B. 1.3)")
            try:
                note = float(note_str.replace(",", "."))
                break
            except ValueError:
                self._console.print("[red]Ungültige Zahl.[/red]")

        while True:
            datum_str = Prompt.ask("Datum [green](TT.MM.JJJJ)[/green]")
            try:
                pruefungsdatum = datetime.strptime(datum_str, "%d.%m.%Y").date()
                break
            except ValueError:
                self._console.print("[red]Ungültiges Format![/red]")

        versuch = IntPrompt.ask("Der wievielte Versuch war dies?")

        try:
            return self._controller.leistung_hinzufuegen(gewaehltes_modul_name, note, pruefungsdatum, versuch)
        except Exception as e:
            self._console.print(f"[bold red]Fehler:[/bold red] {e}")
            return student_dto

    def pruefungsleistung_loeschen_dialog(self, student_dto: StudentDTO) -> StudentDTO:
        """Dialog zum Löschen eines bestimmten Prüfungsversuchs."""
        if not student_dto.studiengang: return student_dto
        moegliche_module = [modul.modul_name for modul in student_dto.studiengang.module if modul.leistungen]
        if not moegliche_module:
            self._console.print("[yellow]Keine Leistungen erfasst.[/yellow]")
            Prompt.ask("\n[dim]Drücke Enter um fortzufahren[/dim]")
            return student_dto

        for i, modul_name in enumerate(moegliche_module): self._console.print(f"[{i + 1}] {modul_name}")
        wahl_str = Prompt.ask("Modul", choices=[str(i + 1) for i in range(len(moegliche_module))])
        gewaehltes_modul_name = moegliche_module[int(wahl_str) - 1]

        gewaehltes_modul_dto = next(
            modul for modul in student_dto.studiengang.module if modul.modul_name == gewaehltes_modul_name)
        versuche = [str(leistung.versuch) for leistung in gewaehltes_modul_dto.leistungen]
        versuch_wahl = Prompt.ask("Welcher Versuch?", choices=versuche)

        try:
            return self._controller.leistung_loeschen(gewaehltes_modul_name, int(versuch_wahl))
        except Exception as e:
            self._console.print(f"[bold red]Fehler:[/bold red] {e}")
            return student_dto

    def zeige_dashboard(self, student_dto: StudentDTO) -> None:
        """Zeigt das Hauptmenü und die Fortschrittsübersicht an."""
        while True:
            self._console.print(
                Panel(f"[bold white] DASHBOARD: ZIELÜBERWACHUNG [/bold white]", style="on blue"))

            if student_dto.studiengang:
                studiengang_daten = student_dto.studiengang
                ects = student_dto.total_ects
                gesamt_ects = studiengang_daten.gesamt_ects_studiengang
                regelstudienzeit = studiengang_daten.regelstudienzeit_monate
                fortschritt = student_dto.fortschritt_prozent
                note = student_dto.notendurchschnitt

                # Zeitberechnungen für Ziel 1
                heute = datetime.now().date()
                start = studiengang_daten.startdatum
                tage_verstrichen = (heute - start).days
                monate_verstrichen = max(0, tage_verstrichen / 30.4368)

                # Verhindert Division by Zero, falls Regelstudienzeit 0 ist
                if regelstudienzeit > 0:
                    erwartete_ects = min(
                        gesamt_ects,
                        monate_verstrichen * (gesamt_ects / regelstudienzeit)
                    )
                else:
                    erwartete_ects = 0.0

                if gesamt_ects > 0:
                    theoretisch_benoetigte_monate = (regelstudienzeit / gesamt_ects) * ects
                    differenz_monate = monate_verstrichen - theoretisch_benoetigte_monate
                else:
                    differenz_monate = 0.0

                # Ziel 1 Aufbereitung
                balken_laenge = 30
                gefuellt = int((fortschritt / 100) * balken_laenge)
                if differenz_monate > 0.5:
                    zeit_status = (f"[bold red]Im Rückstand:[/bold red] "
                                   f"Du hast ca. {differenz_monate:.1f} Monate Verspätung.\n"
                                   f"(Soll: {erwartete_ects:.1f} ECTS | Ist: {ects} ECTS)")
                    ladebalken = (f"[bold red]{'█' * gefuellt}[/bold red]"
                                  f"[dim]{'-' * (balken_laenge - gefuellt)}[/dim]")
                elif differenz_monate < -0.5:
                    zeit_status = (f"[bold green]Dem Plan voraus:[/bold green] "
                                   f"Du bist ca. {abs(differenz_monate):.1f} Monate voraus!\n"
                                   f"(Soll: {erwartete_ects:.1f} ECTS | Ist: {ects} ECTS)")
                    ladebalken = (f"[bold green]{'█' * gefuellt}[/bold green]"
                                  f"[dim]{'-' * (balken_laenge - gefuellt)}[/dim]")
                else:
                    zeit_status = (f"[bold yellow]Auf Kurs:[/bold yellow] "
                                   f"Du liegst im Plan!\n"
                                   f"(Soll: {erwartete_ects:.1f} ECTS | Ist: {ects} ECTS)")
                    ladebalken = (f"[bold yellow]{'█' * gefuellt}[/bold yellow]"
                                  f"[dim]{'-' * (balken_laenge - gefuellt)}[/dim]")

                jahre_regelstudienzeit = regelstudienzeit // 12
                ziel1_inhalt = (
                    f"[bold]Vorgabe:[/bold] {jahre_regelstudienzeit} Jahre Regelstudienzeit "
                    f"(ab {start.strftime('%d.%m.%Y')})\n"
                    f"[bold]Status:[/bold]  [{ladebalken}] {fortschritt:.1f}%\n"
                    f"[bold]ECTS:[/bold]    {ects} von {gesamt_ects} erreicht\n"
                    f"{'-' * 40}\n"
                    f"{zeit_status}"
                )

                # Ziel 2 Aufbereitung
                if ects > 0:
                    if note <= 2.0:
                        ziel2_status = "[bold green]Ziel erfüllt![/bold green]"
                        note_format = f"[bold green]{note:.2f}[/bold green]"
                    else:
                        ziel2_status = "[bold red]Ziel aktuell verfehlt.[/bold red]"
                        note_format = f"[bold red]{note:.2f}[/bold red]"
                else:
                    note_format = "-"
                    ziel2_status = "[dim]Noch keine Noten erfasst.[/dim]"

                ziel2_inhalt = (
                    f"[bold]Vorgabe:[/bold] <= 2.0\n"
                    f"[bold]Aktuell:[/bold] {note_format}\n"
                    f"[bold]Status:[/bold]  {ziel2_status}"
                )

                self._console.print(Panel(
                    ziel1_inhalt,
                    title="[bold cyan]ZIEL 1: STUDIENFORTSCHRITT & ZEITPLAN[/bold cyan]",
                    border_style="cyan"
                ))
                self._console.print(Panel(
                    ziel2_inhalt,
                    title="[bold cyan]ZIEL 2: NOTENDURCHSCHNITT[/bold cyan]",
                    border_style="cyan"
                ))
                print("\n")
            else:
                self._console.print(
                    Panel("[yellow]Nicht eingeschrieben.[/yellow]", title="[bold cyan]STATUS[/bold cyan]"))





            self._console.rule("[bold green]HAUPTMENÜ[/bold green]")
            self._console.print("[bold]1:[/bold] Einschreiben")
            self._console.print("[bold]2:[/bold] Exmatrikulieren")
            self._console.print("[bold]3:[/bold] Modul erfassen")
            self._console.print("[bold]4:[/bold] Modul löschen")
            self._console.print("[bold]5:[/bold] Leistung erfassen")
            self._console.print("[bold]6:[/bold] Leistung löschen")
            self._console.print("[bold]7:[/bold] Profil zurücksetzen")
            self._console.print("[bold]8:[/bold] Beenden")

            menue_auswahl = Prompt.ask("\nWähle eine Option", choices=["1", "2", "3", "4", "5", "6", "7", "8"])

            if menue_auswahl == "1":
                student_dto = self.einschreiben(student_dto)
            elif menue_auswahl == "2":
                student_dto = self._controller.studiengang_exmatrikulieren()
            elif menue_auswahl == "3":
                student_dto = self.neues_modul_erfassen(student_dto)
            elif menue_auswahl == "4":
                student_dto = self.modul_loeschen_dialog(student_dto)
            elif menue_auswahl == "5":
                student_dto = self.neue_pruefungsleistung_erfassen(student_dto)
            elif menue_auswahl == "6":
                student_dto = self.pruefungsleistung_loeschen_dialog(student_dto)
            elif menue_auswahl == "7":
                if Prompt.ask("[red]Alle Daten löschen? (j/n)[/red]", choices=["j", "n"]) == "j":
                    self.neues_profil_erstellen()
                    return
            elif menue_auswahl == "8":
                self._console.print("[yellow]Programm beendet.[/yellow]")
                break
