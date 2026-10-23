# Checklista testów na fizycznym tunerze Enigma2

1. Zrób kopię `opencamview*.json`. Zainstaluj IPK albo DEB zgodny z systemem i zrestartuj GUI.
2. Otwórz menu OpenCamView podczas oglądania TV: kanał nie powinien się zatrzymać.
3. Dodaj kamerę z poprawnym RTSP, sprawdź OK → obraz i EXIT → powrót do poprzedniego kanału.
4. Dodaj URL snapshotu JPEG (nie multipart MJPEG), wybierz INFO. Sprawdź podgląd małego okna na TV, datę odświeżenia, brak starego obrazu po utracie łączności.
5. Dodaj cztery snapshoty. Klawisz 7 wyświetla ścianę, 8 przełącza kamery, CH+/CH- zmienia ręcznie.
6. NIEBIESKI → skaner LAN. Sprawdź poprawność odpowiedzi RTSP i możliwość anulowania skanowania bez crashloga.
7. NIEBIESKI → ONVIF: login/hasło/port, wybór profilu, próbne RTSP/JPEG. Podczas pierwszego PTZ obserwuj fizyczny ruch kamery.
8. Przy TV wybierz 9 (PiP). Jeśli unsupported, sprawdź JPEG. Relay FFmpeg włączaj tylko testowo, jeśli obraz/system to obsługuje. Powtórne 9 po powrocie do menu zamyka nasze PiP.
9. Ustaw domofon klawiszem 0, usuń inną kamerę, otwórz domofon klawiszem 1; identyfikator nie powinien się przemieścić.
10. Eksport 2 i 3: osobny bukiet nie zmienia innych; M3U może zawierać hasła. Sprawdź kopie MENU → backup/restore i odzyskiwanie `.bak`.
11. Zapisz model, obraz, wersję Pythona, kodek kamery i log z każdego nieudanego testu **po usunięciu poświadczeń**.

Diagnostyka:

```sh
python3 --version
ls -l /etc/enigma2/opencamview*.json
command -v ffmpeg || echo 'Relay FFmpeg niedostepny'
```

Odinstalowanie: `opkg remove enigma2-plugin-extensions-opencamview` lub `dpkg -r enigma2-plugin-extensions-opencamview`; restart GUI. Konfiguracja jest poza pakietem.
