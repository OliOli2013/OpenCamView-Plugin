# Audyt OpenCamView 1.3

Analizie poddano faktyczny załączony IPK 1.3, kod `manager.py`, `scanner.py`, `ui.py`, `bouquet.py`, `skins.py` i `plugin.py`.

| Problem oryginału | Skutek | Zmiana 2.0 |
|---|---|---|
| `manager.load()` po błędzie JSON zwraca `[]`, `save()` zapisuje wprost | Możliwa utrata listy i niewykryty brak zapisu | Blokada edycji przy uszkodzeniu, `.bak`, atomowy zapis/odtworzenie |
| `domofon_index` używa indeksu listy | Domofon może wskazać niewłaściwą kamerę po usunięciu | Stałe UUID (identyfikator 32 znaków) |
| `scanner.py` używa connect_ex() i zgaduje `/stream` | Fałszywe kamery, czarny ekran | Walidacja odpowiedzi RTSP OPTIONS, ścieżka od użytkownika |
| Skaner wywołuje callback GUI z wątku | Potencjalne awarie Enigma2 | Timer GUI odpytuje stan wątków |
| MainCamScreen._on_start wywołuje stopService() | Menu przerywa TV | Menu nie zatrzymuje kanału |
| PiP bez sprawdzenia `.playService()` | Fałszywy sukces, czarne PiP | Sprawdzenie odpowiedzi, bez przejmowania obcego PiP, alternatywa JPEG |
| Brak ścisłej ochrony plików z hasłami | Ryzyko ujawnienia RTSP credentials | Ograniczenie plików do 0600, maskowanie w UI, ostrzeżenia eksportowe |
| Eksport do istniejących bukietów | Ryzyko powielania/uszkodzenia list | Tylko własny bukiet OpenCamView; bez duplikatu wpisu w `bouquets.tv` |

Ryzyka pozostające: fizyczny dekoder, możliwości PiP systemu, działanie pluginowego VideoWindow i przeźroczystości GUI, zachowanie ONVIF różnych kamer oraz kodeki wymagają walidacji na tunerze. FFmpeg remux `-c:v copy` **nie transkoduje**; nie zamieni H.265 w zgodne H.264. Hasła mogą zostać ujawnione przez logowanie URL w Enigma2, mimo ochrony plików.
