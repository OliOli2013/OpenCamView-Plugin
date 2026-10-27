# OpenCamView 2.0.2 — aktualizacja / GitKraken / Linux Mint

## Co się zmieniło?

- Menu → Narzędzia → **Język / Language**: Polski, English, System/Auto.
- Menu → Narzędzia → **Sprawdź aktualizacje** / **Check for updates**: odczyt pliku `version.json` po HTTPS z repozytorium GitHub i porównanie numeru wersji.
- Sprawdzanie aktualizacji nie pobiera i nie instaluje pakietów.
- Ustawienia języka trzymane są w `/etc/enigma2/opencamview_settings.json`. Baza kamer pozostaje w `/etc/enigma2/opencamview.json`.

## Aktualizacja istniejącego repozytorium GitKraken

Zakładamy, że lokalne repozytorium z wersją 2.0.1 jest w `~/Pobrane/OpenCamView-Plugin`, a ZIP pobrano do `~/Pobrane`.

```sh
cd "$HOME/Pobrane"
# Kopia źródeł i danych lokalnego repozytorium, włącznie z jego historią:
cp -a OpenCamView-Plugin "OpenCamView-Plugin-backup-$(date +%Y%m%d-%H%M%S)"
# Archiwum zawiera folder OpenCamView-Plugin. Nie zawiera katalogu .git:
unzip -oq OpenCamView-Plugin-2.0.2.zip -d "$HOME/Pobrane"
cd "$HOME/Pobrane/OpenCamView-Plugin"
PYTHONPATH=. python3 -m unittest discover -s tests -v
bash scripts/git_prepare.sh
# Po weryfikacji lokalnych zmian:
git push -u origin main
```

**Nie uruchamiaj ponownie `git init` ani nie twórz drugiego repozytorium w GitKraken.** Skrypt `git_prepare.sh` wykorzystuje istniejące repozytorium i przygotowuje lokalny commit. Po `git push` wtyczka i `version.json` będą publicznie dostępne.

Możesz także wykonać Push graficznie w GitKraken.

## Instalacja / aktualizacja na tunerze (po opublikowaniu plików)

Sposób z oficjalnego repozytorium:

```sh
wget -q -O - https://raw.githubusercontent.com/OliOli2013/OpenCamView-Plugin/main/installer.sh | /bin/sh
```

Instalator sam wybiera IPK lub DEB i sprawdza sumę SHA-256. Wymaga Pythona 3 i odpowiedniego menedżera pakietów. Po instalacji zrestartuj GUI.

Dla ręcznej instalacji prześlij pakiet do `/tmp` i użyj `opkg install /tmp/enigma2-plugin-extensions-opencamview_2.0.2_all.ipk` albo `dpkg -i /tmp/enigma2-plugin-extensions-opencamview_2.0.2_all.deb`, zależnie od systemu.

## Test na tunerze

1. Otwórz OpenCamView, sprawdź, że zapamiętane kamery są widoczne.
2. Wejdź w MENU → Narzędzia → Język / Language → English. Ekran główny, kreator, ONVIF i skaner powinny mieć angielskie etykiety.
3. Zmień język z powrotem na Polski. Sprawdź, że kamery nie zniknęły.
4. MENU → Narzędzia → Sprawdź aktualizacje. Gdy repo jest już opublikowane, pokaże 2.0.2 jako bieżącą wersję; przy braku sieci powinien pokazać błąd, nie crash.
5. W razie awarii zapisz crashlog i wersję systemu, nie publikuj pełnych URL RTSP z loginem i hasłem.

**Uwaga:** Nie sprawdzono fizycznego tunera w tym środowisku. Mechanizm aktualizacji nie umożliwia automatycznej instalacji. Wersja 2.0.2 zacznie być widoczna w sieciowym sprawdzaniu aktualizacji dopiero po `git push` nowego `version.json`.
