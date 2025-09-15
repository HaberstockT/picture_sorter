# Projektdokumentation
## 1. Überblick

Dieses Projekt implementiert eine **robuste, eventbasierte Pipeline** zum automatischen Verarbeiten, Sortieren und Verschieben von Bilddateien auf einem Server.

Ziele:
- Automatisches Erkennen neuer Dateien in einem Eingangsordner.
- Sichere Verarbeitung ohne Datenverlust (keine Datei wird gelöscht).
- Sortieren nach **Dateityp (Erweiterung)** und **Erstelldatum (inkl. Uhrzeit, ms)**.
- **Duplicate-Erkennung** mittels Hashing + Index.
- Automatisches Umbenennen bei Namenskonflikten.
- Sicherstellen, dass kein paralleler Konflikt mit einem Backup-Skript entsteht (Lock-Datei). 
- Möglichkeit den Prozess **manuell** zu starten, auch wenn der Watcher nicht läuft.

## 2. Projektstruktur
Die Pfade sind so definiert, dass sie auch auf **Windows-Systemen** funktionierten (via Pathlib).

- bildpipeline
    - bildpipeline
        - watcher.py
        - processor.py
        - duplicate_index.py
        - utils.py
        - config.py
    - tests
        - test_processor.py
        - test_index.py
        - ...
    - data
        - incoming
        - processed
        - duplicates
        - index.dp
    - scripts
        - run_watcher.py
        - run_manual.py
    - pyproject.toml
    - README.md

## 3. Anforderungen

### 3.1 Python 
Version 3.10+

### 3.2 Dependencies
Use UV to manage dependencies
- watchdog
- pillow
- python-dateutils

## 4. Funktionsweise
### 4.1 Watcher
- Über watchdog wird der incoming/-Ordner überwacht
- Nuee Dateien lösen Event aus.
- Dateienn werden erst nach einer Stabilisierungszeit verarbeitet (Größe ändert sich nicht mehr)

### 4.2 Verarbeitung
- Datei wird eingelesen -> Metadaten bestimmt (Erstelldatum, Extension)
- Neuer Zielname wird generiert
- Falls Name schon vorhanden, *_1, *_2, ...

### 4.3 Dublicate-Handling
- SHA-256 Hash wird berechnet.
- Hash wird in SQLite-Index gespeichert (mit Datum + Extension)
- Duplicate = gleicher Hash + gleiche Extension + gleiches Erstelldatum
- datein landet in duplicates statt processed

### 4.4 Lockfile
Vor Start prüft das Skript ob eine Lockdatei process.lock existiert
Wenn ja, beendet sich das Skript -> Verhindert Konflikte mit Backup-Prozessen.
Beim Start -> Lockdatei wird erstellt Beim Ende -> Lockdatei wird gelöscht

### 4.5 Manueller Start
mit Script/run_manual.py können alle Dateien aus incoming verarbeitet werden, auch ohne Watcher

Nützlich für Recovery-Fälle

## 5. Betrieb
### 5.1 Setup
git clone < Repo-url >
cd bildpipeline
uv sync

### 5.2 Start Watcher
uv run python scripts/run_watcher.py

### 5.3 Start Manual
uv run python scripts/run_manual.py

## 6. Test
Unit-Tests in tests
uv run pytest

## 7. Risiken und Absicherungen
- **Dateiverlust** -> Keine Datei wird gelöscht, nur verschoben
- **Parallelzugriffe** -> Lockfile schützt gegen Konflikte mit Backup-Skripts
- **Performance** -> Hashing ist teuer, wird aber nur 1x pro Datei gemacht und ergebnis im Index gespeicher
- **Windows/Linux** -> Pfade unabhängig mit pathlib implementiert.