# OpenCamView 2.0.2 – IP Camera Viewer for Enigma2

**by: Paweł Pawełek | AIO Team**

**Wersja:** 2.0.2  
**Data wydania:** 27.10.2026  
**Autor:** Paweł Pawełek  
**Strona projektu:** https://aio-iptv-projekt.pages.dev/  
**Platforma:** Enigma2 – Python 3  
**Pakiety:** IPK / DEB  
**Języki:** Polski / English / System Auto

---

## 📹 O projekcie OpenCamView

**OpenCamView** to wtyczka przeznaczona do obsługi kamer IP, monitoringu domowego oraz kamer wejściowych i wideodomofonów na odbiornikach Enigma2.

Pozwala dodawać i zarządzać kamerami działającymi we własnej sieci lokalnej, oglądać strumienie wideo bezpośrednio na telewizorze oraz korzystać z dodatkowych funkcji podglądu podczas oglądania kanałów telewizyjnych.

Projekt został zaprojektowany z myślą o wygodnej obsłudze pilotem, czytelnym interfejsie oraz integracji z Enigma2.

Interfejs wykorzystuje granatowe panele, turkusowe akcenty i kolorowe oznaczenia przycisków, inspirowane projektami **AIO Panel** oraz **IPTV Dream**.

---

## ⭐ Najważniejsze możliwości

### Zarządzanie kamerami

- Dodawanie, edytowanie i usuwanie kamer IP.
- Obsługa adresów RTSP oraz HTTP/HTTPS.
- Konfiguracja strumienia głównego i pomocniczego.
- Obsługa adresów zdjęć JPEG (snapshot).
- Tworzenie listy ulubionych kamer.
- Przypisywanie wybranej kamery jako domofonu.
- Trwała identyfikacja zapisanych kamer.
- Bezpieczny zapis i odzyskiwanie konfiguracji.

### Podgląd obrazu

- Pełnoekranowe odtwarzanie strumienia kamery.
- Powrót do wcześniej oglądanego kanału TV.
- Podgląd zdjęć JPEG podczas oglądania telewizji.
- Eksperymentalna obsługa Picture-in-Picture (PiP).
- Ściana czterech kamer JPEG.
- Automatyczny patrol kamer.
- Regulowany czas odświeżania zdjęć.

### ONVIF i PTZ

- Wyszukiwanie profili kamer ONVIF.
- Pobieranie adresów strumieni wideo.
- Pobieranie adresów snapshotów JPEG.
- Podstawowe sterowanie ruchem kamer PTZ.
- Obsługa funkcji ContinuousMove i Stop w kompatybilnych urządzeniach.

Dostępność ONVIF i PTZ zależy od modelu kamery i jej konfiguracji.

### Skanowanie sieci LAN

- Wyszukiwanie serwerów RTSP w prywatnej sieci lokalnej.
- Sprawdzanie odpowiedzi protokołu RTSP.
- Dodawanie wykrytych adresów do konfiguracji.
- Możliwość ręcznego określenia ścieżki strumienia.

Skaner nie odgaduje automatycznie haseł ani ścieżek RTSP. Wykrycie serwera nie gwarantuje możliwości odtworzenia obrazu.

### Integracja z Enigma2

- Tworzenie osobnego bukietu kamer.
- Eksport kamer do listy M3U.
- Obsługa z poziomu pilota.
- Kopie bezpieczeństwa ustawień.
- Odzyskiwanie konfiguracji z pliku `.bak`.
- Automatyczny dobór języka lub ręczna zmiana.
- Ręczne sprawdzanie dostępności nowych wersji.

---

## 🌐 Obsługa języków PL / EN

Od wersji **2.0.2** OpenCamView obsługuje dwa języki interfejsu:

- **Polski** – polskie menu i komunikaty.
- **English** – angielskie menu i komunikaty.
- **System / Auto** – automatyczne dopasowanie do ustawień językowych Enigma2.

### Jak zmienić język?

1. Uruchom OpenCamView.
2. Naciśnij **MENU**.
3. Wybierz **Narzędzia → Język / Language**.
4. Wskaż Polski, English lub System / Auto.
5. Zatwierdź wybór przyciskiem OK.

Nowy język jest stosowany bez restartu GUI na ekranie głównym. Kolejne okna korzystają z wybranego języka.

Ustawienie jest zapisywane i pozostaje aktywne po ponownym uruchomieniu wtyczki.

Zmiana języka nie usuwa zapisanych kamer.

---

## 🔄 Sprawdzanie aktualizacji

OpenCamView posiada funkcję sprawdzania dostępności nowszej wersji.

**MENU → Narzędzia → Sprawdź aktualizacje**

Wtyczka:

- Pobiera informacje o aktualnym wydaniu z pliku `version.json` przez HTTPS.
- Porównuje wersję zainstalowaną z dostępną.
- Wyświetla informację o wyniku sprawdzenia.
- Informuje o dostępnej nowszej wersji i zmianach.

**Ważne:** funkcja jedynie sprawdza aktualizacje. Nie pobiera ani nie instaluje nowych pakietów automatycznie.

Do działania wymagany jest dostęp do internetu.

---

## 🎮 Obsługa pilota

| Przycisk | Funkcja |
|---|---|
| OK | Podgląd pełnoekranowy |
| EXIT | Powrót / zamknięcie |
| CZERWONY | Usuń kamerę |
| ZIELONY | Dodaj kamerę |
| ŻÓŁTY | Edytuj kamerę |
| NIEBIESKI | Skaner LAN / ONVIF / opcje |
| INFO | Podgląd JPEG na TV |
| 0 | Przypisz kamerę jako domofon |
| 1 | Otwórz kamerę domofonu |
| 2 | Eksport do bukietu Enigma2 |
| 3 | Eksport M3U |
| 4 | Pomoc |
| 5 | Ulubione |
| 6 | Test serwera RTSP |
| 7 | Ściana kamer JPEG |
| 8 | Patrol kamer |
| 9 | Włącz / zamknij PiP OpenCamView |
| MENU | Narzędzia i ustawienia |

Opisy kolorowych przycisków są zgodne z ich funkcjami na pilocie.

W skanerze LAN:

- Czerwony – zamknij.
- Zielony – rozpocznij skanowanie.
- Żółty – dodaj wykryty adres IP.
- Niebieski – pomoc.

W oknie JPEG niebieski przycisk otwiera podstawowe sterowanie ONVIF/PTZ, jeżeli jest dostępne.

---

## 📷 Jak dodać kamerę?

1. Uruchom OpenCamView z menu wtyczek Enigma2.
2. Naciśnij **ZIELONY** przycisk pilota.
3. Wprowadź nazwę kamery.
4. Podaj pełny adres RTSP lub HTTP/HTTPS.
5. Opcjonalnie uzupełnij adres JPEG i strumienia pomocniczego.
6. Zapisz ustawienia.
7. Zaznacz kamerę i naciśnij OK, aby uruchomić obraz.

Przykładowy format adresu RTSP:

`rtsp://LOGIN:HASLO@IP_KAMERY:554/SCIEZKA_STRUMIENIA`

Dokładna ścieżka zależy od producenta i modelu kamery.

Alternatywnie można użyć funkcji:

**NIEBIESKI → Dodaj kamerę ONVIF**

Następnie podać adres IP, port ONVIF oraz dane logowania do urządzenia.

---

## 📺 JPEG na TV i Picture-in-Picture

### JPEG na TV

Funkcja umożliwia wyświetlanie zdjęć z kamery na ekranie telewizora podczas oglądania bieżącego kanału.

Obraz jest odświeżany co kilka sekund.

Nie jest to płynny strumień wideo. Wymagany jest poprawny adres snapshot JPEG.

### PiP – obraz w obrazie

OpenCamView podejmuje próbę wyświetlenia strumienia kamery w osobnym oknie.

Działanie zależy od:

- Możliwości sprzętowych tunera.
- Systemu Enigma2.
- Obsługi drugiego dekodera.
- Kodeka i formatu strumienia kamery.
- Obsługi RTSP przez odtwarzacz.

Dostępny jest również eksperymentalny tryb pośredni FFmpeg, wymagający odpowiedniego oprogramowania na tunerze.

**PiP nie jest gwarantowany na wszystkich odbiornikach Enigma2.**

Jeśli PiP nie działa, zalecany jest podgląd JPEG na TV.

---

## 📦 Instalacja OpenCamView

Wtyczka przeznaczona jest dla odbiorników Enigma2 opartych na Pythonie 3.

Obsługiwane są pakiety IPK i DEB, zgodnie z systemem zarządzania pakietami zastosowanym w danym obrazie.

### Automatyczna instalacja przez terminal

Wykonaj:

```bash
wget -q -O - https://raw.githubusercontent.com/OliOli2013/OpenCamView-Plugin/main/installer.sh | /bin/sh
```

Instalator:

- Sprawdza obecność Pythona 3.
- Rozpoznaje dostępny menedżer pakietów.
- Pobiera odpowiedni pakiet IPK lub DEB.
- Weryfikuje sumę SHA-256.
- Uruchamia instalację pakietu.

**Po instalacji wymagany jest restart GUI Enigma2.**

### Ręczna instalacja IPK

Skopiuj pakiet do katalogu `/tmp`, następnie wykonaj:

```bash
opkg install /tmp/enigma2-plugin-extensions-opencamview_2.0.2_all.ipk
```

### Ręczna instalacja DEB

```bash
dpkg -i /tmp/enigma2-plugin-extensions-opencamview_2.0.2_all.deb
```

Nie instaluj pakietu DEB w systemie korzystającym z opkg ani IPK w systemie dpkg.

### Gdy wersja jest już zainstalowana

Jeżeli podczas instalacji pojawi się komunikat:

`matches the installed version`

oznacza to, że system posiada już tę samą wersję OpenCamView.

Nie jest to uszkodzenie pakietu. Ponowna instalacja nie jest wymagana.

Obecny instalator może w takim przypadku zakończyć działanie komunikatem błędu opkg. Nie oznacza to utraty konfiguracji.

W razie problemów z działaniem zainstalowanej wtyczki można przeprowadzić reinstalację naprawczą po wykonaniu kopii ustawień.

---

## 🔐 Konfiguracja i bezpieczeństwo

OpenCamView zapisuje konfigurację kamer w katalogu Enigma2.

**Lista kamer:**

`/etc/enigma2/opencamview.json`

**Ustawienia:**

`/etc/enigma2/opencamview_settings.json`

**Automatyczna kopia:**

`/etc/enigma2/opencamview.json.bak`

**Eksport ręczny:**

`/etc/enigma2/opencamview-export.json`

Mechanizm zapisu wykorzystuje:

- Atomowy zapis plików JSON.
- Automatyczne kopie poprzedniej konfiguracji.
- Walidację danych.
- Uprawnienia 0600 dla prywatnych plików konfiguracyjnych.
- Ochronę przed zastąpieniem uszkodzonej bazy pustą listą podczas zwykłego zapisu.

**Uwaga:** konfiguracje, pliki M3U i eksporty mogą zawierać adresy kamer wraz z loginami i hasłami. Nie należy ich publikować ani udostępniać osobom nieuprawnionym.

---

## 🆕 Historia wydań

### OpenCamView 2.0.2 – 27.10.2026

- Dodano obsługę języka polskiego i angielskiego.
- Dodano ręczny wybór języka w menu.
- Dodano automatyczne dopasowanie języka do Enigma2.
- Dodano sprawdzanie aktualizacji przez HTTPS.
- Zachowano ustawienia kamer i zgodność konfiguracji wcześniejszych wersji.
- Rozszerzono testy językowe i aktualizacji.

### OpenCamView 2.0.1 – 22.10.2026

- Naprawiono crash podczas dodawania kamery (`TypeError: 'dict' object is not callable`).
- Poprawiono kolorowe przyciski i ich opisy.
- Usprawniono nawigację i komunikaty.
- Dodano stopkę z datą, stroną i podpisem autora.

### OpenCamView 2.0.0 – 22.10.2026

- Przebudowano interfejs w stylu AIO.
- Rozbudowano zarządzanie kamerami.
- Dodano obsługę ONVIF/PTZ.
- Dodano podgląd JPEG na TV i ścianę kamer.
- Dodano patrol kamer i eksperymentalny PiP.
- Dodano eksport do bukietów i M3U.
- Rozbudowano zabezpieczenia i system kopii konfiguracji.

---

## 🛠 Testowanie i rozwój

Projekt zawiera testy automatyczne oraz skrypty budowania pakietów.

Uruchomienie testów w katalogu projektu:

```bash
PYTHONPATH=. python3 -m unittest discover -s tests -v
```

Budowanie pakietów:

```bash
bash scripts/build_packages.sh
```

Weryfikacja sum kontrolnych:

```bash
cd packages
sha256sum -c SHA256SUMS
```

Wymagane narzędzia na komputerze budującym: Python 3, dpkg-deb, ar, tar i sha256sum.

### GitKraken / Linux Mint

Przy aktualizacji kodu należy pracować w istniejącym katalogu lokalnego repozytorium, zachowując jego historię `.git`.

Przed skopiowaniem nowej wersji zaleca się wykonanie kopii projektu.

Po naniesieniu zmian należy sprawdzić status Git, wykonać testy, utworzyć commit i przesłać go na gałąź `main`.

Nie należy ponownie inicjalizować istniejącego repozytorium ani kopiować do niego obcego katalogu `.git`.

---

## ⚠️ Kompatybilność i ograniczenia

OpenCamView rozwijany jest z myślą o obrazach Enigma2 korzystających z Pythona 3, między innymi OpenATV, OpenPLi i podobnych.

Nie oznacza to jednak gwarancji działania wszystkich funkcji na każdej wersji systemu.

Obsługa odtwarzania, kodeków H.264/H.265, sprzętowego PiP oraz funkcji ONVIF/PTZ może różnić się zależnie od modelu odbiornika i kamery.

Testy zgodności nadal trwają.

W przypadku wystąpienia problemu warto podać model tunera, wersję systemu, wersję Pythona i opis problemu. Jeśli wystąpi crash, można dołączyć log po usunięciu z niego danych dostępu do kamer.

---

## 🌐 Strona projektu

**AIO TunerHub – AIO Team**

https://aio-iptv-projekt.pages.dev/

Zapraszam do testowania, zgłaszania błędów oraz proponowania kolejnych funkcji.

Celem OpenCamView jest stworzenie praktycznego i wygodnego narzędzia do monitoringu domowego, zintegrowanego z Enigma2.

**OpenCamView – by: Paweł Pawełek**  
**© 2026 AIO Team**
