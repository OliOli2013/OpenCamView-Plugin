# -*- coding: utf-8 -*-
"""Localized update notices for six supported UI languages."""
UPDATE_NOTICES = {'pl': ('Dostępna nowa wersja: %s (zainstalowana: %s).\n%s\nZainstaluj aktualizację oficjalnym instalatorem OpenCamView.',
        'Masz najnowszą wersję: %s'),
 'en': ('New version available: %s (installed: %s).\n%s\nInstall the update using the official OpenCamView installer.',
        'You have the latest version: %s'),
 'it': ('Nuova versione disponibile: %s (installata: %s).\n%s\nInstalla l’aggiornamento con l’installer ufficiale di OpenCamView.',
        'Hai già la versione più recente: %s'),
 'de': ('Neue Version verfügbar: %s (installiert: %s).\n%s\nInstalliere das Update mit dem offiziellen OpenCamView-Installer.',
        'Du verwendest die neueste Version: %s'),
 'ru': ('Доступна новая версия: %s (установлена: %s).\n%s\nУстановите обновление с помощью официального установщика OpenCamView.',
        'Установлена последняя версия: %s'),
 'ar': ('يتوفر إصدار جديد: %s (المثبت: %s).\n%s\nثبّت التحديث باستخدام مُثبّت OpenCamView الرسمي.', 'لديك أحدث إصدار: %s')}


def format_update_info(info, code):
    templates = UPDATE_NOTICES.get(code, UPDATE_NOTICES['en'])
    if info['newer']:
        notes = info.get('notes', {})
        note = notes.get(code) or notes.get('en') or notes.get('pl') or ''
        return templates[0] % (info['latest'], info['installed'], note)
    return templates[1] % info['installed']
