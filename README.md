# KanbanX – Dein schlankes CLI-Kanban-Board

![KanbanX Logo](https://via.placeholder.com/150x50?text=KanbanX) <!-- Placeholder-Bild, kann später ersetzt werden -->

## Inhaltsverzeichnis
1.  [Einführung](#1-einführung)
2.  [Warum KanbanX?](#2-warum-kanbanx)
3.  [Installation](#3-installation)
4.  [Grundlegende Nutzung](#4-grundlegende-nutzung)
5.  [Befehlsreferenz](#5-befehlsreferenz)
    *   [`add` – Aufgabe hinzufügen](#add--aufgabe-hinzufügen)
    *   [`move` – Aufgabe verschieben](#move--aufgabe-verschieben)
    *   [`sub` – Unteraufgabe hinzufügen](#sub--unteraufgabe-hinzufügen)
    *   [`done` – Unteraufgabe als erledigt markieren](#done--unteraufgabe-als-erledigt-markieren)
    *   [`note` – Notiz hinzufügen/aktualisieren](#note--notiz-hinzufügenaktualisieren)
    *   [`clip` – Snippet hinzufügen](#clip--snippet-hinzufügen)
    *   [`list` – Board anzeigen](#list--board-anzeigen)
6.  [Datenhaltung](#6-datenhaltung)
7.  [Fehlerbehebung & Häufige Fragen (FAQ)](#7-fehlerbehebung--häufige-fragen-faq)
8.  [Beitrag leisten](#8-beitrag-leisten)
9.  [Lizenz](#9-lizenz)

---

## 1. Einführung

**KanbanX** ist ein minimalistisches, Kommandozeilen-basiertes Tool zur persönlichen Aufgabenverwaltung. Es kombiniert die Einfachheit eines Kanban-Boards mit erweiterten Funktionen für Unteraufgaben, Notizen und einen integrierten "Clipboard"-Bereich. Entwickelt als einzelne Python-Datei, kommt es ohne externe Abhängigkeiten aus und ist sowohl unter Windows als auch unter Unix-ähnlichen Systemen lauffähig. Alle Daten werden lokal in einer JSON-Datei im selben Verzeichnis wie das Skript gespeichert, was es extrem portabel und einfach zu handhaben macht.

## 2. Warum KanbanX?

*   **Zero-Dependency:** Keine Installation zusätzlicher Bibliotheken erforderlich. Einfach herunterladen und loslegen!
*   **Portabel:** Da alle Daten lokal in einer `kanbanx.json`-Datei gespeichert werden, kannst du das Skript und deine Aufgabenliste problemlos zwischen verschiedenen Systemen verschieben.
*   **CLI-basiert:** Ideal für Entwickler und Benutzer, die eine schnelle, effiziente und tastaturzentrierte Aufgabenverwaltung bevorzugen.
*   **Übersichtlich:** Organisiert Aufgaben in den klassischen Kanban-Spalten "Todo", "Doing" und "Done" für einen klaren Überblick über deinen Workflow.
*   **Erweiterte Funktionen:** Verwalte detaillierte Unteraufgaben, füge Notizen hinzu und speichere wichtige Text-Snippets oder Referenzen direkt bei deinen Aufgaben.

## 3. Installation

KanbanX benötigt lediglich eine installierte **Python 3**-Umgebung.

1.  **Herunterladen:** Lade die Datei `kanbanx.py` in ein Verzeichnis deiner Wahl herunter.
    *   Du kannst sie direkt von der Quelle kopieren oder mit `curl` herunterladen, falls verfügbar.
    ```bash
    # Beispiel: Herunterladen in dein aktuelles Verzeichnis
    # curl -O https://raw.githubusercontent.com/dein_repo/kanbanx.py
    ```
2.  **Ausführen:** Öffne ein Terminal oder eine Kommandozeile, navigiere in das Verzeichnis, in dem sich `kanbanx.py` befindet, und führe das Skript aus.
    ```bash
    cd /pfad/zu/deinem/kanbanx-ordner
    python kanbanx.py list
    ```
    Beim ersten Start wird automatisch eine Datei namens `kanbanx.json` im selben Verzeichnis wie das Skript erstellt. Diese Datei speichert alle deine Aufgaben und Daten.

## 4. Grundlegende Nutzung

Alle Befehle werden nach dem Muster `python kanbanx.py <befehl> [argumente]` ausgeführt.

*   **`--plain` Option:** Du kannst jedem Befehl, der Ausgaben erzeugt (insbesondere `list`), die Option `--plain` hinzufügen, um die Farbausgabe zu deaktivieren. Dies ist nützlich, wenn dein Terminal keine ANSI-Farbcodes unterstützt oder du eine reine Textausgabe bevorzugst.
    ```bash
    python kanbanx.py list --plain
    ```

## 5. Befehlsreferenz

### `add` – Aufgabe hinzufügen

Fügt eine neue Aufgabe zu einer der Kanban-Spalten hinzu.

*   **Syntax:** `python kanbanx.py add <spalte> "<titel>" ["<notiz>"]`
    *   `<spalte>`: Die Kanban-Spalte, zu der die Aufgabe hinzugefügt werden soll. Wähle aus: `todo`, `doing`, `done`.
    *   `"<titel>"`: Der Titel deiner Aufgabe. **Muss in Anführungszeichen stehen**, wenn er Leerzeichen enthält.
    *   `"<notiz>"` (optional): Eine anfängliche Notiz für die Aufgabe. **Muss in Anführungszeichen stehen**, wenn sie Leerzeichen enthält.

*   **Beispiele:**
    ```bash
    # Eine einfache Aufgabe ohne Notiz
    python kanbanx.py add todo "Neue Funktion implementieren"

    # Eine Aufgabe mit Titel und Notiz
    python kanbanx.py add doing "Meeting mit Team A" "Besprechung der nächsten Schritte und Ergebnisse"

    # Eine Aufgabe direkt als erledigt markieren
    python kanbanx.py add done "Altes Projekt abgeschlossen"
    ```
*   **Ausgabe:** Nach dem Hinzufügen erhältst du eine eindeutige ID für die Aufgabe (z.B. `ID-abc123`). Diese ID benötigst du für alle weiteren Operationen mit dieser Aufgabe.
    ```
    ✅ 'Neue Funktion implementieren' → todo (ID-e6e6d5)
    ```

### `move` – Aufgabe verschieben

Verschiebt eine Aufgabe von einer Spalte in eine andere.

*   **Syntax:** `python kanbanx.py move <aufgaben-id> <zielspalte>`
    *   `<aufgaben-id>`: Die ID der Aufgabe, die du verschieben möchtest (z.B. `ID-e6e6d5`).
    *   `<zielspalte>`: Die Ziel-Kanban-Spalte. Wähle aus: `todo`, `doing`, `done`.

*   **Beispiele:**
    ```bash
    # Verschiebt die Aufgabe in die "Doing"-Spalte
    python kanbanx.py move ID-e6e6d5 doing

    # Verschiebt die Aufgabe in die "Done"-Spalte
    python kanbanx.py move ID-e6e6d5 done
    ```
*   **Ausgabe:**
    ```
    📦 ID-e6e6d5 → doing
    ```

### `sub` – Unteraufgabe hinzufügen

Fügt einer bestehenden Aufgabe eine Unteraufgabe hinzu.

*   **Syntax:** `python kanbanx.py sub <aufgaben-id> "<text>"`
    *   `<aufgaben-id>`: Die ID der Hauptaufgabe.
    *   `"<text>"`: Die Beschreibung der Unteraufgabe. **Muss in Anführungszeichen stehen**, wenn sie Leerzeichen enthält.

*   **Beispiele:**
    ```bash
    # Unteraufgabe zu einer bestehenden Aufgabe hinzufügen
    python kanbanx.py sub ID-e6e6d5 "Datenbankmodell entwerfen"

    # Eine weitere Unteraufgabe
    python kanbanx.py sub ID-e6e6d5 "API-Endpunkte definieren"
    ```
*   **Ausgabe:** Nach dem Hinzufügen erhältst du eine eindeutige ID für die Unteraufgabe.
    ```
    ➕ Subtask ID-c7b972 zu ID-e6e6d5
    ```

### `done` – Unteraufgabe als erledigt markieren

Markiert eine Unteraufgabe als erledigt.

*   **Syntax:** `python kanbanx.py done <aufgaben-id> <unteraufgaben-id>`
    *   `<aufgaben-id>`: Die ID der Hauptaufgabe.
    *   `<unteraufgaben-id>`: Die ID der Unteraufgabe, die als erledigt markiert werden soll.

*   **Beispiel:**
    ```bash
    python kanbanx.py done ID-e6e6d5 ID-c7b972
    ```
*   **Ausgabe:**
    ```
    ✅ ID-c7b972 erledigt
    ```

### `note` – Notiz hinzufügen/aktualisieren

Fügt einer Aufgabe eine Notiz hinzu oder hängt Text an eine bestehende Notiz an.

*   **Syntax:** `python kanbanx.py note <aufgaben-id> "<text>"`
    *   `<aufgaben-id>`: Die ID der Aufgabe.
    *   `"<text>"`: Der Text, der zur Notiz hinzugefügt werden soll. **Muss in Anführungszeichen stehen**, wenn er Leerzeichen enthält.

*   **Beispiele:**
    ```bash
    # Eine neue Notiz hinzufügen
    python kanbanx.py note ID-e6e6d5 "Wichtige Erkenntnisse aus dem Meeting: Fokus auf Performance."

    # Weiteren Text an die bestehende Notiz anhängen
    python kanbanx.py note ID-e6e6d5 "Weitere Details: Siehe Dokumentation X."
    ```
*   **Ausgabe:**
    ```
    📝 Notiz zu ID-e6e6d5 gespeichert
    ```

### `clip` – Snippet hinzufügen

Speichert ein Text-Snippet oder eine Referenz bei einer Aufgabe. Dies ist nützlich, um schnell Code-Snippets, URLs oder andere relevante Informationen zu speichern.

*   **Syntax:** `python kanbanx.py clip <aufgaben-id> "<snippet>"`
    *   `<aufgaben-id>`: Die ID der Aufgabe.
    *   `"<snippet>"`: Der Text des Snippets. **Muss in Anführungszeichen stehen**, wenn er Leerzeichen enthält.

*   **Beispiele:**
    ```bash
    # Ein Code-Snippet speichern
    python kanbanx.py clip ID-e6e6d5 "pip install requests"

    # Einen Link speichern
    python kanbanx.py clip ID-e6e6d5 "Link zur API-Doku: https://example.com/api"
    ```
*   **Ausgabe:**
    ```
    📎 Clip zu ID-e6e6d5 gespeichert
    ```
*   **Hinweis:** Beim Auflisten der Aufgabe werden die letzten drei Clips angezeigt.

### `list` – Board anzeigen

Zeigt den aktuellen Zustand deines Kanban-Boards an, einschließlich aller Aufgaben, Notizen, Unteraufgaben und Clips.

*   **Syntax:** `python kanbanx.py list [--plain]`
    *   `--plain` (optional): Deaktiviert die Farbausgabe. Nützlich, wenn dein Terminal keine ANSI-Farbcodes unterstützt oder du eine reine Textausgabe bevorzugst.

*   **Beispiel:**
    ```bash
    python kanbanx.py list
    ```
*   **Beispiel-Ausgabe:**
    ```
    TODO
      ID-aaeec3  Dokumentation für KanbanX schreiben
          NOTE  "Heute noch erledigen"
            ○ ID-db6e83  "Gemini's aufgaben"
            ○ ID-bd4f83  "Meine Aufgaben"
          CLIP  "D:\Second-Brain\04_Archive\kanbanx\kanbanx_user_manual.md"

    DOING
      ID-b22e74  Testaufgabe mit Leerzeichen
          NOTE  "Dies ist eine Notiz für die Testaufgabe""Zusätzliche Notiz nach der Korrektur"
            ✓ ID-eae573  "Erste Unteraufgabe für die neue Aufgabe"
          CLIP  "Ein Test-Clip nach der Korrektur"

    DONE
    ```

## 6. Datenhaltung

Alle deine Aufgaben und deren Details werden in der Datei `kanbanx.json` gespeichert. Diese Datei befindet sich im **selben Verzeichnis wie das Skript `kanbanx.py`**.

*   **Sicherung:** Es wird dringend empfohlen, diese Datei regelmäßig zu sichern.
*   **Manuelle Bearbeitung:** Du kannst diese Datei bei Bedarf manuell bearbeiten, aber sei vorsichtig! Eine fehlerhafte JSON-Struktur kann dazu führen, dass das Skript nicht mehr funktioniert. Es wird nur empfohlen, wenn du mit JSON-Strukturen vertraut bist.

## 7. Fehlerbehebung & Häufige Fragen (FAQ)

**F: Mein Titel wird nicht korrekt angezeigt, wenn er Leerzeichen enthält!**
**A:** Stelle sicher, dass du den Titel **immer in Anführungszeichen** setzt, wenn er Leerzeichen enthält. Beispiel: `python kanbanx.py add todo "Mein neuer Titel"`. Das Skript wurde angepasst, um dies korrekt zu verarbeiten.

**F: Ich erhalte einen `IndentationError` oder andere Python-Fehler nach dem Bearbeiten des Skripts.**
**A:** Dies deutet auf einen Fehler in der Python-Syntax oder der Einrückung hin. Stelle sicher, dass du einen geeigneten Texteditor verwendest, der Python-Einrückungen korrekt handhabt (normalerweise 4 Leerzeichen pro Ebene). Wenn du das Skript manuell bearbeitet hast, überprüfe die Einrückungen sorgfältig.

**F: Die Farben werden in meinem Terminal nicht angezeigt.**
**A:** Dein Terminal unterstützt möglicherweise keine ANSI-Farbcodes. Verwende die Option `--plain` mit dem `list`-Befehl, um die Farbausgabe zu deaktivieren: `python kanbanx.py list --plain`.

## 8. Beitrag leisten

KanbanX ist ein Open-Source-Projekt. Beiträge sind willkommen! Wenn du Ideen für neue Funktionen, Verbesserungen oder Fehlerbehebungen hast, kannst du:
*   Ein Issue auf GitHub erstellen (falls das Projekt dort gehostet wird).
*   Einen Pull Request mit deinen Änderungen einreichen.

## 9. Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe die `LICENSE`-Datei für weitere Details.
