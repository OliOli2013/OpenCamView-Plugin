"""Simulated Enigma2 API smoke tests. Does not certify physical receiver."""
import sys,types,unittest,tempfile,os,xml.etree.ElementTree as ET

def module(name,**attrs):
 m=types.ModuleType(name)
 for k,v in attrs.items():setattr(m,k,v)
 sys.modules[name]=m
class S:
 def width(self):return 1280
 def height(self):return 720
 def size(self):return self
class Screen(dict):
 def __init__(self,session):super().__init__();self.session=session;self.onClose=[];self.onLayoutFinish=[]
 def close(self):
  for fn in self.onClose:fn()
 def hide(self):
  # Prawdziwy Screens.Screen dziedziczy z dict i wywoluje self.values().
  # Tak odtwarzamy crash z OpenATV 8.0.1 przy otwarciu klawiatury.
  list(self.values())
 def show(self):list(self.values())
class Label:
 def __init__(self,t=''):self.text=t
 def setText(self,t):self.text=t
class MenuList:
 def __init__(self,rows):self.rows=rows;self.idx=0
 def setList(self,rows):self.rows=rows;self.idx=0
 def getCurrent(self):return self.rows[self.idx] if self.rows else None
 def up(self):self.idx=max(0,self.idx-1)
 def down(self):self.idx=min(len(self.rows)-1,self.idx+1)
 def moveToIndex(self,i):self.idx=i
class ActionMap:
 def __init__(self,contexts,actions,*args,**kwargs):self.contexts=contexts;self.actions=actions
class Box:TYPE_ERROR=3;TYPE_INFO=1;TYPE_YESNO=2
class Window:
 def __init__(self,*args,**kwargs):self.instance=self
 def size(self):return S()
 def hide(self):pass
 def show(self):pass
 def setPixmap(self,v):pass
class Timer:
 def __init__(self):self.callback=[]
 def start(self,*a):pass
 def stop(self):pass
class Picture:
 def __init__(self):self.PictureData=types.SimpleNamespace(get=lambda:[])
 def setPara(self,x):pass
 def startDecode(self,p):pass
 def getData(self):return None
class Ref:
 def __init__(self,*args):self.url=str(args[-1])
 def toString(self):return self.url
class PIP:
 accepted=True
 def __init__(self):self.stopped=False
 def show(self):pass
 def hide(self):pass
 def stopService(self):self.stopped=True
 def playService(self,ref):return self.accepted
module('Screens');module('Screens.Screen',Screen=Screen);module('Screens.MessageBox',MessageBox=Box)
module('Screens.ChoiceBox',ChoiceBox=object);module('Screens.VirtualKeyBoard',VirtualKeyBoard=object)
module('Screens.PictureInPicture',PictureInPicture=PIP)
module('Components');module('Components.ActionMap',ActionMap=ActionMap);module('Components.Label',Label=Label)
module('Components.MenuList',MenuList=MenuList);module('Components.Pixmap',Pixmap=Window)
module('Components.VideoWindow',VideoWindow=Window);module('Components.SystemInfo',SystemInfo={'PIPAvailable':True})
module('enigma',eServiceReference=Ref,eTimer=Timer,ePicLoad=Picture,getDesktop=lambda n:S())
from OpenCamView import ui,theme
class Nav:
 def __init__(self):self.current=Ref(1,0,'tv://before');self.stops=0
 def getCurrentlyPlayingServiceReference(self):return self.current
 def playService(self,x):self.current=x
 def stopService(self):self.stops+=1;self.current=None
class Session:
 def __init__(self):self.nav=Nav();self.pip=None;self.pipshown=False
 def open(self,*a,**kw):pass
 def openWithCallback(self,cb,*a,**kw):self.last_callback=cb;self.last_dialog=(a,kw)
 def instantiateDialog(self,cls):return cls()
 def deleteDialog(self,pip):pass

class GuiSmoke(unittest.TestCase):
 def test_wizard_does_not_shadow_screen_dict_values(self):
  s=Session();screen=ui.MainScreen(s)
  self.assertTrue(callable(screen.values))
  screen.add()  # zielony -> VirtualKeyBoard
  self.assertTrue(callable(screen.values))
  self.assertEqual(s.last_dialog[0][0],object)
  screen.hide()  # dokladna sciezka crasha w Screen.hide()
  self.assertEqual(screen.form_values['name'],'Kamera')
 def test_wizard_steps_allow_return_to_screen(self):
  with tempfile.TemporaryDirectory() as tmp:
   s=Session();screen=ui.MainScreen(s)
   screen.manager=ui.Manager(os.path.join(tmp,'cameras.json'),os.path.join(tmp,'settings.json'))
   screen.add()
   for answer in ('Wejscie', 'rtsp://192.168.1.2:554/live', '', ''):
    s.last_callback(answer)
    screen.hide()  # Enigma2 chowa ekran miedzy dialogami
   self.assertTrue(callable(screen.values))
   self.assertEqual(screen.form_values['name'],'Wejscie')
   self.assertEqual(len(screen.manager.cameras),1)
 def test_legend_bindings_and_credits(self):
  s=Session();screen=ui.MainScreen(s)
  self.assertEqual([screen['key_'+x].text for x in ('red','green','yellow','blue')],
                   ['Usuń','Dodaj','Edytuj','Opcje / LAN'])
  self.assertIn('Paweł Pawełek',screen['credits'].text)
  self.assertIn('aio-iptv-projekt.pages.dev',screen['credits'].text)
  for key,expected in [('red','ask_delete'),('green','add'),('yellow','edit'),('blue','options')]:
   self.assertEqual(screen['actions'].actions[key].__name__,expected)
  scan=ui.ScanScreen(s,screen.manager)
  self.assertEqual([scan['key_'+x].text for x in ('red','green','yellow','blue')],
                   ['Zamknij','Skanuj LAN','Dodaj IP','Pomoc'])
  for color in ('red','green','yellow','blue'):
   self.assertIn('key_'+color,ui.theme.main())
  for key,expected in [('red','finish'),('green','start'),('yellow','add'),('blue','help')]:
   self.assertEqual(scan['actions'].actions[key].__name__,expected)
 def test_skin_has_correct_buttons_each_screen(self):
  for skin,buttons in ((ui.theme.main(),{'key_red','key_green','key_yellow','key_blue'}),
                       (ui.theme.video(),{'key_red'}),
                       (ui.theme.overlay(1),{'key_red','key_blue'})):
   root=ET.fromstring(skin)
   self.assertTrue(buttons.issubset({node.attrib.get('name') for node in root.findall('widget')}))
   self.assertIn('credits',{node.attrib.get('name') for node in root.findall('widget')})
 def test_main_no_tv_stop(self):
  s=Session();screen=ui.MainScreen(s)
  for fn in screen.onLayoutFinish:fn()
  self.assertEqual(s.nav.stops,0)
 def test_owned_pip(self):
  s=Session();initial=s.nav.current
  ui.start_pip(s,'rtsp://10.0.0.1/stream')
  self.assertIs(initial,s.nav.current)
  self.assertTrue(s.ocv_pip_owned)
  obj=s.pip
  self.assertTrue(ui.stop_pip(s));self.assertTrue(obj.stopped)
 def test_foreign_pip_not_closed(self):
  s=Session();s.pip=PIP();s.pipshown=True
  self.assertFalse(ui.stop_pip(s));self.assertTrue(s.pipshown)
 def test_rejected_pip_falls_back(self):
  s=Session();PIP.accepted=False
  try:
   with self.assertRaises(RuntimeError):ui.start_pip(s,'rtsp://10.0.0.1/live')
  finally:PIP.accepted=True
 def test_player_restores_tv(self):
  s=Session();p=ui.Player(s,{'name':'Front','url':'rtsp://10.0.0.1/live'})
  p.start();p.restore();self.assertEqual(s.nav.current.toString(),'tv://before')
 def test_player_doesnt_override_changed_tv(self):
  s=Session();p=ui.Player(s,{'name':'Front','url':'rtsp://10.0.0.1/live'})
  p.start();s.nav.current=Ref(1,0,'tv://new');p.restore()
  self.assertEqual(s.nav.current.toString(),'tv://new')
 def test_skin_valid(self):
  for x in (theme.main(),theme.video(),theme.overlay(1),theme.overlay(4)):
   self.assertEqual(ET.fromstring(x).tag,'screen')
