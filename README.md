# OpenCamView 2.0.2 — by: Paweł Pawełek

Kompletnie przebudowana wtyczka do domowego monitoringu IP/RTSP/ONVIF dla **Enigma2 z Pythonem 3**. Interfejs: granatowe panele, turkusowe akcenty, HD/FHD responsywny skin inspirowany AIO Panel i IPTV Dream.

**Autor:** Paweł Pawełek  
**Data wydania:** 27.10.2026
**Strona projektu:** https://aio-iptv-projekt.pages.dev/  

**Naprawiono błąd występujący w 2.0.0:** po wybraniu „Dodaj kamerę” Enigma2 wyrzucało błąd `TypeError: 'dict' object is not callable`. Przyczyną był konflikt nazwy pola formularza z metodą `dict.values()` klasy `Screen`. Wersja 2.0.1 zawierała poprawkę i test regresyjny; została zachowana w wersji 2.0.2.

## Wersja 2.0.2 – języki i aktualizacje

- **MENU → Narzędzia → Język / Language**: `Polski`, `English` albo `System / Auto` (według języka Enigma2). Wybór zapisuje się bez utraty kamer i jest stosowany natychmiast na ekranie głównym; kolejne okna otwierają się w wybranym języku.
- **MENU → Narzędzia → Sprawdź aktualizacje / Check for updates**: sprawdza `version.json` w oficjalnym repozytorium (HTTPS), porównuje wersje i wyświetla wynik oraz informacje o wydaniu. **Nie instaluje nic automatycznie**. Potrzebny dostęp do internetu.
- Nowy plik `version.json` jest publikowany przy każdym wydaniu i musi być aktualizowany wraz z pakietami IPK/DEB oraz `installer.sh`.

## Nowości

- Dodawanie/edycja kamer RTSP, HTTPS/HTTP, adres JPEG, strumień pomocniczy.
- ONVIF: GetCapabilities, GetProfiles, GetStreamUri i GetSnapshotUri; podstawowe PTZ ContinuousMove/Stop tam, gdzie kamera to obsługuje.
- Skanowanie prywatnego LAN /24 z potwierdzeniem odpowiedzi RTSP zamiast samego otwartego portu. Rzeczywista ścieżka kamery musi być znana.
- Podgląd pełnoekranowy z zachowaniem poprzednio oglądanego kanału (o ile użytkownik w międzyczasie nie zmienił usługi).
- **JPEG na oglądanym kanale TV** (statyczny obraz odświeżany co kilka sekund, nie płynny film) bez drugiego dekodera.
- Sprzętowy PiP **best-effort** i eksperymentalny relay FFmpeg/HTTP MPEG-TS, jeśli PiP natywnie odrzuca RTSP. Żadnego gwarantowanego PiP na każdym tunerze.
- Ściana 4 JPEG, patrol kamer, ulubione, domofon przypisany stabilnym ID, oddzielny bukiet, M3U.
- Atomowy zapis JSON, automatyczny `.bak`, ręczny backup i restore, ochrona plików z hasłami uprawnieniami 0600, walidacja adresów.

## Pilot

| Klawisz | Funkcja |
|---|---|
| OK | Pełny obraz; EXIT powrót |
| Czerwony / Zielony / Żółty / Niebieski | Usuń / dodaj / edytuj / opcje LAN |
| INFO | JPEG na oglądanym programie TV |
| 0 / 1 | Przypisz domofon / otwórz domofon |
| 2 / 3 / 4 | Bukiet / M3U / pomoc |
| 5 / 6 | Ulubione / test RTSP |
| 7 / 8 / 9 | Ściana JPEG / patrol / PiP (ponownie 9 zamyka własny PiP) |
| MENU | Kopia, przywracanie, naprawa bazy, eksport |
| Niebieski w oknie JPEG | Podstawowe PTZ (jeśli ONVIF dostępny) |

W skanerze: **czerwony** — zamknij, **zielony** — skanuj, **żółty** — dodaj znalezione IP, **niebieski** — pomoc. W oknie JPEG: **czerwony** — zamknij, **niebieski** — ONVIF/PTZ. Każdy kolor ma własne tło odpowiadające pilotowi.

## Instalacja pakietu

Skopiuj do `/tmp` na tunerze właściwy pakiet. **IPK dla opkg:**

```sh
opkg install /tmp/enigma2-plugin-extensions-opencamview_2.0.2_all.ipk
```

**DEB dla dpkg:**

```sh
dpkg -i /tmp/enigma2-plugin-extensions-opencamview_2.0.2_all.deb
```

Uruchom ponownie GUI. Pakiety są `Architecture: all` i nie zawierają kodu maszynowego. Nie oznacza to gwarantowanej obsługi wszystkich obrazów Enigma2 ani kodeków. FFmpeg jest opcjonalny. Nie instaluj DEB w systemie opkg.

### Instalator internetowy po opublikowaniu repozytorium

```sh
wget -q -O - https://raw.githubusercontent.com/OliOli2013/OpenCamView-Plugin/main/installer.sh | /bin/sh
```

**To polecenie będzie instalować wydanie 2.0.2 dopiero po przesłaniu nowych plików do repozytorium GitHub.** Instalator automatycznie wybiera format i sprawdza SHA-256.

## GitKraken / Linux Mint

1. Otwórz istniejące lokalne repozytorium `OpenCamView-Plugin` w GitKraken na Linux Mint.
2. Rozpakuj paczkę aktualizacji `OpenCamView-Plugin-2.0.2.zip` i skopiuj pliki z katalogu `OpenCamView-Plugin/` do istniejącego repozytorium lokalnego, z zastąpieniem zmienionych plików. NIE kopiuj `.git` (paczka nie zawiera `.git`).
3. W terminalu GitKraken w katalogu istniejącego repozytorium wykonaj:

```sh
bash scripts/git_prepare.sh
```

Skrypt doda zmienione pliki i przygotuje lokalny commit, bez automatycznej publikacji. Następnie wykonaj `Push → origin/main`. Zachowaj dotychczasowy katalog `.git`.

## Dane, backup i bezpieczeństwo

Dane: `/etc/enigma2/opencamview.json`, ustawienia: `/etc/enigma2/opencamview_settings.json`, automatyczna kopia `.bak`, backup ręczny `/etc/enigma2/opencamview-export.json`. **Pliki JSON, M3U, bukietów mogą zawierać hasła** — nie umieszczaj ich na GitHub i nie publikuj zrzutów z pełnymi URL.

Podstawowy test RTSP OPTIONS **nie dowodzi możliwości odtwarzania obrazu ani poprawności hasła**. Podgląd PiP i ONVIF PTZ różnią się pomiędzy tunerami i producentami kamer. Przeprowadź checklistę `docs/TESTY_TUNER_PL.md`.

## Test i przebudowa na Linux Mint

```sh
PYTHONPATH=. python3 -m unittest discover -s tests -v
bash scripts/build_packages.sh
cd packages && sha256sum -c SHA256SUMS
```

Wymagane lokalnie: Python 3, `dpkg-deb`, `ar`, `tar`, `sha256sum`.

**Ważne:** sprawdzenie online zacznie pokazywać 2.0.2 po przesłaniu `version.json`, `installer.sh` i pakietów 2.0.2 do gałęzi `main`. Wydanie musi być opublikowane jako komplet plików w jednym commicie.
