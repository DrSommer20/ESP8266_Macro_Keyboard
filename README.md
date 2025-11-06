# ESP8266_Macro_Keyboard

(Generiert mit Copilot)
Dieses Projekt verwandelt einen einfachen ESP8266-basierten Macro-Controller in eine serielle Makrotastatur. Der ESP8266 sendet bei Tastendrücken einfache Serialevents, und ein Python-Listener empfängt diese Events und simuliert lokale Tastendrücke oder tippt Text.

Kurzüberblick
- Der ESP8266 (NodeMCU / Amica) liest 7 Buttons und sendet über die serielle Schnittstelle Events im Format:
  - `DOWN <LABEL>`
  - `UP <LABEL>`
  Diese Events werden vom Sketch in [Arduino.ino](Arduino.ino) erzeugt (siehe Funktion [`sendEvent`](Arduino.ino)).

- Das Python-Skript [serial_macro_listener.py](serial_macro_listener.py) öffnet den seriellen Port, parst die Events und führt die zugeordneten Aktionen aus:
  - Text tippen oder
  - Tastenkombinationen drücken / loslassen
  (Implementierung in [`simulate_keypress`](serial_macro_listener.py) und Hauptschleife in [`run_listener`](serial_macro_listener.py)).

Serielle Schnittstelle / Protokoll
- Format: ASCII-Text mit Zeilen, z. B. `DOWN F13` oder `UP F13`.
- Labels: `F13` ... `F19` (konfiguriert in [Arduino.ino](Arduino.ino)).

Tasten-Zuordnung
- Die Standardzuordnung ist in [serial_macro_listener.py](serial_macro_listener.py) definiert (Konstante `KEY_MAPPING`).
- Mapping-Einträge können Zeichenketten (für Text) oder Listen mit `pynput`-Keys/Zeichen (für Kombinationen) sein.

Installation & Voraussetzungen
- ESP8266: Mit der Arduino-IDE oder PlatformIO den Sketch [Arduino.ino](Arduino.ino) auf den NodeMCU flashen.
- Host-Rechner: Python 3
  - Abhängigkeiten installieren:
    ```sh
    pip install pyserial pynput
    ```
- In [serial_macro_listener.py](serial_macro_listener.py) den seriellen Port anpassen (Variable `COM_PORT`) und das Script starten:
  ```sh
  python serial_macro_listener.py
  ```

Sicherheit & Berechtigungen
- Auf manchen OS (z. B. macOS) benötigt `pynput` Zugriff auf Eingabehilfen bzw. Accessibility-Permissions.
- Das Script emuliert Tastatureingaben — Vorsicht beim Testen (Terminal-Fokus, Passwörter etc.).

Fehlerbehandlung
- Das Python-Skript versucht, die serielle Verbindung neu zu verbinden, falls diese getrennt wird.
- Unbekannte Labels werden geloggt (Warnung).

Dateien
- [Arduino.ino](Arduino.ino) — ESP8266 Sketch, erzeugt serielle Events (`sendEvent`).
- [serial_macro_listener.py](serial_macro_listener.py) — Python Listener, mappt Events zu Tasteneingaben (`simulate_keypress`, `run_listener`).

}
