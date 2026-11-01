# -*- coding: utf-8 -*-
"""User-facing OpenCamView translations: Polish, English, Italian, German, Arabic, Russian.

Keys are the historical Polish source strings, preserved for API compatibility.
Foreign-language translations are loaded as plain Python dicts without dependencies.
Arabic shaping and bidirectional display depend on the Enigma2 image and fonts.
"""
from .locale_extra import DE, RU, AR

EN = {'\nOK: strumien kamery\nINFO: JPEG na TV bez zmiany kanalu\n9: PiP — tylko wspierane tunery\n0/1: domofon, 5: ulubione, 6: test RTSP\n7: sciana, 8: patrol\nNIEBIESKI: skan LAN i ONVIF\nMENU: kopia, odzyskiwanie, eksport': '\n'
                                                                                                                                                                                                                               'OK: '
                                                                                                                                                                                                                               'camera '
                                                                                                                                                                                                                               'stream\n'
                                                                                                                                                                                                                               'INFO: '
                                                                                                                                                                                                                               'JPEG '
                                                                                                                                                                                                                               'on '
                                                                                                                                                                                                                               'TV '
                                                                                                                                                                                                                               'without '
                                                                                                                                                                                                                               'changing '
                                                                                                                                                                                                                               'channels\n'
                                                                                                                                                                                                                               '9: '
                                                                                                                                                                                                                               'PiP '
                                                                                                                                                                                                                               '— '
                                                                                                                                                                                                                               'supported '
                                                                                                                                                                                                                               'receivers '
                                                                                                                                                                                                                               'only\n'
                                                                                                                                                                                                                               '0/1: '
                                                                                                                                                                                                                               'doorbell, '
                                                                                                                                                                                                                               '5: '
                                                                                                                                                                                                                               'favorites, '
                                                                                                                                                                                                                               '6: '
                                                                                                                                                                                                                               'RTSP '
                                                                                                                                                                                                                               'test\n'
                                                                                                                                                                                                                               '7: '
                                                                                                                                                                                                                               'wall, '
                                                                                                                                                                                                                               '8: '
                                                                                                                                                                                                                               'patrol\n'
                                                                                                                                                                                                                               'BLUE: '
                                                                                                                                                                                                                               'LAN '
                                                                                                                                                                                                                               'scan '
                                                                                                                                                                                                                               'and '
                                                                                                                                                                                                                               'ONVIF\n'
                                                                                                                                                                                                                               'MENU: '
                                                                                                                                                                                                                               'backup, '
                                                                                                                                                                                                                               'recovery, '
                                                                                                                                                                                                                               'export, '
                                                                                                                                                                                                                               'language, '
                                                                                                                                                                                                                               'updates',
 ' — pobieranie JPEG': ' — downloading JPEG',
 '%d kamer': '%d cameras',
 '%s   |   OK/EXIT: powrót do TV': '%s   |   OK/EXIT: return to TV',
 'Adres JPEG / snapshot (opcjonalnie)': 'JPEG / snapshot URL (optional)',
 'Anuluj': 'Cancel',
 'BLAD BAZY! MENU -> napraw z .bak: ': 'DATABASE ERROR! MENU -> recover from .bak: ',
 'BLAD JPEG: ': 'JPEG ERROR: ',
 'BRAK': 'NONE',
 'BRAK adresu': 'NO URL',
 'Baza uszkodzona: %s. Przywroc .bak!': 'Database corrupted: %s. Restore .bak!',
 'Blad dekodowania JPEG': 'JPEG decoding error',
 'Blad zapisu: ': 'Save error: ',
 'Blad: ': 'Error: ',
 'Bledna lista kamer': 'Invalid camera list',
 'Bledny host/port': 'Invalid host/port',
 'Brak ONVIF Media': 'ONVIF Media not available',
 'Brak ONVIF/PTZ': 'ONVIF/PTZ not available',
 'Brak adresu JPEG kamery': 'Camera JPEG URL is missing',
 'Brak automatycznej kopii .bak': 'Automatic .bak backup not found',
 'Brak ffmpeg w obrazie Enigma2': 'FFmpeg is not installed in this Enigma2 image',
 'Brak kamer': 'No cameras',
 'Brak kamer z adresem JPEG': 'No cameras with a JPEG URL',
 'Brak kamer. ZIELONY = dodaj kamere': 'No cameras. GREEN = add a camera',
 'Brak listy kamer w kopii': 'No camera list in backup',
 'Brak lokalnego IPv4': 'No local IPv4 address',
 'Brak naszego PiP': 'No OpenCamView PiP active',
 'Brak odpowiedzi RTSP': 'No RTSP response',
 'Błąd zmiany języka: ': 'Language change error: ',
 'DOMOFON ': 'DOORBELL ',
 'Dodaj': 'Add',
 'Dodaj IP': 'Add IP',
 'Dodaj adres snapshot JPEG w edycji kamery': 'Please enter a JPEG snapshot URL in camera settings',
 'Dodaj adresy zdjec JPEG': 'Please configure JPEG URLs',
 'Dodaj kamere ONVIF': 'Add ONVIF camera',
 'Dodano profil ONVIF': 'ONVIF profile added',
 'Dodano; edytuj URL aby dopisac login i haslo': 'Added; edit URL to include username and password',
 'Dol': 'Down',
 'Drugi dekoder odrzucil strumien': 'The second decoder rejected this stream',
 'Edytuj': 'Edit',
 'Eksport M3U': 'Export M3U',
 'Eksport bukietu': 'Export bouquet',
 'Gora': 'Up',
 'Haslo ONVIF': 'ONVIF password',
 'IP kamery ONVIF': 'ONVIF camera IP',
 'Inny PiP jest aktywny': 'Another PiP window is already active',
 'JPEG na TV': 'JPEG on TV',
 'JPEG: odświeżanie co kilka sekund | CH +/-: patrol': 'JPEG: refreshes every few seconds | CH +/-: patrol',
 'Kamera ': 'Camera ',
 'Kamery IP w Twojej sieci domowej': 'IP cameras on your home network',
 'Konfiguracja zbyt duza': 'Configuration too large',
 'Kopia ustawien (z haslami!)': 'Backup settings (includes passwords!)',
 'Kopia z haslami: ': 'Backup with passwords: ',
 'Lewo': 'Left',
 'Login ONVIF': 'ONVIF username',
 'M3U moze zawierac hasla RTSP. Kontynuowac?': 'M3U may contain RTSP passwords. Continue?',
 'MONITORING DOMOWY\n\nKamery IP, RTSP i ONVIF\nPodglad bez list IPTV\n\nNIEBIESKI — skaner/ONVIF\nMENU — dodatkowe narzedzia': 'HOME '
                                                                                                                                'MONITORING\n'
                                                                                                                                '\n'
                                                                                                                                'IP '
                                                                                                                                'cameras, '
                                                                                                                                'RTSP '
                                                                                                                                'and '
                                                                                                                                'ONVIF\n'
                                                                                                                                'Preview '
                                                                                                                                'without '
                                                                                                                                'IPTV '
                                                                                                                                'lists\n'
                                                                                                                                '\n'
                                                                                                                                'BLUE '
                                                                                                                                '— '
                                                                                                                                'scanner/ONVIF\n'
                                                                                                                                'MENU '
                                                                                                                                '— '
                                                                                                                                'additional '
                                                                                                                                'tools',
 'Najpierw odzyskaj uszkodzona baze z .bak': 'Recover corrupted database from .bak first',
 'Napraw baze z automatycznej .bak': 'Recover database from automatic .bak',
 'Narzedzia OpenCamView': 'OpenCamView tools',
 'Nazwa kamery': 'Camera name',
 'Nazwa kamery musi miec 1-90 znakow': 'Camera name must be 1–90 characters',
 'Nie wykryto strumieni ONVIF': 'No ONVIF streams found',
 'Niedozwolony plik': 'Disallowed file',
 'Niedozwolony protokol': 'Unsupported protocol',
 'Nieprawidlowe ID': 'Invalid ID',
 'Nieprawidlowy PTZ': 'Invalid PTZ',
 'Nieprawidlowy URL': 'Invalid URL',
 'Nieprawidlowy URL: %s': 'Invalid URL: %s',
 'Nieprawidlowy adres': 'Invalid address',
 'Nieprawidlowy plik konfiguracji': 'Invalid configuration file',
 'OK: Dodaj kamerę   EXIT: Powrót   Skaner nie odgaduje hasła ani ścieżki RTSP': 'OK: Add camera   EXIT: Back   '
                                                                                 'Scanner cannot guess RTSP '
                                                                                 'passwords or paths',
 'OK: Odtwórz   INFO: JPEG na TV   5: Ulubione   9: PiP   MENU: Narzędzia   EXIT': 'OK: Play   INFO: JPEG on TV   '
                                                                                   '5: Favorites   9: PiP   MENU: '
                                                                                   'Tools   EXIT',
 'Opcje / LAN': 'Options / LAN',
 'OpenCamView — funkcje': 'OpenCamView — features',
 'OpenCamView — skaner RTSP LAN': 'OpenCamView — RTSP LAN scanner',
 'Operacja zastapi obecna liste kamer. Kontynuowac?': 'This will replace the current camera list. Continue?',
 'PTZ / ONVIF': 'PTZ / ONVIF',
 'PTZ blad: ': 'PTZ error: ',
 'PTZ — wykonano ruch': 'PTZ — movement completed',
 'Patrol kamer': 'Camera patrol',
 'Pelny adres RTSP/HTTP': 'Full RTSP/HTTP URL',
 'PiP kamery': 'Camera PiP',
 'PiP niedostepne: %s': 'PiP unavailable: %s',
 'PiP zamkniety': 'PiP closed',
 'Pobieram profile ONVIF...': 'Loading ONVIF profiles...',
 'Podglad JPEG na TV': 'JPEG preview on TV',
 'Pomoc': 'Help',
 'Port': 'Port',
 'Port ONVIF': 'ONVIF port',
 'Powtorzone ID': 'Duplicate IDs',
 'Prawo': 'Right',
 'Protokol/host': 'Protocol/host',
 'Przywroc kopie reczna': 'Restore manual backup',
 'Przywrocono %d kamer': 'Restored %d cameras',
 'Rzeczywista sciezka RTSP (np. /Streaming/Channels/101)': 'Actual RTSP path (e.g. /Streaming/Channels/101)',
 'Sciana 4 kamer': '4-camera wall',
 'Serwer nie zwrocil poprawnego JPEG (maks 2 MiB)': 'Server returned invalid JPEG (max 2 MiB)',
 'Skan dozwolony tylko dla prywatnej podsieci /24 lub mniejszej': 'Scan permitted only for private /24 subnet or '
                                                                  'smaller',
 'Skanowanie RTSP...': 'Scanning RTSP...',
 'Skanuj LAN': 'Scan LAN',
 'Skanuj RTSP w sieci domowej': 'Scan RTSP on home network',
 'Skanuj sieć lokalną przyciskiem zielonym. Zaznacz wykryte urządzenie i naciśnij żółty lub OK, aby dodać adres RTSP. Wpisz poprawną ścieżkę strumienia.': 'Press '
                                                                                                                                                           'GREEN '
                                                                                                                                                           'to '
                                                                                                                                                           'scan '
                                                                                                                                                           'your '
                                                                                                                                                           'LAN. '
                                                                                                                                                           'Select '
                                                                                                                                                           'a '
                                                                                                                                                           'device '
                                                                                                                                                           'and '
                                                                                                                                                           'press '
                                                                                                                                                           'YELLOW '
                                                                                                                                                           'or '
                                                                                                                                                           'OK '
                                                                                                                                                           'to '
                                                                                                                                                           'add '
                                                                                                                                                           'its '
                                                                                                                                                           'RTSP '
                                                                                                                                                           'URL. '
                                                                                                                                                           'Enter '
                                                                                                                                                           'the '
                                                                                                                                                           'correct '
                                                                                                                                                           'stream '
                                                                                                                                                           'path.',
 'Sprawdzam aktualizacje...': 'Checking for updates...',
 'Sprawdź aktualizacje': 'Check for updates',
 'Sprobuj FFmpeg relay — eksperymentalne': 'Try FFmpeg relay — experimental',
 'Sterowanie PTZ': 'PTZ controls',
 'Strumien pomocniczy (opcjonalnie)': 'Substream URL (optional)',
 'TAK': 'YES',
 'Test dotyczy RTSP': 'This test supports RTSP only',
 'Test serwera RTSP...': 'Testing RTSP server...',
 'Trwa poprzednia operacja': 'Another operation is in progress',
 'Tuner nie obsluguje PiP': 'This receiver does not support PiP',
 'Usunac kamere %s?': 'Delete camera %s?',
 'Usuń': 'Delete',
 'Utworzono osobny bukiet: ': 'Created a separate bouquet: ',
 'WYBRANA KAMERA\n\n%s\n\n%s\n\nJPEG: %s\n\nONVIF PTZ: %s\n\n0 Domofon\n1 Otworz domofon\n2 Bukiet / 3 M3U\n6 Test RTSP\n7 Sciana / 8 Patrol': 'SELECTED '
                                                                                                                                               'CAMERA\n'
                                                                                                                                               '\n'
                                                                                                                                               '%s\n'
                                                                                                                                               '\n'
                                                                                                                                               '%s\n'
                                                                                                                                               '\n'
                                                                                                                                               'JPEG: '
                                                                                                                                               '%s\n'
                                                                                                                                               '\n'
                                                                                                                                               'ONVIF '
                                                                                                                                               'PTZ: '
                                                                                                                                               '%s\n'
                                                                                                                                               '\n'
                                                                                                                                               '0 '
                                                                                                                                               'Set '
                                                                                                                                               'doorbell\n'
                                                                                                                                               '1 '
                                                                                                                                               'Open '
                                                                                                                                               'doorbell\n'
                                                                                                                                               '2 '
                                                                                                                                               'Bouquet '
                                                                                                                                               '/ '
                                                                                                                                               '3 '
                                                                                                                                               'M3U\n'
                                                                                                                                               '6 '
                                                                                                                                               'RTSP '
                                                                                                                                               'test\n'
                                                                                                                                               '7 '
                                                                                                                                               'Wall '
                                                                                                                                               '/ '
                                                                                                                                               '8 '
                                                                                                                                               'Patrol',
 'Wybierz profil ONVIF': 'Select ONVIF profile',
 'Wykrywanie prawdziwych odpowiedzi RTSP.\nWpisz sciezke obrazu po znalezieniu serwera.\nNie kazdy otwarty port jest kamera.': 'Detecting '
                                                                                                                               'real '
                                                                                                                               'RTSP '
                                                                                                                               'responses.\n'
                                                                                                                               'Enter '
                                                                                                                               'the '
                                                                                                                               'stream '
                                                                                                                               'path '
                                                                                                                               'after '
                                                                                                                               'discovering '
                                                                                                                               'a '
                                                                                                                               'server.\n'
                                                                                                                               'Not '
                                                                                                                               'every '
                                                                                                                               'open '
                                                                                                                               'port '
                                                                                                                               'is '
                                                                                                                               'a '
                                                                                                                               'camera.',
 'ZIELONY: skanuj prywatna siec /24': 'GREEN: scan a private /24 subnet',
 'Zamknieto PiP OpenCamView': 'OpenCamView PiP closed',
 'Zamknij': 'Close',
 'Zamknij PiP': 'Close PiP',
 'Zapisano ustawienia kamery': 'Camera settings saved',
 'Zaznacz kamere i wcisnij 0 aby przypisac domofon': 'Select a camera and press 0 to set it as doorbell',
 'Zla sciezka': 'Invalid path',
 'Zle ustawienia': 'Invalid settings',
 'Zly format kopii': 'Invalid backup format',
 'Zmieniono język OpenCamView.': 'OpenCamView language changed.',
 'Znaleziono %d serwerow': 'Found %d servers',
 '[ukryty adres]': '[hidden URL]',
 'Kamery IP / RTSP / ONVIF': 'IP / RTSP / ONVIF cameras'}

IT = {'\nOK: strumien kamery\nINFO: JPEG na TV bez zmiany kanalu\n9: PiP — tylko wspierane tunery\n0/1: domofon, 5: ulubione, 6: test RTSP\n7: sciana, 8: patrol\nNIEBIESKI: skan LAN i ONVIF\nMENU: kopia, odzyskiwanie, eksport': '\n'
                                                                                                                                                                                                                               'OK: '
                                                                                                                                                                                                                               'stream '
                                                                                                                                                                                                                               'telecamera\n'
                                                                                                                                                                                                                               'INFO: '
                                                                                                                                                                                                                               'JPEG '
                                                                                                                                                                                                                               'su '
                                                                                                                                                                                                                               'TV '
                                                                                                                                                                                                                               'senza '
                                                                                                                                                                                                                               'cambiare '
                                                                                                                                                                                                                               'canale\n'
                                                                                                                                                                                                                               '9: '
                                                                                                                                                                                                                               'PiP '
                                                                                                                                                                                                                               '— '
                                                                                                                                                                                                                               'solo '
                                                                                                                                                                                                                               'ricevitori '
                                                                                                                                                                                                                               'supportati\n'
                                                                                                                                                                                                                               '0/1: '
                                                                                                                                                                                                                               'citofono, '
                                                                                                                                                                                                                               '5: '
                                                                                                                                                                                                                               'preferiti, '
                                                                                                                                                                                                                               '6: '
                                                                                                                                                                                                                               'test '
                                                                                                                                                                                                                               'RTSP\n'
                                                                                                                                                                                                                               '7: '
                                                                                                                                                                                                                               'muro, '
                                                                                                                                                                                                                               '8: '
                                                                                                                                                                                                                               'pattuglia\n'
                                                                                                                                                                                                                               'BLU: '
                                                                                                                                                                                                                               'scansione '
                                                                                                                                                                                                                               'LAN '
                                                                                                                                                                                                                               'e '
                                                                                                                                                                                                                               'ONVIF\n'
                                                                                                                                                                                                                               'MENU: '
                                                                                                                                                                                                                               'backup, '
                                                                                                                                                                                                                               'ripristino, '
                                                                                                                                                                                                                               'esporta, '
                                                                                                                                                                                                                               'lingua, '
                                                                                                                                                                                                                               'aggiornamenti',
 ' — pobieranie JPEG': ' — download JPEG in corso',
 '%d kamer': '%d telecamere',
 '%s   |   OK/EXIT: powrót do TV': '%s   |   OK/EXIT: torna alla TV',
 'Adres JPEG / snapshot (opcjonalnie)': 'URL JPEG / snapshot (opzionale)',
 'Anuluj': 'Annulla',
 'BLAD BAZY! MENU -> napraw z .bak: ': 'ERRORE DATABASE! MENU -> ripristina da .bak: ',
 'BLAD JPEG: ': 'ERRORE JPEG: ',
 'BRAK': 'NESSUNO',
 'BRAK adresu': 'NESSUN URL',
 'Baza uszkodzona: %s. Przywroc .bak!': 'Database corrotto: %s. Ripristina .bak!',
 'Blad dekodowania JPEG': 'Errore di decodifica JPEG',
 'Blad zapisu: ': 'Errore di salvataggio: ',
 'Blad: ': 'Errore: ',
 'Bledna lista kamer': 'Lista telecamere non valida',
 'Bledny host/port': 'Host/porta non validi',
 'Brak ONVIF Media': 'ONVIF Media non disponibile',
 'Brak ONVIF/PTZ': 'ONVIF/PTZ non disponibile',
 'Brak adresu JPEG kamery': 'URL JPEG della telecamera mancante',
 'Brak automatycznej kopii .bak': 'Nessun backup automatico .bak trovato',
 'Brak ffmpeg w obrazie Enigma2': 'FFmpeg non installato in questa immagine Enigma2',
 'Brak kamer': 'Nessuna telecamera',
 'Brak kamer z adresem JPEG': 'Nessuna telecamera con URL JPEG',
 'Brak kamer. ZIELONY = dodaj kamere': 'Nessuna telecamera. VERDE = aggiungi una telecamera',
 'Brak listy kamer w kopii': 'Nessuna lista telecamere nel backup',
 'Brak lokalnego IPv4': 'Nessun indirizzo IPv4 locale',
 'Brak naszego PiP': 'Nessun PiP di OpenCamView attivo',
 'Brak odpowiedzi RTSP': 'Nessuna risposta RTSP',
 'Błąd zmiany języka: ': 'Errore cambio lingua: ',
 'DOMOFON ': 'CITOFONO ',
 'Dodaj': 'Aggiungi',
 'Dodaj IP': 'Aggiungi IP',
 'Dodaj adres snapshot JPEG w edycji kamery': 'Inserisci un URL snapshot JPEG nelle impostazioni della telecamera',
 'Dodaj adresy zdjec JPEG': 'Configura gli URL JPEG',
 'Dodaj kamere ONVIF': 'Aggiungi telecamera ONVIF',
 'Dodano profil ONVIF': 'Profilo ONVIF aggiunto',
 'Dodano; edytuj URL aby dopisac login i haslo': "Aggiunto; modifica l'URL per inserire nome utente e password",
 'Dol': 'Giù',
 'Drugi dekoder odrzucil strumien': 'Il secondo decoder ha rifiutato lo stream',
 'Edytuj': 'Modifica',
 'Eksport M3U': 'Esporta M3U',
 'Eksport bukietu': 'Esporta bouquet',
 'Gora': 'Su',
 'Haslo ONVIF': 'Password ONVIF',
 'IP kamery ONVIF': 'IP telecamera ONVIF',
 'Inny PiP jest aktywny': "Un'altra finestra PiP è già attiva",
 'JPEG na TV': 'JPEG su TV',
 'JPEG: odświeżanie co kilka sekund | CH +/-: patrol': 'JPEG: aggiornamento ogni pochi secondi | CH +/-: '
                                                       'pattuglia',
 'Kamera ': 'Telecamera ',
 'Kamery IP w Twojej sieci domowej': 'Telecamere IP nella tua rete domestica',
 'Konfiguracja zbyt duza': 'Configurazione troppo grande',
 'Kopia ustawien (z haslami!)': 'Backup impostazioni (include le password!)',
 'Kopia z haslami: ': 'Backup con password: ',
 'Lewo': 'Sinistra',
 'Login ONVIF': 'Nome utente ONVIF',
 'M3U moze zawierac hasla RTSP. Kontynuowac?': 'M3U può contenere password RTSP. Continuare?',
 'MONITORING DOMOWY\n\nKamery IP, RTSP i ONVIF\nPodglad bez list IPTV\n\nNIEBIESKI — skaner/ONVIF\nMENU — dodatkowe narzedzia': 'MONITORAGGIO '
                                                                                                                                'DOMESTICO\n'
                                                                                                                                '\n'
                                                                                                                                'Telecamere '
                                                                                                                                'IP, '
                                                                                                                                'RTSP '
                                                                                                                                'e '
                                                                                                                                'ONVIF\n'
                                                                                                                                'Anteprima '
                                                                                                                                'senza '
                                                                                                                                'liste '
                                                                                                                                'IPTV\n'
                                                                                                                                '\n'
                                                                                                                                'BLU '
                                                                                                                                '— '
                                                                                                                                'scanner/ONVIF\n'
                                                                                                                                'MENU '
                                                                                                                                '— '
                                                                                                                                'strumenti '
                                                                                                                                'aggiuntivi',
 'Najpierw odzyskaj uszkodzona baze z .bak': 'Ripristina prima il database corrotto da .bak',
 'Napraw baze z automatycznej .bak': 'Ripristina il database dal .bak automatico',
 'Narzedzia OpenCamView': 'Strumenti OpenCamView',
 'Nazwa kamery': 'Nome telecamera',
 'Nazwa kamery musi miec 1-90 znakow': 'Il nome della telecamera deve avere 1–90 caratteri',
 'Nie wykryto strumieni ONVIF': 'Nessuno stream ONVIF rilevato',
 'Niedozwolony plik': 'File non consentito',
 'Niedozwolony protokol': 'Protocollo non supportato',
 'Nieprawidlowe ID': 'ID non valido',
 'Nieprawidlowy PTZ': 'PTZ non valido',
 'Nieprawidlowy URL': 'URL non valido',
 'Nieprawidlowy URL: %s': 'URL non valido: %s',
 'Nieprawidlowy adres': 'Indirizzo non valido',
 'Nieprawidlowy plik konfiguracji': 'File di configurazione non valido',
 'OK: Dodaj kamerę   EXIT: Powrót   Skaner nie odgaduje hasła ani ścieżki RTSP': 'OK: Aggiungi telecamera   EXIT: '
                                                                                 'Indietro   Lo scanner non '
                                                                                 'indovina password né percorsi '
                                                                                 'RTSP',
 'OK: Odtwórz   INFO: JPEG na TV   5: Ulubione   9: PiP   MENU: Narzędzia   EXIT': 'OK: Riproduci   INFO: JPEG su '
                                                                                   'TV   5: Preferiti   9: PiP   '
                                                                                   'MENU: Strumenti   EXIT',
 'Opcje / LAN': 'Opzioni / LAN',
 'OpenCamView — funkcje': 'OpenCamView — funzioni',
 'OpenCamView — skaner RTSP LAN': 'OpenCamView — scanner RTSP LAN',
 'Operacja zastapi obecna liste kamer. Kontynuowac?': 'Questa operazione sostituirà la lista telecamere attuale. '
                                                      'Continuare?',
 'PTZ / ONVIF': 'PTZ / ONVIF',
 'PTZ blad: ': 'Errore PTZ: ',
 'PTZ — wykonano ruch': 'PTZ — movimento eseguito',
 'Patrol kamer': 'Pattuglia telecamere',
 'Pelny adres RTSP/HTTP': 'URL RTSP/HTTP completo',
 'PiP kamery': 'PiP telecamera',
 'PiP niedostepne: %s': 'PiP non disponibile: %s',
 'PiP zamkniety': 'PiP chiuso',
 'Pobieram profile ONVIF...': 'Caricamento profili ONVIF...',
 'Podglad JPEG na TV': 'Anteprima JPEG su TV',
 'Pomoc': 'Aiuto',
 'Port': 'Porta',
 'Port ONVIF': 'Porta ONVIF',
 'Powtorzone ID': 'ID duplicati',
 'Prawo': 'Destra',
 'Protokol/host': 'Protocollo/host',
 'Przywroc kopie reczna': 'Ripristina backup manuale',
 'Przywrocono %d kamer': 'Ripristinate %d telecamere',
 'Rzeczywista sciezka RTSP (np. /Streaming/Channels/101)': 'Percorso RTSP effettivo (es. /Streaming/Channels/101)',
 'Sciana 4 kamer': 'Muro 4 telecamere',
 'Serwer nie zwrocil poprawnego JPEG (maks 2 MiB)': 'Il server non ha restituito un JPEG valido (max 2 MiB)',
 'Skan dozwolony tylko dla prywatnej podsieci /24 lub mniejszej': 'Scansione consentita solo per subnet private '
                                                                  '/24 o inferiori',
 'Skanowanie RTSP...': 'Scansione RTSP...',
 'Skanuj LAN': 'Scansiona LAN',
 'Skanuj RTSP w sieci domowej': 'Scansiona RTSP nella rete domestica',
 'Skanuj sieć lokalną przyciskiem zielonym. Zaznacz wykryte urządzenie i naciśnij żółty lub OK, aby dodać adres RTSP. Wpisz poprawną ścieżkę strumienia.': 'Premi '
                                                                                                                                                           'VERDE '
                                                                                                                                                           'per '
                                                                                                                                                           'scansionare '
                                                                                                                                                           'la '
                                                                                                                                                           'LAN. '
                                                                                                                                                           'Seleziona '
                                                                                                                                                           'un '
                                                                                                                                                           'dispositivo '
                                                                                                                                                           'e '
                                                                                                                                                           'premi '
                                                                                                                                                           'GIALLO '
                                                                                                                                                           'o '
                                                                                                                                                           'OK '
                                                                                                                                                           'per '
                                                                                                                                                           'aggiungere '
                                                                                                                                                           'il '
                                                                                                                                                           'suo '
                                                                                                                                                           'URL '
                                                                                                                                                           'RTSP. '
                                                                                                                                                           'Inserisci '
                                                                                                                                                           'il '
                                                                                                                                                           'percorso '
                                                                                                                                                           'dello '
                                                                                                                                                           'stream '
                                                                                                                                                           'corretto.',
 'Sprawdzam aktualizacje...': 'Verifica aggiornamenti in corso...',
 'Sprawdź aktualizacje': 'Verifica aggiornamenti',
 'Sprobuj FFmpeg relay — eksperymentalne': 'Prova relay FFmpeg — sperimentale',
 'Sterowanie PTZ': 'Controlli PTZ',
 'Strumien pomocniczy (opcjonalnie)': 'URL substream (opzionale)',
 'TAK': 'SÌ',
 'Test dotyczy RTSP': 'Questo test supporta solo RTSP',
 'Test serwera RTSP...': 'Test del server RTSP...',
 'Trwa poprzednia operacja': "Un'altra operazione è in corso",
 'Tuner nie obsluguje PiP': 'Questo ricevitore non supporta il PiP',
 'Usunac kamere %s?': 'Eliminare la telecamera %s?',
 'Usuń': 'Elimina',
 'Utworzono osobny bukiet: ': 'Creato un bouquet separato: ',
 'WYBRANA KAMERA\n\n%s\n\n%s\n\nJPEG: %s\n\nONVIF PTZ: %s\n\n0 Domofon\n1 Otworz domofon\n2 Bukiet / 3 M3U\n6 Test RTSP\n7 Sciana / 8 Patrol': 'TELECAMERA '
                                                                                                                                               'SELEZIONATA\n'
                                                                                                                                               '\n'
                                                                                                                                               '%s\n'
                                                                                                                                               '\n'
                                                                                                                                               '%s\n'
                                                                                                                                               '\n'
                                                                                                                                               'JPEG: '
                                                                                                                                               '%s\n'
                                                                                                                                               '\n'
                                                                                                                                               'ONVIF '
                                                                                                                                               'PTZ: '
                                                                                                                                               '%s\n'
                                                                                                                                               '\n'
                                                                                                                                               '0 '
                                                                                                                                               'Imposta '
                                                                                                                                               'citofono\n'
                                                                                                                                               '1 '
                                                                                                                                               'Apri '
                                                                                                                                               'citofono\n'
                                                                                                                                               '2 '
                                                                                                                                               'Bouquet '
                                                                                                                                               '/ '
                                                                                                                                               '3 '
                                                                                                                                               'M3U\n'
                                                                                                                                               '6 '
                                                                                                                                               'Test '
                                                                                                                                               'RTSP\n'
                                                                                                                                               '7 '
                                                                                                                                               'Muro '
                                                                                                                                               '/ '
                                                                                                                                               '8 '
                                                                                                                                               'Pattuglia',
 'Wybierz profil ONVIF': 'Seleziona profilo ONVIF',
 'Wykrywanie prawdziwych odpowiedzi RTSP.\nWpisz sciezke obrazu po znalezieniu serwera.\nNie kazdy otwarty port jest kamera.': 'Rilevamento '
                                                                                                                               'di '
                                                                                                                               'risposte '
                                                                                                                               'RTSP '
                                                                                                                               'reali.\n'
                                                                                                                               'Inserisci '
                                                                                                                               'il '
                                                                                                                               'percorso '
                                                                                                                               'dello '
                                                                                                                               'stream '
                                                                                                                               'dopo '
                                                                                                                               'aver '
                                                                                                                               'trovato '
                                                                                                                               'un '
                                                                                                                               'server.\n'
                                                                                                                               'Non '
                                                                                                                               'ogni '
                                                                                                                               'porta '
                                                                                                                               'aperta '
                                                                                                                               'è '
                                                                                                                               'una '
                                                                                                                               'telecamera.',
 'ZIELONY: skanuj prywatna siec /24': 'VERDE: scansiona una subnet privata /24',
 'Zamknieto PiP OpenCamView': 'PiP di OpenCamView chiuso',
 'Zamknij': 'Chiudi',
 'Zamknij PiP': 'Chiudi PiP',
 'Zapisano ustawienia kamery': 'Impostazioni telecamera salvate',
 'Zaznacz kamere i wcisnij 0 aby przypisac domofon': 'Seleziona una telecamera e premi 0 per impostarla come '
                                                     'citofono',
 'Zla sciezka': 'Percorso non valido',
 'Zle ustawienia': 'Impostazioni non valide',
 'Zly format kopii': 'Formato backup non valido',
 'Zmieniono język OpenCamView.': 'Lingua di OpenCamView cambiata.',
 'Znaleziono %d serwerow': 'Trovati %d server',
 '[ukryty adres]': '[URL nascosto]',
 'Kamery IP / RTSP / ONVIF': 'Telecamere IP / RTSP / ONVIF'}

SUPPORTED = ('system', 'pl', 'en', 'it', 'de', 'ar', 'ru')
TRANSLATIONS = {'en': EN, 'it': IT, 'de': DE, 'ar': AR, 'ru': RU}
MODE = 'system'


def set_language(mode):
    global MODE
    if mode not in SUPPORTED:
        raise ValueError('Unsupported language')
    MODE = mode


def get_language():
    if MODE != 'system':
        return MODE
    try:
        from Components.Language import language
        system_code = str(language.getLanguage()).lower().replace('-', '_')
        prefix = system_code.split('_', 1)[0]
        return prefix if prefix in TRANSLATIONS or prefix == 'pl' else 'en'
    except (ImportError, AttributeError, TypeError):
        return 'pl'


def tr(value):
    language = get_language()
    if language == 'pl':
        return value
    return TRANSLATIONS.get(language, EN).get(value, EN.get(value, value))
