import json,os,socket,tempfile,threading,time,unittest,xml.etree.ElementTree as ET
from http.server import HTTPServer,BaseHTTPRequestHandler
from unittest.mock import patch
from OpenCamView.core import Manager,camera,valid,masked,credentials
from OpenCamView.network import probe,jpeg,Scanner
from OpenCamView.exports import bouquet,m3u
from OpenCamView import onvif

class DBTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.db=self.t.name+'/cam.json';self.settings=self.t.name+'/settings.json'
        self.m=Manager(self.db,self.settings)
    def tearDown(self):self.t.cleanup()
    def a(self,n='A'):return self.m.add(n,'rtsp://10.0.0.2/live')
    def test_empty(self):self.assertEqual(self.m.cameras,[])
    def test_add_persist(self):
        a=self.a();self.assertEqual(Manager(self.db,self.settings).cameras[0]['id'],a['id'])
    def test_atomic_private(self):
        self.a();self.assertEqual(os.stat(self.db).st_mode&0o777,0o600)
    def test_backup_created(self):
        self.a();self.a('B');self.assertTrue(os.path.isfile(self.db+'.bak'))
    def test_corrupt_blocks_save(self):
        with open(self.db,'w') as f:f.write('{bad')
        m=Manager(self.db,self.settings)
        with self.assertRaises(IOError):m.add('B','rtsp://10.0.0.2/live')
        with open(self.db) as f:self.assertEqual(f.read(),'{bad')
    def test_migrate_v13(self):
        with open(self.db,'w') as f:json.dump([{'name':'Old','url':'rtsp://10.0.0.1/stream'}],f)
        self.assertEqual(Manager(self.db,self.settings).cameras[0]['name'],'Old')
    def test_intercom_not_shifted(self):
        self.a();b=self.a('B');self.m.set_intercom(b['id']);self.m.delete(0)
        self.assertEqual(self.m.intercom()['name'],'B')
    def test_removed_intercom_clears(self):
        a=self.a();self.m.set_intercom(a['id']);self.m.delete(0)
        self.assertIsNone(self.m.intercom())
    def test_edit_id_preserved(self):
        a=self.a();self.m.edit(0,'Z','rtsp://10.0.0.2/z')
        self.assertEqual(self.m.cameras[0]['id'],a['id'])
    def test_favorites(self):
        self.a();self.m.favorite(0);self.assertTrue(Manager(self.db,self.settings).cameras[0]['favorite'])
    def test_manual_backup_restore(self):
        self.a();p=self.m.backup(self.t.name+'/backup.json');self.a('B')
        self.assertEqual(self.m.restore(p),1)
    def test_recover(self):
        self.a();self.a('B')
        with open(self.db,'w') as f:f.write('broken')
        m=Manager(self.db,self.settings)
        self.assertEqual(m.recover(),1)
        self.assertEqual(Manager(self.db,self.settings).cameras[0]['name'],'A')
    def test_recover_missing_doesnt_erase(self):
        self.a()
        with self.assertRaises(ValueError):self.m.recover()
        self.assertEqual(len(Manager(self.db,self.settings).cameras),1)
    def test_restore_missing_cameras_refused(self):
        p=self.t.name+'/bad.json'
        with open(p,'w') as f:json.dump({'format':'ocv2'},f)
        with self.assertRaises(ValueError):self.m.restore(p)
    def test_old_domofon(self):
        self.a();b=self.a('B')
        with open(self.settings,'w') as f:json.dump({'domofon_index':1},f)
        self.assertEqual(self.m.intercom()['id'],b['id'])

class Validation(unittest.TestCase):
    def test_scheme_allowlist(self):
        for scheme in ('rtsp','rtsps','http','https'):self.assertTrue(valid(scheme+'://10.0.0.1/x'))
    def test_disallow_file(self):
        for url in ('ftp://a/b','file:///etc/passwd','http:///a',''):
            with self.assertRaises(ValueError):valid(url)
    def test_redact(self):self.assertNotIn('secret',masked('rtsp://admin:secret@10.0.0.1/live'))
    def test_credentials_escaped(self):self.assertIn('a%40b:p%2Fw@',credentials('rtsp://10.0.0.1/','a@b','p/w'))
    def test_duplicate_ids(self):
        with self.assertRaises(ValueError):camera('', 'rtsp://10.0.0.1/x')
    def test_bad_port(self):
        with self.assertRaises(ValueError):valid('rtsp://10.0.0.1:99999/a')

class Export(unittest.TestCase):
    def setUp(self):self.t=tempfile.TemporaryDirectory();self.c=[{'name':'Front','url':'rtsp://admin:pw@10.0.0.2/live'}]
    def tearDown(self):self.t.cleanup()
    def test_bouquet_dedup(self):
        bouquet(self.c,self.t.name);bouquet(self.c,self.t.name)
        with open(self.t.name+'/bouquets.tv') as f:self.assertEqual(f.read().count('opencamview.tv'),1)
    def test_export_m3u(self):
        path=m3u(self.c,self.t.name)
        with open(path) as f:self.assertIn('#EXTM3U',f.read())
        self.assertEqual(os.stat(path).st_mode&0o777,0o600)
    def test_export_no_camera(self):
        with self.assertRaises(ValueError):bouquet([],self.t.name)

class RTSPSim(unittest.TestCase):
    def serve(self,msg):
        s=socket.socket();s.bind(('127.0.0.1',0));s.listen(1);port=s.getsockname()[1]
        def accept():
            conn,_=s.accept();conn.recv(1024);conn.sendall(msg);conn.close();s.close()
        threading.Thread(target=accept,daemon=True).start();return port
    def test_options_401(self):self.assertIn('401',probe('127.0.0.1',self.serve(b'RTSP/1.0 401 Unauthorized\r\n'),1))
    def test_http_not_rtsp(self):self.assertIsNone(probe('127.0.0.1',self.serve(b'HTTP/1.1 200 OK\r\n'),1))
    def test_reject_public(self):
        scan=Scanner();scan.start('8.8.8.0/24')
        for _ in range(100):
            if not scan.running:break
            time.sleep(.01)
        self.assertTrue(scan.error)
    def test_reject_wide_subnet(self):
        scan=Scanner();scan.start('10.0.0.0/8')
        for _ in range(100):
            if not scan.running:break
            time.sleep(.01)
        self.assertTrue(scan.error)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data=b'\xff\xd8\xff\xe0TEST\xff\xd9' if self.path=='/ok' else b'not jpeg'
        self.send_response(200);self.end_headers();self.wfile.write(data)
    def log_message(self,*a):pass
class JPEGSim(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=HTTPServer(('127.0.0.1',0),Handler)
        threading.Thread(target=cls.s.serve_forever,daemon=True).start()
        cls.base='http://127.0.0.1:%d'%cls.s.server_address[1]
    @classmethod
    def tearDownClass(cls):cls.s.shutdown();cls.s.server_close()
    def setUp(self):self.t=tempfile.TemporaryDirectory();self.path=self.t.name+'/j.jpg'
    def tearDown(self):self.t.cleanup()
    def test_valid(self):
        jpeg(self.base+'/ok',self.path)
        with open(self.path,'rb') as f:self.assertTrue(f.read().startswith(b'\xff\xd8'))
    def test_no_invalid_save(self):
        with self.assertRaises(ValueError):jpeg(self.base+'/bad',self.path)
        self.assertFalse(os.path.exists(self.path))
    def test_private(self):
        jpeg(self.base+'/ok',self.path);self.assertEqual(os.stat(self.path).st_mode&0o777,0o600)

class OnvifSim(unittest.TestCase):
    def test_digest(self):
        x=onvif.wsse('admin','password');self.assertIn('UsernameToken',x)
        self.assertNotIn('>password<',x)
    def test_bad_host(self):
        with self.assertRaises(ValueError):onvif.endpoint('http://evil.example/api','10.0.0.2')
    def test_loopback_rewrite(self):
        self.assertEqual(onvif.endpoint('http://0.0.0.0:80/onvif','10.0.0.2'),'http://10.0.0.2:80/onvif')
    def test_ptz_stop(self):
        with patch('OpenCamView.onvif.soap',return_value=ET.fromstring('<body/>')) as call:
            onvif.ptz('http://10.0.0.2/ptz','t','a','b',.4,0,0)
        self.assertEqual(call.call_count,2)
    def test_ptz_stops_on_failure(self):
        with patch('OpenCamView.onvif.soap',side_effect=[OSError('fail'),ET.fromstring('<body/>')]) as call:
            with self.assertRaises(OSError):onvif.ptz('http://10.0.0.2/ptz','t','a','b',.4,0,0)
        self.assertEqual(call.call_count,2)
    def test_profile_discovery(self):
        cap=ET.fromstring('<root><Media><XAddr>http://10.0.0.2/onvif/media</XAddr></Media></root>')
        profiles=ET.fromstring('<root><Profiles token="t"><Name>main</Name></Profiles></root>')
        uri=ET.fromstring('<root><Uri>rtsp://10.0.0.2/live</Uri></root>')
        snap=ET.fromstring('<root><Uri>http://10.0.0.2/snapshot.jpg</Uri></root>')
        with patch('OpenCamView.onvif.soap',side_effect=[cap,profiles,uri,snap]):
            x=onvif.discover('10.0.0.2',80,'admin','secret')
        self.assertEqual(x[0]['token'],'t');self.assertIn('admin:secret@',x[0]['url'])
