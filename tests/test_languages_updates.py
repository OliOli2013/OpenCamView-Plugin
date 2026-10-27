"""PL/EN menu and read-only update checker: deterministic tests, no network calls."""
import io, os, json, tempfile, unittest
from unittest.mock import patch
from OpenCamView.i18n import tr, get_language, set_language
from OpenCamView import VERSION
from OpenCamView import updates
from OpenCamView.core import Manager
from OpenCamView import ui
from test_gui_stub import Session

class FakeResponse:
    def __init__(self,payload): self.payload=payload
    def __enter__(self): return self
    def __exit__(self,*a): pass
    def read(self,n): return self.payload[:n]

class LanguageTests(unittest.TestCase):
    def setUp(self): set_language('pl')
    def tearDown(self): set_language('pl')
    def test_lang_validated(self):
        with self.assertRaises(ValueError): set_language('fr')
        with self.assertRaises(ValueError): set_language('__class__')
    def test_translation_both_directions(self):
        self.assertEqual(tr('Dodaj'),'Dodaj')
        set_language('en')
        self.assertEqual(tr('Dodaj'),'Add')
        self.assertEqual(tr('Zamknij'),'Close')
        self.assertEqual(tr('Sprawdź aktualizacje'),'Check for updates')
        self.assertIn('snapshot',tr('Adres JPEG / snapshot (opcjonalnie)'))
        set_language('pl')
        self.assertEqual(tr('Dodaj'),'Dodaj')
    def test_auto_system_selects_english(self):
        import sys,types
        from unittest.mock import patch
        fake=types.SimpleNamespace(language=types.SimpleNamespace(getLanguage=lambda:'en_EN'))
        with patch.dict(sys.modules,{'Components.Language':fake}):
            set_language('system')
            self.assertEqual(get_language(),'en')
        set_language('pl')
    def test_settings_backward_compatible_and_persist(self):
        with tempfile.TemporaryDirectory() as tmp:
            m=Manager(tmp+'/c.json',tmp+'/s.json')
            c=m.add('Front','rtsp://10.0.0.2/live')
            m.set_intercom(c['id'])
            self.assertEqual(m.setting()['language'],'system')
            m.set_language('en')
            self.assertEqual(Manager(tmp+'/c.json',tmp+'/s.json').setting()['language'],'en')
            self.assertEqual(Manager(tmp+'/c.json',tmp+'/s.json').intercom()['name'],'Front')
            self.assertEqual(os.stat(tmp+'/s.json').st_mode & 0o777,0o600)
            m.set_language('pl')
            self.assertEqual(m.setting()['language'],'pl')
            with self.assertRaises(ValueError):m.set_language('fr')
    def test_menu_switch_to_english_immediately(self):
        with tempfile.TemporaryDirectory() as tmp:
            session=Session();screen=ui.MainScreen(session)
            screen.manager=Manager(tmp+'/c.json',tmp+'/s.json')
            screen.language_menu()
            self.assertTrue(any(value=='en' for _,value in session.last_dialog[1]['list']))
            session.last_callback(('English','en'))
            self.assertEqual(screen['key_green'].text,'Add')
            self.assertEqual(screen['key_red'].text,'Delete')
            self.assertIn('Favorites',screen['footer'].text)
            self.assertEqual(screen.manager.setting()['language'],'en')
            screen.add()
            self.assertEqual(session.last_dialog[1]['title'],'Camera name')
            screen.tools()
            options=session.last_dialog[1]['list']
            self.assertIn(('Check for updates','updates'),options)
            self.assertIn(('Język / Language','language'),options)
            screen.language_chosen(('Polski','pl'))
            self.assertEqual(screen['key_green'].text,'Dodaj')
    def test_update_menu_callback(self):
        session=Session();screen=ui.MainScreen(session)
        with patch.object(screen,'run_job') as run:
            screen.updates_menu()
            args=run.call_args.args
            self.assertIs(args[1],ui.check_update)

class UpdateTests(unittest.TestCase):
    def fake(self,content):
        if isinstance(content,dict):content=json.dumps(content).encode()
        return lambda request,timeout:FakeResponse(content)
    def test_manifest_is_repo_https(self):
        self.assertTrue(updates.MANIFEST_URL.startswith('https://raw.githubusercontent.com/OliOli2013/OpenCamView-Plugin/'))
    def test_equal(self):
        v=updates.check_update(self.fake({'version':VERSION,'notes':{'pl':'Aktualna'}}))
        self.assertFalse(v['newer']);self.assertEqual(v['installed'],VERSION)
    def test_newer(self):
        v=updates.check_update(self.fake({'version':'2.1.0','date':'2026-11-01','notes':{'en':'New features'}}))
        self.assertTrue(v['newer']);self.assertEqual(v['notes']['en'],'New features')
    def test_older(self):
        self.assertFalse(updates.check_update(self.fake({'version':'2.0.1'}))['newer'])
    def test_reject_malformed(self):
        for data in (b'bad json',b'[]',b'{}',b'{"version":"2.0.2;rm"}',b'{"version":"9999.1.1"}'):
            with self.assertRaises((ValueError,TypeError,KeyError)):
                updates.check_update(self.fake(data))
    def test_reject_oversize(self):
        with self.assertRaises(ValueError):updates.check_update(self.fake(b' '*9000))
    def test_disconnect(self):
        def offline(req,timeout):raise OSError('network unreachable')
        with self.assertRaises(OSError):updates.check_update(offline)
    def test_no_exec_or_auto_install(self):
        with patch('subprocess.run',side_effect=AssertionError('executed')),patch('os.system',side_effect=AssertionError('executed')):
            updates.check_update(self.fake({'version':'3.0.0','notes':{'en':'safe'}}))

if __name__=='__main__':unittest.main()
