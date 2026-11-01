# OpenCamView 2.0.3 — kamery IP dla Enigma2

**Autor:** Paweł Pawełek | AIO Team  
**Wydanie:** 1 listopada 2026  
**System:** Enigma2 z Pythonem 3  
**Języki:** polski, angielski, włoski, niemiecki, arabski, rosyjski (plus System / Auto)  
**Strona:** https://aio-iptv-projekt.pages.dev/

## O wtyczce

OpenCamView służy do obsługi domowego monitoringu IP/RTSP/ONVIF na odbiornikach Enigma2. Pozwala dodawać i edytować kamery, uruchamiać podgląd strumienia, oglądać odświeżane zdjęcia JPEG na tle oglądanego kanału, sterować podstawowymi funkcjami ONVIF/PTZ oraz skanować prywatną sieć LAN. Dostępne są także ulubione, domofon, ściana czterech obrazów JPEG, patrol kamer, eksport do bukietu i M3U oraz kopie konfiguracji.

**Ograniczenia:** podgląd JPEG nie jest płynnym wideo; PiP i przekazywanie strumieni przez FFmpeg są eksperymentalne i zależą od tunera oraz kodeków. Skaner nie odgaduje ścieżek RTSP ani haseł. Funkcje ONVIF/PTZ zależą od kamery.

## Nowości w wersji 2.0.3

- **Sześć języków interfejsu:** polski, angielski, włoski (tłumaczenie społeczności LinuxSat), niemiecki, arabski i rosyjski.
- **System / Auto** rozpoznaje ustawiony język Enigma2, jeśli jest obsługiwany. Wybór języka jest zapisywany i nie usuwa kamer.
- **Sprawdzanie aktualizacji** wyświetla wynik we wszystkich sześciu językach; niczego nie instaluje automatycznie.
- **Instalator** rozpoznaje już zainstalowaną tę samą wersję i nie zgłasza błędu ponownej instalacji.
- Zachowano poprawkę awarii kreatora kamer z 2.0.1.

**Uwaga o języku arabskim:** poprawność kształtowania liter i kierunku tekstu (RTL) zależy także od fontów i silnika tekstowego obrazu Enigma2. Tłumaczenia są dostępne, ale zgodność wyświetlania wymaga sprawdzenia na tunerze.

## Zmiana języka

**OpenCamView → MENU → Narzędzia → Język / Language**. Wybierz Polski, English, Italiano, Deutsch, العربية, Русский lub System / Auto. Główny ekran zmienia język od razu, następne okna otwierają się w wybranym języku.

## Sterowanie pilotem

| Klawisz | Funkcja |
|---|---|
| OK / EXIT | Pełny podgląd / powrót |
| Czerwony / zielony / żółty / niebieski | Usuń / dodaj / edytuj / opcje LAN i ONVIF |
| INFO | JPEG na oglądanym kanale TV |
| 0 / 1 | Ustaw / otwórz kamerę domofonu |
| 2 / 3 / 4 | Bukiet / M3U / pomoc |
| 5 / 6 | Ulubione / test RTSP |
| 7 / 8 / 9 | Ściana JPEG / patrol / PiP |
| MENU | Narzędzia, język, aktualizacje, kopie |

## Instalacja i aktualizacja

W terminalu tunera Enigma2 (SSH/Telnet):

```sh
wget -q -O - https://raw.githubusercontent.com/OliOli2013/OpenCamView-Plugin/main/installer.sh | /bin/sh
```

Instalator dobiera IPK dla `opkg` lub DEB dla `dpkg`, pobiera pakiet z oficjalnego repozytorium i weryfikuje SHA-256. **Po instalacji uruchom ponownie GUI Enigma2.** Przy ponownym uruchomieniu instalatora tej samej wersji zobaczysz komunikat, że aktualizacja nie jest wymagana.

Instalacja ręczna z pliku skopiowanego do `/tmp`:

- IPK: `opkg install /tmp/enigma2-plugin-extensions-opencamview_2.0.3_all.ipk`
- DEB: `dpkg -i /tmp/enigma2-plugin-extensions-opencamview_2.0.3_all.deb`

Nie instaluj DEB na obrazie opkg ani IPK na obrazie dpkg. Obsługa wszystkich systemów Enigma2 nie jest gwarantowana.

## Ustawienia, backup i prywatność

Konfiguracje kamer i ustawień przechowywane są w `/etc/enigma2/` (pliki `opencamview.json` oraz `opencamview_settings.json`). Dostępne są automatyczne kopie `.bak` i eksport ręczny. Listy M3U oraz pliki JSON mogą zawierać loginy, hasła i prywatne URL — **nie udostępniaj ich publicznie**.

## Historia zmian

- **2.0.3 (01.11.2026):** PL/EN/IT/DE/AR/RU, wielojęzyczne aktualizacje, ulepszony instalator.
- **2.0.2 (27.10.2026):** polski i angielski, ręczne sprawdzanie aktualizacji.
- **2.0.1 (22.10.2026):** poprawka awarii podczas dodawania kamery, poprawione kolorowe przyciski.
- **2.0.0 (22.10.2026):** przebudowa interfejsu i obsługi monitoringu.

**Projekt:** https://github.com/OliOli2013/OpenCamView-Plugin  
**by Paweł Pawełek | AIO Team**
