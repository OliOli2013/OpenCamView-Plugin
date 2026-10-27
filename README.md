# 📹 OpenCamView 2.0.2 – Monitoring IP dla Enigma2

**OpenCamView – by Paweł Pawełek | AIO Team**

**Wersja:** 2.0.2  
**Data wydania:** 27.10.2026  
**Autor:** Paweł Pawełek  
**Platforma:** Enigma2 / Python 3  
**Języki:** Polski / English / Auto  
**Pakiety instalacyjne:** IPK / DEB  
**Strona projektu:** https://aio-iptv-projekt.pages.dev/  
**GitHub:** https://github.com/OliOli2013/OpenCamView-Plugin

---

## 📺 Czym jest OpenCamView?

**OpenCamView** to wtyczka dla odbiorników telewizji satelitarnej i IPTV pracujących pod kontrolą Enigma2, umożliwiająca obsługę kamer IP bezpośrednio na ekranie telewizora.

Pozwala zarządzać domowym monitoringiem, oglądać obraz z kamer, korzystać z protokołów RTSP i ONVIF oraz uruchamiać wybrane funkcje bez przerywania oglądania telewizji.

Wtyczka została gruntownie przebudowana. Otrzymała nowoczesny, przejrzysty interfejs z granatowymi panelami, turkusowymi akcentami oraz kolorowymi przyciskami odpowiadającymi klawiszom pilota.

Interfejs jest przystosowany do wyświetlaczy HD i Full HD.

OpenCamView może być przydatny do obserwowania posesji, podjazdu, bramy, wejścia do domu, garażu czy innych miejsc objętych monitoringiem IP.

---

## ⭐ Najważniejsze funkcje

### 📹 Obsługa kamer IP

- Dodawanie, edytowanie i usuwanie kamer.
- Obsługa strumieni RTSP oraz adresów HTTP/HTTPS.
- Współpraca z kamerami udostępniającymi standard ONVIF.
- Konfiguracja głównego i pomocniczego strumienia.
- Obsługa zdjęć JPEG (snapshot).
- Zapisywanie ulubionych kamer.
- Przypisywanie wybranej kamery jako domofonu.
- Zachowywanie ustawień i zapisanych kamer po aktualizacji.

### 📺 Wyświetlanie obrazu

**Podgląd pełnoekranowy**

Obraz wybranej kamery można uruchomić na całym ekranie telewizora. Po zakończeniu podglądu wtyczka przywraca wcześniej oglądany kanał, o ile w międzyczasie nie nastąpiła zmiana usługi.

**Podgląd JPEG podczas oglądania TV**

Jedna z ciekawszych funkcji OpenCamView.

Pozwala wyświetlać zdjęcia z kamery na ekranie podczas oglądania programu telewizyjnego, bez konieczności przełączania na strumień kamery.

Zdjęcie odświeżane jest co kilka sekund. Nie jest to płynny obraz wideo, lecz cyklicznie aktualizowany snapshot JPEG.

**Picture-in-Picture (PiP)**

Wtyczka podejmuje próbę wyświetlenia obrazu z kamery w osobnym oknie na ekranie telewizora.

Dostępność funkcji zależy od możliwości sprzętowych odbiornika, systemu Enigma2 oraz obsługi danego strumienia wideo.

W niektórych konfiguracjach możliwe jest eksperymentalne wykorzystanie FFmpeg.

**Ściana czterech kamer**

Możliwość wyświetlania zdjęć JPEG z maksymalnie czterech kamer w jednym widoku.

**Patrol kamer**

Automatyczne przechodzenie pomiędzy wybranymi kamerami udostępniającymi zdjęcia JPEG.

---

## 🌐 ONVIF i sterowanie PTZ

OpenCamView obsługuje wybrane funkcje protokołu ONVIF, dzięki czemu można łatwiej skonfigurować zgodne kamery sieciowe.

Dostępne możliwości obejmują:

- Pobieranie informacji o urządzeniu.
- Wykrywanie profili kamery.
- Pobieranie adresów strumieni RTSP.
- Pobieranie adresów snapshot JPEG.
- Podstawowe sterowanie ruchem kamery PTZ.
- Zatrzymywanie ruchu kamery.

Sterowanie PTZ dostępne jest wyłącznie w urządzeniach obsługujących odpowiednie funkcje ONVIF.

---

## 🔍 Skaner sieci lokalnej

Wbudowany skaner LAN umożliwia wyszukiwanie urządzeń odpowiadających na zapytania RTSP w prywatnej sieci lokalnej.

Po wykryciu serwera można dodać jego adres do konfiguracji kamery.

**Ważne:** skaner nie wyszukuje haseł ani nie odgaduje ścieżek transmisji. W przypadku niektórych kamer konieczne jest ręczne wprowadzenie właściwego adresu RTSP.

---

## 🌍 NOWOŚĆ – Polski i angielski interfejs

Od wersji **OpenCamView 2.0.2** dostępna jest obsługa języka angielskiego.

Użytkownik może wybrać:

- 🇵🇱 **Polski** – polskie menu i komunikaty.
- 🇬🇧 **English** – angielskie menu i komunikaty.
- **System / Auto** – automatyczne dopasowanie języka do ustawień Enigma2.

**Zmiana języka:**

MENU → Narzędzia → Język / Language

Wybrany język zostaje zapisany. Zmiana jest stosowana na ekranie głównym bez konieczności ponownego uruchamiania GUI, a kolejne okna korzystają z nowych ustawień językowych.

Zmiana języka nie wpływa na zapisane kamery.

---

## 🔄 NOWOŚĆ – Sprawdzanie aktualizacji

OpenCamView 2.0.2 wprowadza możliwość sprawdzania dostępności nowych wydań bezpośrednio z poziomu wtyczki.

**MENU → Narzędzia → Sprawdź aktualizacje**

Funkcja sprawdza informacje o najnowszym wydaniu w oficjalnym repozytorium projektu na GitHubie.

Użytkownik otrzymuje informację, czy korzysta z aktualnej wersji, czy dostępna jest nowsza.

**Uwaga:** sprawdzanie aktualizacji nie oznacza automatycznej instalacji. Instalację nowego wydania wykonuje się osobno.

---

## 🎮 Sterowanie pilotem

| Przycisk | Funkcja |
|---|---|
| OK | Pełnoekranowy podgląd kamery |
| EXIT | Zamknij / powrót do TV |
| 🔴 Czerwony | Usuń kamerę |
| 🟢 Zielony | Dodaj kamerę |
| 🟡 Żółty | Edytuj kamerę |
| 🔵 Niebieski | Opcje / skaner LAN / ONVIF |
| INFO | Podgląd JPEG podczas oglądania TV |
| 0 | Przypisz kamerę jako domofon |
| 1 | Otwórz kamerę domofonu |
| 2 | Eksport do bukietu |
| 3 | Eksport listy M3U |
| 4 | Pomoc |
| 5 | Ulubione kamery |
| 6 | Test serwera RTSP |
| 7 | Ściana kamer JPEG |
| 8 | Patrol kamer |
| 9 | Picture-in-Picture |
| MENU | Narzędzia i ustawienia |

Funkcje kolorowych przycisków mogą zmieniać się zależnie od otwartego okna. Ich aktualne przeznaczenie jest wyświetlane na ekranie.

---

## 💾 Kopie bezpieczeństwa i ochrona ustawień

OpenCamView wyposażono w mechanizmy zabezpieczające zapisane konfiguracje kamer.

Dostępne są:

- Automatyczne kopie zapasowe.
- Ręczne tworzenie kopii konfiguracji.
- Przywracanie zapisanych ustawień.
- Odzyskiwanie bazy z kopii `.bak`.
- Kontrola poprawności wprowadzanych danych.
- Ochrona dostępu do prywatnych plików konfiguracyjnych.

Aktualizacja wtyczki nie wymaga ponownego dodawania wcześniej zapisanych kamer.

**Uwaga dotycząca prywatności:** kopie konfiguracji i eksportowane listy mogą zawierać adresy kamer oraz dane logowania. Takich plików nie należy udostępniać publicznie.

---

## 📦 Instalacja OpenCamView 2.0.2

Wtyczka jest przeznaczona dla odbiorników Enigma2 z **Pythonem 3**.

Dostępne są pakiety IPK i DEB.

### Instalacja internetowa – SSH / Telnet

`wget -q -O - https://raw.githubusercontent.com/OliOli2013/OpenCamView-Plugin/main/installer.sh | /bin/sh`

Instalator rozpoznaje dostępny menedżer pakietów, pobiera odpowiedni plik i sprawdza jego integralność za pomocą SHA-256.

### Instalacja ręczna – IPK

Dla systemów korzystających z opkg:

`opkg install /tmp/enigma2-plugin-extensions-opencamview_2.0.2_all.ipk`

### Instalacja ręczna – DEB

Dla systemów korzystających z dpkg:

`dpkg -i /tmp/enigma2-plugin-extensions-opencamview_2.0.2_all.deb`

Przed instalacją ręczną należy skopiować odpowiedni pakiet do katalogu `/tmp` odbiornika.

**Po instalacji należy uruchomić ponownie GUI Enigma2.**

### Informacja dla użytkowników aktualnej wersji

Jeżeli instalator wyświetli komunikat:

`matches the installed version`

oznacza to, że na odbiorniku jest już zainstalowana ta sama wersja OpenCamView.

System opkg może w takiej sytuacji odmówić ponownej instalacji. Nie oznacza to uszkodzenia wtyczki ani utraty zapisanych danych.

---

## 🛠 Zgodność z odbiornikami Enigma2

OpenCamView został przygotowany dla środowiska **Enigma2 / Python 3**.

Może pracować z kompatybilnymi obrazami Enigma2, takimi jak OpenATV, OpenPLi oraz innymi systemami opartymi na Pythonie 3.

Zakres dostępnych funkcji może różnić się w zależności od odbiornika.

**Istotne ograniczenia:**

- Odtwarzanie zależy od obsługi kodeków i strumieni w danym systemie.
- PiP wymaga odpowiednich możliwości sprzętowych.
- Nie wszystkie kamery wspierają ONVIF lub sterowanie PTZ.
- Podgląd JPEG wymaga dostępnego adresu snapshot.
- Eksperymentalne funkcje FFmpeg mogą wymagać dodatkowego oprogramowania.

Pakiet oznaczony jako `Architecture: all` nie gwarantuje pełnej zgodności z każdym odbiornikiem.

---

## 🆕 Historia wersji

### OpenCamView 2.0.2 – 27.10.2026

**Aktualizacja językowa i funkcjonalna**

- Dodano język angielski.
- Dodano ręczny wybór języka polskiego i angielskiego.
- Dodano automatyczny wybór języka systemowego.
- Dodano funkcję sprawdzania aktualizacji.
- Zachowano kompatybilność z konfiguracjami poprzednich wersji.
- Rozszerzono testy działania interfejsu.

### OpenCamView 2.0.1 – 22.10.2026

**Poprawki stabilności i interfejsu**

- Usunięto błąd powodujący crash Enigma2 podczas dodawania kamery.
- Poprawiono oznaczenia kolorowych przycisków.
- Usprawniono działanie kreatora kamer.
- Dodano informacje o autorze i projekcie w interfejsie.

### OpenCamView 2.0.0 – 22.10.2026

**Gruntowna przebudowa wtyczki**

- Nowy interfejs w stylu AIO.
- Rozbudowana obsługa kamer IP.
- Integracja RTSP i ONVIF.
- Podgląd JPEG na TV.
- Eksperymentalny PiP.
- Ściana kamer i patrol.
- Podstawowe sterowanie PTZ.
- Skaner sieci LAN.
- Ulubione i obsługa domofonu.
- Eksport bukietów i M3U.
- Rozbudowany system kopii bezpieczeństwa.

---

## 🤝 Informacje i wsparcie

OpenCamView jest rozwijany jako część projektów **AIO Team** dla społeczności użytkowników Enigma2.

Uwagi dotyczące działania, propozycje nowych funkcji i zgłoszenia problemów pomagają rozwijać wtyczkę i zwiększać jej zgodność z kolejnymi odbiornikami.

Przy zgłaszaniu problemów przydatne są informacje o modelu tunera, wersji systemu Enigma2 oraz opis zachowania wtyczki.

**Oficjalna strona projektu:**  
https://aio-iptv-projekt.pages.dev/

**Repozytorium OpenCamView:**  
https://github.com/OliOli2013/OpenCamView-Plugin

---

**OpenCamView 2.0.2**  
**by Paweł Pawełek | AIO Team**

*Monitoring IP bezpośrednio na Twoim odbiorniku Enigma2.*
