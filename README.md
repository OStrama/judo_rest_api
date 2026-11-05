# Judo REST API für Home Assistant

Lokale Home-Assistant-Integration für Judo-Wasseraufbereitung (Enthärter, Leckageschutz u. a.) über die REST-API des Judo Connectivity-Moduls (WLAN). Polling im Intervall, keine Cloud.

> Inoffizielle Integration, nicht mit Judo verbunden. Siehe [Haftungsausschluss](#haftungsausschluss).

Basiert auf [OStrama/judo_rest_api](https://github.com/OStrama/judo_rest_api). Dieser Fork enthält Stabilitätsfixes und eine Filterung der Kommandos nach Gerätetyp (siehe [Änderungen](#änderungen-gegenüber-dem-original)).

## Dokumentation der API

* Kommandoreferenz (Judo): <https://judo.eu/ftp-upload/download/REST-API/RESTAPI_Kommandos.pdf>
* Connectivity-Modul: <https://judo.eu/produkte/connectivity-modul-wlan/>

Die Integration folgt dieser Referenz. Welche Kommandos ein Gerät kennt, hängt vom Gerätetyp ab (Abruf `/api/rest/FF00`).

## Installation

### HACS (benutzerdefiniertes Repository)

1. HACS → Integrationen → ⋮ → *Benutzerdefinierte Repositories*
2. URL `https://github.com/AndyKausG/judo_rest_api`, Kategorie *Integration*
3. „Judo Rest API“ installieren, Home Assistant neu starten
4. Einstellungen → Geräte & Dienste → Integration hinzufügen → *Judo Wasseraufbereitung*

### Manuell

Inhalt von `custom_components/judo_rest_api/` nach `<config>/custom_components/judo_rest_api/` kopieren, Home Assistant neu starten.

Die Domain `judo_rest_api` ist identisch mit dem Original. Ein bestehender Eintrag und seine Statistiken bleiben beim Wechsel erhalten. Beide Varianten lassen sich nicht parallel installieren.

## Konfiguration

| Feld | Standard | Beschreibung |
|---|---|---|
| Host | – | IP oder Hostname des Connectivity-Moduls |
| Port | 80 | HTTP-Port |
| Benutzername | `admin` | Zugang des Moduls (im Web-Interface des Moduls änderbar) |
| Passwort | `Connectivity` | wie oben |
| Device postfix | leer | Nur für mehrere Geräte in einer HA-Instanz: Suffix für Gerät und Entities. Bei einem Gerät leer lassen. |
| Abfrageintervall | 60 s | Zu kleine Werte provozieren Timeouts, das Modul ist langsam. Bei Problemen 300 s probieren. |

Der Eintrag lässt sich über *Neu konfigurieren* ändern, danach wird die Integration neu geladen.

## Entities

Es werden nur Entities angelegt, deren Kommando der erkannte Gerätetyp laut Judo-Doku kennt.

| Entity | Kommando | Enthärter i-soft / i-soft PRO | SOFTwell | ZEWA / PROM i-SAFE, i-dos eco, i-fill |
|---|---|:-:|:-:|:-:|
| Gerätetyp, Gerätenummer, Softwareversion, Inbetriebnahme | FF, 06, 01, 0E | ✓ | ✓ | ✓ |
| Gesamtwassermenge (m³) | 28 | ✓ | – | ✓ |
| Weichwassermenge (m³) | 29 | ✓ | ✓ | – |
| Betriebszeit (Minuten/Stunden/Tage) | 25 | ✓ | ✓ | – |
| Wasserhärte (Number) | 51 / 30 | ✓ | – | – |
| Salzvorrat Masse (Number, Sensor), Salzreichweite, Salzwarnung | 56, 57 | ✓ | – | – |
| Kundendienst-Kontakt | 58 | ✓ | – | – |
| Buttons: Regeneration starten, Leckageschutz öffnen/schließen | 35, 3C, 3D | ✓ | – | – |

Hinweis: Die Tabelle zeigt, was die Filterliste im Code vorsieht. Getestet wurde bisher nur am **SOFTwell P (Typ 0x34)**.

Unbekannte Gerätetypen bekommen alle Entities (wie im Original).

### Wasserzähler im Energie-Dashboard

`Weichwassermenge` bzw. `Gesamtwassermenge` haben `device_class: water`, `state_class: total_increasing`, Einheit m³ und lassen sich direkt als Wasserverbrauch wählen. Beim SOFTwell ist die Weichwassermenge der einzige Zähler (die Gesamtwassermenge liefert dort dauerhaft 0 und wird nicht mehr abgefragt).

Einen Durchfluss gibt die API des SOFTwell nicht her. Als Näherung: Helfer *Ableitung* (Derivative) auf die Weichwassermenge, Zeiteinheit Stunden, Einheit m³/h, Zeitfenster ca. 5 min. Die Auflösung ist durch Zähler (1 l) und Intervall begrenzt.

## Funktionsweise

* Ein `DataUpdateCoordinator` fragt alle Werte zyklisch ab. Jede Adresse wird pro Zyklus nur einmal angefragt (z. B. liefert `2500` Minuten, Stunden und Tage in einer Antwort).
* **Alle Requests laufen strikt nacheinander** (Lock im Executor-Thread, `Connection: close`). Das Connectivity-Modul verarbeitet nur eine Anfrage gleichzeitig. Parallele oder abgebrochene Requests lassen es hängen, danach antwortet es nicht einmal mehr auf TCP-Ebene, bis es stromlos gemacht wurde.
* Antwortet das Gerät beim Setup nicht, wiederholt HA das Setup selbst mit wachsenden Abständen (*Einrichtungsfehler, wird erneut versucht*).
* Kommt im Betrieb keine einzige Antwort an, werden die Entities „nicht verfügbar“, statt alte Werte weiter zu zeigen.
* Schreibzugriffe (Number, Select, Buttons) gehen als `GET`-Request mit hex-kodierter Nutzlast an `/api/rest/<cmd><data>`.

## Fehlersuche

Erreichbarkeit direkt prüfen (vom HA-Host aus):

```bash
curl -s -m 10 -w ' HTTP %{http_code}\n' -u admin:Connectivity http://<ip>/api/rest/FF00
```

Erwartet: `{"data": "34"} HTTP 200` (Gerätetyp als Hex).

| Ergebnis | Bedeutung |
|---|---|
| Timeout schon beim Verbindungsaufbau | Modul hängt (Webserver/WLAN) oder falsche IP. Connectivity-Modul kurz stromlos machen, DHCP-Reservierung einrichten. |
| HTTP 401 | Benutzername oder Passwort falsch |
| `{"data": ""}` | Kommando vom Gerät nicht unterstützt oder Gerät gerade beschäftigt |

Debug-Log:

```yaml
logger:
  default: warning
  logs:
    custom_components.judo_rest_api: debug
```

Fehlgeschlagene Abrufe loggen Befehl und Ursache (`Judo REST API call <cmd> failed with ...`).

## Änderungen gegenüber dem Original

**1.0.6**
* SOFTwell: Gesamtwassermenge (0x28) nicht mehr abgefragt, neue Typcodes 59/63/5A/62/64 mit demselben Filter

**1.0.5**
* Kommandos werden nach Gerätetyp gefiltert. Auf ZEWA i-SAFE und i-fill bedeuten `5100` „Leckageschutz schließen“ und `5700`/`5800` Urlaubsmodus. Die alte Version hat diese als Leseabfragen bei jedem Zyklus gesendet.

**1.0.4**
* Strikt serielle Requests, kein Abbruch durch globales `asyncio.timeout`, jede Adresse einmal pro Zyklus
* `UpdateFailed` statt verschluckter Exceptions, `ConfigEntryNotReady` bei nicht erreichbarem Gerät
* `update_before_add` aus (Lastspitze beim Start)
* Fehlerlogs mit Befehl und Ursache, Korrektur „Passwor1“ → „Passwort“ in der deutschen Übersetzung

## Entwicklung

`custom_components/judo_rest_api/jdconst.py` enthält die Item-Liste. Neue Items bekommen bei Bedarf `exclude_types=(...)` mit den Gerätetyp-Codes (Hex, Großbuchstaben), auf denen das Kommando nicht existiert oder etwas anderes bewirkt. `judo_rest_test.py` ist ein einfaches Skript zum Abfragen der API ohne HA.

## Lizenz

Apache License 2.0, siehe [LICENSE](LICENSE).

```
Copyright 2025 OStrama und Beitragende (Original: https://github.com/OStrama/judo_rest_api)
Änderungen Copyright 2026 AndyKausG
```

Änderungen gegenüber dem Original sind in der Git-Historie und im Abschnitt [Änderungen](#änderungen-gegenüber-dem-original) dokumentiert. Beiträge zu diesem Repository stehen unter derselben Lizenz.

## Haftungsausschluss

Die Entwickler sind nicht mit Judo verbunden. Die Integration entstand als Open Source in der Freizeit auf Basis öffentlich zugänglicher Informationen. Die Nutzung erfolgt auf eigene Gefahr, es wird keine Haftung für Schäden übernommen. Das gilt besonders für Schreibzugriffe wie das Schließen des Leckageschutzes.
