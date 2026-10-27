## v2.0.2 — 27.10.2026 (PL/EN + aktualizacje)

- MENU → Narzędzia → Język / Language: ręczny wybór Polski / English / System Auto, zapisywany prywatnie w `/etc/enigma2/opencamview_settings.json`.
- Przetłumaczono komunikaty UI, kreator kamer, skaner, ONVIF, PTZ i etykiety przycisków.
- MENU → Narzędzia → Sprawdź aktualizacje / Check for updates: odczyt małego pliku HTTPS `version.json` z repozytorium i porównanie wersji, bez automatycznej instalacji.
- Nowe testy zmiany języka i obsługi poprawnych, uszkodzonych i niedostępnych manifestów.
- Zachowano kompatybilność bazy kamer, ustawienia PTZ/RTSP i poprawkę crasha z 2.0.1.

# OpenCamView changelog

## v2.0.0 — 22.10.2026 (wersja do testów na tunerach)

- Zmiana interfejsu na ciemny AIO; dynamiczne HD/FHD w granatowo-turkusowej palecie.
- Przebudowa bazy kamer z migracją 1.3, atomowym zapisem, kopią `.bak` i stałym ID domofonu.
- ONVIF (profile i URI), RTSP OPTIONS scanner zamiast zgadywania ścieżek.
- Odtwarzacz, JPEG na TV, 4 kamerowy JPEG wall, patrol, PTZ.
- Próba PiP bez zmiany kanału, z opcjonalnym FFmpeg relay i komunikatem o braku zgodności.
- Ulubione, osobny bukiet, M3U, kopie/odzyskiwanie, zabezpieczenie poświadczeń na dysku (0600).
- Źródła, skrypty budowania IPK/DEB, przygotowanie lokalnego commita GitKraken, instalator sieciowy.
- Uwaga: kompatybilność renderera, PiP, H.264/H.265 i kamer ONVIF wymaga testu na sprzęcie.

## v2.0.1 — 22.10.2026 (poprawka crasha i interfejsu)

- Naprawiono crash `TypeError: 'dict' object is not callable` po naciśnięciu zielonego klawisza „Dodaj”. W Enigma2 `Screen` dziedziczy z `dict`; nazwa `self.values` przesłaniała jego metodę `values()`. Kreator używa teraz `self.form_values`.
- Cztery kolorowe przyciski na ekranie głównym mają osobne, fizycznie zgodne barwy oraz opisy zgodne z faktycznym przypisaniem pilota.
- Poprawiono legendę skanera RTSP oraz dodano kolorowe wskazówki w odtwarzaczu i oknie JPEG/PTZ.
- Stopka na ekranach wtyczki: https://aio-iptv-projekt.pages.dev/ · data wydania: 22.10.2026 · by: Paweł Pawełek.
- Dodano test regresji odtwarzający `Screen.hide()` z OpenATV oraz testy legend i stopki.
- Aktualizacja z 2.0.0 zachowuje dotychczasowe ustawienia kamer w `/etc/enigma2/`.
