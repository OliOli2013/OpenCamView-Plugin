# -*- coding: utf-8 -*-
"""Regression coverage for 2.0.3 six-language update and reinstall handling."""
import os
import re
import sys
import json
import tempfile
import subprocess
import unittest
import types
from pathlib import Path
from unittest.mock import patch
from test_gui_stub import Session  # installs Enigma2 stub modules before importing UI
from OpenCamView import VERSION
from OpenCamView import ui, updates
from OpenCamView.i18n import (EN, IT, SUPPORTED, TRANSLATIONS, set_language,
                               get_language, tr)
from OpenCamView.core import Manager
from OpenCamView.update_messages import format_update_info

ROOT = Path(__file__).resolve().parents[1]

class SixLanguages(unittest.TestCase):
    def tearDown(self):
        set_language('pl')

    def test_languages_including_system(self):
        self.assertEqual(SUPPORTED, ('system', 'pl', 'en', 'it', 'de', 'ar', 'ru'))
        self.assertEqual(VERSION, '2.0.3')

    def test_six_translations_complete(self):
        for lang, dictionary in TRANSLATIONS.items():
            with self.subTest(lang=lang):
                self.assertEqual(set(dictionary), set(EN))
                self.assertEqual(len(dictionary), len(EN))
                for key, phrase in dictionary.items():
                    self.assertIsInstance(phrase, str)
                    self.assertTrue(phrase.strip(), (lang, key))
                    self.assertEqual(re.findall(r'%(?:s|d)', key), re.findall(r'%(?:s|d)', phrase), (lang, key, phrase))

    def test_translated_core_buttons_and_formatting(self):
        for lang in ('pl', 'en', 'it', 'de', 'ar', 'ru'):
            with self.subTest(lang=lang):
                set_language(lang)
                self.assertTrue(tr('Dodaj'))
                self.assertTrue(tr('Usuń'))
                self.assertTrue(tr('Sprawdź aktualizacje'))
                self.assertIn('12', tr('%d kamer') % 12)
                self.assertIn('Front', tr('Usunac kamere %s?') % 'Front')
                self.assertIn('3', tr('Przywrocono %d kamer') % 3)
                self.assertTrue(tr('Kamery IP / RTSP / ONVIF'))

    def test_autodetect_all_six(self):
        for code in ('pl_PL', 'en_GB', 'it_IT', 'de_DE', 'ar_SA', 'ru_RU'):
            fake = types.SimpleNamespace(language=types.SimpleNamespace(getLanguage=lambda c=code: c))
            with patch.dict(sys.modules, {'Components.Language': fake}):
                set_language('system')
                self.assertEqual(get_language(), code.split('_')[0])
        with patch.dict(sys.modules, {'Components.Language':types.SimpleNamespace(language=types.SimpleNamespace(getLanguage=lambda:'fr_FR'))}):
            set_language('system')
            self.assertEqual(get_language(),'en')

    def test_persist_and_keep_cameras(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = Manager(tmp+'/c.json', tmp+'/s.json')
            c = m.add('Driveway', 'rtsp://192.168.1.3/cam')
            m.set_intercom(c['id'])
            for code in ('it','de','ar','ru','en','pl','system'):
                m.set_language(code)
                z = Manager(tmp+'/c.json', tmp+'/s.json')
                self.assertEqual(z.setting()['language'],code)
                self.assertEqual(z.intercom()['name'],'Driveway')
            self.assertEqual(os.stat(tmp+'/s.json').st_mode & 0o777, 0o600)
            with self.assertRaises(ValueError): m.set_language('es')

    def test_change_language_in_menu(self):
        with tempfile.TemporaryDirectory() as tmp:
            s=Session(); main=ui.MainScreen(s)
            main.manager=Manager(tmp+'/c.json', tmp+'/s.json')
            main.language_menu()
            options=dict((value,label) for label,value in s.last_dialog[1]['list'])
            self.assertEqual(set(options),set(SUPPORTED))
            for code in ('it','de','ar','ru','en','pl'):
                main.language_chosen((options[code],code))
                self.assertEqual(main['key_green'].text,tr('Dodaj'))
                self.assertEqual(main.manager.setting()['language'],code)

    def test_localized_update_messages(self):
        for lang in ('pl','en','it','de','ar','ru'):
            newer={'newer':True,'latest':'3.0.0','installed':'2.0.3','notes':{lang:'Message '+lang}}
            old={'newer':False,'latest':'2.0.3','installed':'2.0.3','notes':{}}
            s1=format_update_info(newer,lang)
            s2=format_update_info(old,lang)
            self.assertIn('3.0.0',s1)
            self.assertIn('2.0.3',s1)
            self.assertIn('Message '+lang,s1)
            self.assertIn('2.0.3',s2)
            self.assertNotEqual(s1,s2)
        self.assertIn('in English',format_update_info({'newer':True,'latest':'3.0.0','installed':'2.0.3','notes':{'en':'in English'}},'ar'))

    def test_manifest_six_notes(self):
        manifest=json.loads((ROOT/'version.json').read_text('utf-8'))
        self.assertEqual(manifest['version'], VERSION)
        self.assertEqual(set(manifest['notes']),set(SUPPORTED)-{'system'})
        for code in ('pl','en','it','de','ar','ru'):
            self.assertTrue(manifest['notes'][code])

    def test_manifest_parsed_six_notes(self):
        import io
        class Resp:
            def __enter__(self):return self
            def __exit__(self,*args):return False
            def read(self,n):return (ROOT/'version.json').read_bytes()[:n]
        v=updates.check_update(lambda *a,**k:Resp())
        self.assertEqual(set(v['notes']), set(SUPPORTED)-{'system'})
        self.assertFalse(v['newer'])

    def test_installer_skips_same_version_without_download(self):
        with tempfile.TemporaryDirectory() as tmp:
            opkg=Path(tmp)/'opkg'
            opkg.write_text('#!/bin/sh\nif [ "$1" = status ]; then echo "Package: enigma2-plugin-extensions-opencamview"; echo "Version: 2.0.3"; exit 0; fi\nexit 89\n')
            opkg.chmod(0o755)
            env=dict(os.environ,PATH=tmp+':'+os.environ['PATH'])
            res=subprocess.run(['/bin/sh',str(ROOT/'installer.sh')], env=env, capture_output=True, text=True, timeout=5)
            self.assertEqual(res.returncode,0, res.stderr)
            self.assertIn('already installed',res.stdout)

if __name__=='__main__':unittest.main()
