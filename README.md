# Installationsanleitung

**GitHub-Repository:** [https://github.com/smilenow789/dashboard_iu](https://github.com/smilenow789/dashboard_iu)

## Voraussetzungen
* **Windows 11**
* **Python** (getestet mit Version 3.14.3)
* **Internetverbindung** zum Herunterladen des Projekts

## Projekt herunterladen & vorbereiten

1. **Repository über das Terminal klonen:**
   ```bash
   git clone https://github.com/smilenow789/dashboard_iu.git
   ```
   (Alternativ: Auf GitHub unter "Code" die ZIP-Datei herunterladen und entpacken).

2. **Im Terminal in den Projektordner wechseln:**
   ```bash
   cd dashboard_iu
   ```

3. **Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt
   ```

## Anwendung starten
- Im Terminal die Anwendung starten:
  ```bash
  python main.py
  ```

## Hinweise
- Die Anwendung speichert alle Fortschritte lokal in der Datei `cmd_dashboard_daten.pickle`. Diese wird im selben Ordner automatisch erzeugt.
- Nach dem Start überprüft das System automatisch, ob bereits lokale Daten vorhanden sind. Falls kein Profil existiert, wird die Erstellung eines neuen Studierendenprofils gestartet.
