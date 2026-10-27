# -*- coding: utf-8 -*-
"""OpenCamView Enigma2 front-end, TV-safe camera workflows."""
import os,threading,tempfile,shutil,time
from datetime import datetime
from urllib.parse import urlsplit,unquote
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap
from Components.VideoWindow import VideoWindow
from enigma import eServiceReference,eTimer,ePicLoad
from .core import Manager,masked,credentials
from . import VERSION,onvif,theme
from .i18n import tr,set_language,get_language
from .updates import check_update

# Wydanie - metadane widoczne w stopce kazdego ekranu.
RELEASE_DATE = "27.10.2026"
WEBSITE = "https://aio-iptv-projekt.pages.dev/"
CREDITS = "%s  |  %s  |  by: Paweł Pawełek" % (WEBSITE, RELEASE_DATE)
from .network import Scanner,probe,jpeg
from .exports import bouquet,m3u

def inform(session,txt,error=False):
    session.open(MessageBox,str(txt),MessageBox.TYPE_ERROR if error else MessageBox.TYPE_INFO,timeout=6)

class Job:
    def __init__(self,fn):
        self.done=False;self.result=None;self.error=None
        def run():
            try:self.result=fn()
            except Exception as e:self.error=str(e)
            finally:self.done=True
        self.thread=threading.Thread(target=run,daemon=True);self.thread.start()

def stop_pip(session):
    if not getattr(session,'ocv_pip_owned',False):return False
    try:
        p=getattr(session,'pip',None)
        if p:
            try:p.stopService()
            except Exception:pass
            p.hide()
            try:session.deleteDialog(p)
            except Exception:pass
    finally:
        session.pip=None;session.pipshown=False;session.ocv_pip_owned=False
        relay=getattr(session,'ocv_relay',None);session.ocv_relay=None
        if relay:relay.stop()
    return True

def start_pip(session,url,use_relay=False):
    from Components.SystemInfo import SystemInfo
    if getattr(session,'pipshown',False) or getattr(session,'pip',None):raise RuntimeError(tr('Inny PiP jest aktywny'))
    if not SystemInfo.get('PIPAvailable',False):raise RuntimeError(tr('Tuner nie obsluguje PiP'))
    relay=None;pip=None
    try:
        if use_relay:
            from .relay import Relay
            relay=Relay(url);url=relay.start()
        from Screens.PictureInPicture import PictureInPicture
        pip=session.instantiateDialog(PictureInPicture);pip.show()
        if not pip.playService(eServiceReference(4097,0,url)):
            raise RuntimeError(tr('Drugi dekoder odrzucil strumien'))
        session.pip=pip;session.pipshown=True;session.ocv_pip_owned=True;session.ocv_relay=relay
    except Exception:
        if pip:
            try:pip.stopService();pip.hide();session.deleteDialog(pip)
            except Exception:pass
        if relay:relay.stop()
        raise

class MainScreen(Screen):
    def __init__(self,session):
        self.skin=theme.main();Screen.__init__(self,session)
        self.manager=Manager();self.work=None;self.done_callback=None
        try:set_language(self.manager.setting().get('language','system'))
        except Exception:set_language('system')
        self.timer=eTimer();self.timer.callback.append(self.poll)
        self['header']=Label('OpenCamView     v%s'%VERSION);self['count']=Label('')
        self['menu']=MenuList([]);self['detail']=Label('');self['status']=Label(tr('Kamery IP w Twojej sieci domowej'))
        self['key_red']=Label(tr('Usuń'))
        self['key_green']=Label(tr('Dodaj'))
        self['key_yellow']=Label(tr('Edytuj'))
        self['key_blue']=Label(tr('Opcje / LAN'))
        self['footer']=Label(tr('OK: Odtwórz   INFO: JPEG na TV   5: Ulubione   9: PiP   MENU: Narzędzia   EXIT'))
        self['credits']=Label(CREDITS)
        self['actions']=ActionMap(['OkCancelActions','ColorActions','MenuActions','InfobarActions','NumberActions','DirectionActions','EPGSelectActions'],{
            'cancel':self.close,'ok':self.play,'green':self.add,'red':self.ask_delete,
            'yellow':self.edit,'blue':self.options,'menu':self.tools,'info':self.snapshot,'showEventInfo':self.snapshot,
            'up':self.up,'down':self.down,'0':self.intercom_set,'1':self.intercom_play,'2':self.export_bouquet,
            '3':self.export_m3u,'4':self.help,'5':self.favorite,'6':self.check_rtsp,'7':self.wall,'8':self.patrol,'9':self.pip},-1)
        self.onLayoutFinish.append(self.refresh);self.onClose.append(self.timer.stop)

    def refresh_language(self):
        self['status'].setText(tr('Kamery IP w Twojej sieci domowej'))
        for key,caption in [('key_red','Usuń'),('key_green','Dodaj'),('key_yellow','Edytuj'),('key_blue','Opcje / LAN')]:
            self[key].setText(tr(caption))
        self['footer'].setText(tr('OK: Odtwórz   INFO: JPEG na TV   5: Ulubione   9: PiP   MENU: Narzędzia   EXIT'))
        self.refresh(self.current()['id'] if self.current() else None)

    def language_menu(self):
        chosen=self.manager.setting().get('language','system')
        items=[('System / Auto','system'),('Polski','pl'),('English','en')]
        self.session.openWithCallback(self.language_chosen,ChoiceBox,
            title='Język / Language [%s]'%chosen,list=items)

    def language_chosen(self,choice):
        if not choice:return
        code=choice[1]
        try:
            self.manager.set_language(code)
            set_language(code)
            self.refresh_language()
            self.alert(tr('Zmieniono język OpenCamView.'))
        except Exception as e:self.alert(tr('Błąd zmiany języka: ')+str(e),True)

    def updates_menu(self):
        self.run_job(tr('Sprawdzam aktualizacje...'),check_update,self.updates_result)

    def updates_result(self,info):
        from .i18n import get_language
        if info['newer']:
            if get_language()=='en':
                message='New version available: %s (installed: %s).\n%s\nInstall the update using the official OpenCamView installer from the project page.'%(info['latest'],info['installed'],info['notes']['en'])
            else:
                message='Dostępna nowa wersja: %s (zainstalowana: %s).\n%s\nAktualizację zainstaluj oficjalnym instalatorem OpenCamView ze strony projektu.'%(info['latest'],info['installed'],info['notes']['pl'])
        else:
            message=('You have the latest version: %s' if get_language()=='en' else 'Masz najnowszą wersję: %s')%info['installed']
        self.alert(message)

    def current_index(self):
        x=self['menu'].getCurrent()
        return x[1] if x and x[1]>=0 else None
    def current(self):
        i=self.current_index()
        return self.manager.cameras[i] if i is not None else None
    def up(self):self['menu'].up();self.detail()
    def down(self):self['menu'].down();self.detail()
    def refresh(self,uid=None):
        try:inter=self.manager.setting()['intercom']
        except Exception:inter=None
        items=[('%02d  %s%s%s'%(i+1,'★ ' if c['favorite'] else '',
                tr('DOMOFON ') if inter==c['id'] else '',c['name']),i) for i,c in enumerate(self.manager.cameras)]
        self['menu'].setList(items or [(tr('Brak kamer. ZIELONY = dodaj kamere'),-1)])
        if uid:
            for i,c in enumerate(self.manager.cameras):
                if c['id']==uid:self['menu'].moveToIndex(i);break
        self['count'].setText(tr('%d kamer')%len(self.manager.cameras));self.detail()
        if self.manager.error:self['status'].setText(tr('BLAD BAZY! MENU -> napraw z .bak: ')+self.manager.error[:75])
    def detail(self):
        c=self.current()
        if c:
            self['detail'].setText(tr('WYBRANA KAMERA\n\n%s\n\n%s\n\nJPEG: %s\n\nONVIF PTZ: %s\n\n0 Domofon\n1 Otworz domofon\n2 Bukiet / 3 M3U\n6 Test RTSP\n7 Sciana / 8 Patrol')%(c['name'],masked(c['url'])[:54],
                tr('TAK') if c['snapshot'] else tr('BRAK adresu'),tr('TAK') if c['token'] else tr('BRAK')))
        else:self['detail'].setText(tr('MONITORING DOMOWY\n\nKamery IP, RTSP i ONVIF\nPodglad bez list IPTV\n\nNIEBIESKI — skaner/ONVIF\nMENU — dodatkowe narzedzia'))
    def alert(self,txt,err=False):
        self['status'].setText(str(txt).replace('\n',' ')[:110]);inform(self.session,txt,err)
    def run_job(self,txt,fn,callback):
        if self.work and not self.work.done:return self.alert(tr('Trwa poprzednia operacja'))
        self['status'].setText(txt);self.done_callback=callback;self.work=Job(fn);self.timer.start(300,False)
    def poll(self):
        if not self.work or not self.work.done:return
        self.timer.stop();work=self.work;cb=self.done_callback;self.work=None;self.done_callback=None
        if work.error:self.alert(tr('Blad: ')+work.error,True)
        elif cb:
            try:cb(work.result)
            except Exception as e:self.alert(str(e),True)

    def wizard(self,c=None):
        self.editid=c['id'] if c else None
        self.fields=[('name',tr('Nazwa kamery')),('url',tr('Pelny adres RTSP/HTTP')),('snapshot',tr('Adres JPEG / snapshot (opcjonalnie)')),
                     ('substream',tr('Strumien pomocniczy (opcjonalnie)'))]
        self.form_values=dict(c) if c else {'name':'Kamera','url':'rtsp://192.168.1.100:554/stream1','snapshot':'','substream':''}
        self.wizard_step(0)
    def wizard_step(self,i):
        if i>=len(self.fields):
            try:
                d=self.form_values
                if self.editid:
                    idx=next(k for k,c in enumerate(self.manager.cameras) if c['id']==self.editid)
                    self.manager.edit(idx,d['name'],d['url'],snapshot=d['snapshot'],substream=d['substream'])
                    uid=self.editid
                else:uid=self.manager.add(d['name'],d['url'],snapshot=d['snapshot'],substream=d['substream'])['id']
                self.refresh(uid);self['status'].setText(tr('Zapisano ustawienia kamery'))
            except Exception as e:self.alert(tr('Blad zapisu: ')+str(e),True)
            return
        key,label=self.fields[i]
        self.session.openWithCallback(lambda ans,step=i,name=key:self.wizard_answer(step,name,ans),
              VirtualKeyBoard,title=label,text=self.form_values.get(key,''))
    def wizard_answer(self,i,key,ans):
        if ans is None:return
        self.form_values[key]=ans.strip();self.wizard_step(i+1)
    def add(self):self.wizard()
    def edit(self):
        if self.current():self.wizard(self.current())
    def ask_delete(self):
        if self.current():self.session.openWithCallback(self.delete,MessageBox,
                    tr('Usunac kamere %s?')%self.current()['name'],MessageBox.TYPE_YESNO)
    def delete(self,yes):
        if not yes:return
        try:self.manager.delete(self.current_index());self.refresh()
        except Exception as e:self.alert(str(e),True)
    def favorite(self):
        i=self.current_index()
        if i is None:return
        try:self.manager.favorite(i);self.refresh(self.manager.cameras[i]['id'])
        except Exception as e:self.alert(str(e),True)
    def intercom_set(self):
        if not self.current():return
        try:self.manager.set_intercom(self.current()['id']);self.refresh(self.current()['id'])
        except Exception as e:self.alert(str(e),True)
    def intercom_play(self):
        try:c=self.manager.intercom()
        except Exception as e:return self.alert(str(e),True)
        if c:self.session.open(Player,c)
        else:self.alert(tr('Zaznacz kamere i wcisnij 0 aby przypisac domofon'))
    def play(self):
        if self.current():self.session.open(Player,self.current())
    def show_again(self,*a):self.show();self.detail()
    def snapshot(self):
        c=self.current()
        if not c:return
        if not c['snapshot']:return self.alert(tr('Dodaj adres snapshot JPEG w edycji kamery'))
        self.hide();self.session.openWithCallback(self.show_again,Snapshot,[c],'overlay')
    def wall(self):
        cams=[c for c in self.manager.cameras if c['snapshot']]
        if not cams:return self.alert(tr('Brak kamer z adresem JPEG'))
        self.hide();self.session.openWithCallback(self.show_again,Snapshot,cams[:4],'wall')
    def patrol(self):
        cams=[c for c in self.manager.cameras if c['snapshot']]
        if not cams:return self.alert(tr('Dodaj adresy zdjec JPEG'))
        self.hide();self.session.openWithCallback(self.show_again,Snapshot,cams,'patrol')
    def pip(self):
        if stop_pip(self.session):return self.alert(tr('Zamknieto PiP OpenCamView'))
        c=self.current()
        if not c:return
        try:start_pip(self.session,c['substream'] or c['url']);self.close()
        except Exception as e:self.session.openWithCallback(lambda choice,cam=c:self.pip_fallback(choice,cam),ChoiceBox,
             title=tr('PiP niedostepne: %s')%str(e)[:90],list=[(tr('Podglad JPEG na TV'),'jpeg'),
             (tr('Sprobuj FFmpeg relay — eksperymentalne'),'relay'),(tr('Anuluj'),'cancel')])
    def pip_fallback(self,choice,c):
        if not choice:return
        if choice[1]=='jpeg':
            if c['snapshot']:self.hide();self.session.openWithCallback(self.show_again,Snapshot,[c],'overlay')
            else:self.alert(tr('Brak adresu JPEG kamery'))
        elif choice[1]=='relay':
            try:start_pip(self.session,c['substream'] or c['url'],True);self.close()
            except Exception as e:self.alert(str(e),True)

    def check_rtsp(self):
        c=self.current()
        if not c:return
        p=urlsplit(c['url'])
        if p.scheme not in ('rtsp','rtsps'):return self.alert(tr('Test dotyczy RTSP'))
        self.run_job(tr('Test serwera RTSP...'),lambda:probe(p.hostname,p.port or 554,3),
          lambda answer:self.alert(answer if answer else tr('Brak odpowiedzi RTSP'),not bool(answer)))
    def export_bouquet(self):
        try:
            path=bouquet(self.manager.cameras)
            try:
                from enigma import eDVBDB
                eDVBDB.getInstance().reloadBouquets()
            except Exception:pass
            self.alert(tr('Utworzono osobny bukiet: ')+path)
        except Exception as e:self.alert(str(e),True)
    def export_m3u(self):
        if not self.manager.cameras:return self.alert(tr('Brak kamer'))
        self.session.openWithCallback(self.m3u_confirm,MessageBox,tr('M3U moze zawierac hasla RTSP. Kontynuowac?'),MessageBox.TYPE_YESNO)
    def m3u_confirm(self,yes):
        if yes:
            try:self.alert(m3u(self.manager.cameras))
            except Exception as e:self.alert(str(e),True)
    def options(self):
        self.session.openWithCallback(self.option,ChoiceBox,title=tr('OpenCamView — funkcje'),list=[
            (tr('Skanuj RTSP w sieci domowej'),'scan'),(tr('Dodaj kamere ONVIF'),'onvif'),(tr('JPEG na TV'),'snap'),
            (tr('PiP kamery'),'pip'),(tr('Sciana 4 kamer'),'wall'),(tr('Patrol kamer'),'patrol'),(tr('Zamknij PiP'),'closepip')])
    def option(self,choice):
        if not choice:return
        key=choice[1]
        {'scan':self.scan,'onvif':self.onvif_wizard,'snap':self.snapshot,'pip':self.pip,
         'wall':self.wall,'patrol':self.patrol,'closepip':lambda:self.alert(tr('PiP zamkniety') if stop_pip(self.session) else tr('Brak naszego PiP'))}[key]()
    def scan(self):self.session.openWithCallback(self.refresh,ScanScreen,self.manager)
    def onvif_wizard(self):
        self.ovfields=[('host',tr('IP kamery ONVIF'),'192.168.1.100'),('port',tr('Port ONVIF'),'80'),
                       ('user',tr('Login ONVIF'),'admin'),('pwd',tr('Haslo ONVIF'),'')]
        self.ov={};self.onvif_step(0)
    def onvif_step(self,i):
        if i==len(self.ovfields):
            d=self.ov
            self.run_job(tr('Pobieram profile ONVIF...'),lambda:onvif.discover(d['host'],int(d['port']),d['user'],d['pwd']),self.onvif_results)
            return
        key,label,default=self.ovfields[i]
        self.session.openWithCallback(lambda x,k=key,n=i:self.onvif_answer(x,k,n),VirtualKeyBoard,title=label,text=default)
    def onvif_answer(self,answer,key,i):
        if answer is None:return
        self.ov[key]=answer.strip();self.onvif_step(i+1)
    def onvif_results(self,rows):
        self.session.openWithCallback(self.onvif_choice,ChoiceBox,title=tr('Wybierz profil ONVIF'),
            list=[('%s  %s'%(x['name'],masked(x['url'])[:52]),x) for x in rows])
    def onvif_choice(self,choice):
        if not choice:return
        x=choice[1]
        try:
            c=self.manager.add('ONVIF '+x['name'],x['url'],snapshot=x['snapshot'],onvif=x['onvif'],token=x['token'])
            self.refresh(c['id']);self.alert(tr('Dodano profil ONVIF'))
        except Exception as e:self.alert(str(e),True)
    def tools(self):
        self.session.openWithCallback(self.tool_choice,ChoiceBox,title=tr('Narzedzia OpenCamView'),list=[
           (tr('Kopia ustawien (z haslami!)'),'backup'),(tr('Przywroc kopie reczna'),'restore'),
           (tr('Napraw baze z automatycznej .bak'),'recover'),(tr('Eksport bukietu'),'bouquet'),
           (tr('Eksport M3U'),'m3u'),('Język / Language','language'),(tr('Sprawdź aktualizacje'),'updates'),(tr('Pomoc'),'help')])
    def tool_choice(self,choice):
        if not choice:return
        op=choice[1]
        if op in ('restore','recover'):
            self.session.openWithCallback(lambda yes,key=op:self.restore_confirm(yes,key),MessageBox,
               tr('Operacja zastapi obecna liste kamer. Kontynuowac?'),MessageBox.TYPE_YESNO)
        elif op=='backup':
            try:self.alert(tr('Kopia z haslami: ')+self.manager.backup())
            except Exception as e:self.alert(str(e),True)
        else:{'bouquet':self.export_bouquet,'m3u':self.export_m3u,
              'language':self.language_menu,'updates':self.updates_menu,'help':self.help}[op]()
    def restore_confirm(self,yes,key):
        if not yes:return
        try:n=self.manager.recover() if key=='recover' else self.manager.restore();self.refresh();self.alert(tr('Przywrocono %d kamer')%n)
        except Exception as e:self.alert(str(e),True)
    def help(self):self.alert('OpenCamView %s' % VERSION + tr('\nOK: strumien kamery\nINFO: JPEG na TV bez zmiany kanalu\n'
        '9: PiP — tylko wspierane tunery\n0/1: domofon, 5: ulubione, 6: test RTSP\n7: sciana, 8: patrol\n'
        'NIEBIESKI: skan LAN i ONVIF\nMENU: kopia, odzyskiwanie, eksport'))

class ScanScreen(Screen):
    def __init__(self,session,manager):
        self.skin=theme.main();Screen.__init__(self,session)
        self.manager=manager;self.scanner=Scanner();self.timer=eTimer();self.timer.callback.append(self.tick)
        self['header']=Label(tr('OpenCamView — skaner RTSP LAN'));self['count']=Label('')
        self['menu']=MenuList([]);self['detail']=Label(tr('Wykrywanie prawdziwych odpowiedzi RTSP.\nWpisz sciezke obrazu po znalezieniu serwera.\nNie kazdy otwarty port jest kamera.'))
        self['status']=Label(tr('ZIELONY: skanuj prywatna siec /24'))
        self['key_red']=Label(tr('Zamknij'))
        self['key_green']=Label(tr('Skanuj LAN'))
        self['key_yellow']=Label(tr('Dodaj IP'))
        self['key_blue']=Label(tr('Pomoc'))
        self['footer']=Label(tr('OK: Dodaj kamerę   EXIT: Powrót   Skaner nie odgaduje hasła ani ścieżki RTSP'))
        self['credits']=Label(CREDITS)
        self['actions']=ActionMap(['OkCancelActions','ColorActions','DirectionActions'],{
            'cancel':self.finish,'red':self.finish,'green':self.start,'yellow':self.add,'blue':self.help,'ok':self.add,
            'up':self.up,'down':self.down},-1)
        self.onClose.append(self.stop)
    def up(self):self['menu'].up()
    def down(self):self['menu'].down()
    def help(self):inform(self.session,tr('Skanuj sieć lokalną przyciskiem zielonym. Zaznacz wykryte urządzenie i naciśnij żółty lub OK, aby dodać adres RTSP. Wpisz poprawną ścieżkę strumienia.'))
    def start(self):self.scanner.start();self.timer.start(450,False);self['status'].setText(tr('Skanowanie RTSP...'))
    def tick(self):
        x=self.scanner.snapshot()
        self['menu'].setList([('%s:%d %s'%(c['ip'],c['port'],c['status']),c) for c in x])
        self['count'].setText('%d RTSP'%len(x))
        if not self.scanner.running:
            self.timer.stop();self['status'].setText(self.scanner.error or (tr('Znaleziono %d serwerow')%len(x)))
    def add(self):
        c=self['menu'].getCurrent()
        if not c:return
        self.session.openWithCallback(lambda ans,x=c[1]:self.add_path(x,ans),VirtualKeyBoard,
            title=tr('Rzeczywista sciezka RTSP (np. /Streaming/Channels/101)'),text='/Streaming/Channels/101')
    def add_path(self,x,path):
        if path is None:return
        if not path.startswith('/') or any(ord(c)<32 for c in path):return inform(self.session,tr('Zla sciezka'),True)
        try:self.manager.add(tr('Kamera ')+x['ip'],'rtsp://%s:%d%s'%(x['ip'],x['port'],path));inform(self.session,tr('Dodano; edytuj URL aby dopisac login i haslo'))
        except Exception as e:inform(self.session,str(e),True)
    def stop(self):self.timer.stop();self.scanner.stop()
    def finish(self):self.stop();self.close()

class Player(Screen):
    def __init__(self,session,cam):
        self.skin=theme.video();Screen.__init__(self,session)
        self.cam=cam;self.previous=None;self.ownref=None
        self['video']=VideoWindow(decoder=0)
        self['info']=Label(tr('%s   |   OK/EXIT: powrót do TV')%cam['name'])
        self['key_red']=Label(tr('Zamknij'))
        self['credits']=Label(CREDITS)
        self['actions']=ActionMap(['OkCancelActions','ColorActions'],{'cancel':self.close,'ok':self.close,'red':self.close},-1)
        self.onLayoutFinish.append(self.start);self.onClose.append(self.restore)
    def start(self):
        try:
            self.previous=self.session.nav.getCurrentlyPlayingServiceReference()
            self.ownref=eServiceReference(4097,0,self.cam['url'])
            self.session.nav.playService(self.ownref)
        except Exception as e:inform(self.session,str(e),True)
    def restore(self):
        try:
            cur=self.session.nav.getCurrentlyPlayingServiceReference()
            if self.ownref and cur and self.ownref.toString()==cur.toString():
                if self.previous:self.session.nav.playService(self.previous)
                else:self.session.nav.stopService()
        except Exception:pass

class Snapshot(Screen):
    def __init__(self,session,cameras,mode='overlay'):
        self.mode=mode;self.cams=cameras;self.idx=0;self.n=4 if mode=='wall' else 1
        self.skin=theme.overlay(self.n);Screen.__init__(self,session)
        self['status']=Label(tr('JPEG: odświeżanie co kilka sekund | CH +/-: patrol'))
        self['key_red']=Label(tr('Zamknij'))
        self['key_blue']=Label(tr('PTZ / ONVIF'))
        self['credits']=Label(CREDITS)
        self.decoders=[];self.jobs={};self.decoding=set();self.closed=False
        self.dir=tempfile.mkdtemp(prefix='opencamview-',dir='/tmp')
        self.paths=[os.path.join(self.dir,'snapshot-%d.jpg'%i) for i in range(self.n)]
        for i in range(self.n):
            self['pic%d'%i]=Pixmap();self['name%d'%i]=Label('')
            loader=ePicLoad();loader.PictureData.get().append(lambda *args,i=i:self.decoded(i));self.decoders.append(loader)
        try:self.interval=max(4,min(60,int(Manager().setting()['snapshot_interval'])))
        except Exception:self.interval=7
        self.last=0;self.ptz_job=None;self.timer=eTimer();self.timer.callback.append(self.tick)
        self['actions']=ActionMap(['OkCancelActions','ColorActions','ChannelSelectBaseActions'],{
            'cancel':self.close,'ok':self.close,'red':self.close,'blue':self.ptz_options,
            'channelUp':self.next,'channelDown':self.previous},-1)
        self.onLayoutFinish.append(self.start);self.onClose.append(self.finish)
    def active(self):return self.cams[:4] if self.mode=='wall' else [self.cams[self.idx]]
    def start(self):
        for i,loader in enumerate(self.decoders):
            size=self['pic%d'%i].instance.size()
            loader.setPara((size.width(),size.height(),1,1,False,1,'#00000000'))
        self.timer.start(400,False);self.load()
    def load(self):
        if self.closed:return
        self.last=time.monotonic()
        for i,c in enumerate(self.active()):
            self['pic%d'%i].hide();self['name%d'%i].setText(c['name']+tr(' — pobieranie JPEG'))
            self.jobs[i]=Job(lambda url=c['snapshot'],path=self.paths[i]:jpeg(url,path))
    def tick(self):
        if self.closed:return
        for i,job in list(self.jobs.items()):
            if not job.done:continue
            del self.jobs[i]
            if job.error:self['pic%d'%i].hide();self['name%d'%i].setText(tr('BLAD JPEG: ')+job.error[:45])
            else:
                self.decoding.add(i)
                try:self.decoders[i].startDecode(self.paths[i])
                except Exception as e:self.decoding.discard(i);self['name%d'%i].setText('JPEG: '+str(e)[:45])
        if self.ptz_job and self.ptz_job.done:
            self['status'].setText(tr('PTZ blad: ')+self.ptz_job.error if self.ptz_job.error else tr('PTZ — wykonano ruch'));self.ptz_job=None
        if not self.jobs and not self.decoding and time.monotonic()-self.last>=self.interval:
            if self.mode=='patrol':self.idx=(self.idx+1)%len(self.cams)
            self.load()
    def decoded(self,i):
        self.decoding.discard(i)
        if self.closed:return
        data=self.decoders[i].getData()
        if data:
            self['pic%d'%i].instance.setPixmap(data);self['pic%d'%i].show()
            self['name%d'%i].setText('%s   JPEG %s'%(self.active()[i]['name'],datetime.now().strftime('%H:%M:%S')))
        else:self['name%d'%i].setText(tr('Blad dekodowania JPEG'));self['pic%d'%i].hide()
    def next(self):
        if self.mode=='patrol' and not self.jobs:self.idx=(self.idx+1)%len(self.cams);self.load()
    def previous(self):
        if self.mode=='patrol' and not self.jobs:self.idx=(self.idx-1)%len(self.cams);self.load()
    def ptz_options(self):
        c=self.active()[0]
        if not c['onvif'] or not c['token']:return inform(self.session,tr('Brak ONVIF/PTZ'))
        self.session.openWithCallback(self.ptz_action,ChoiceBox,title=tr('Sterowanie PTZ'),list=[
            (tr('Lewo'),(-.4,0,0)),(tr('Prawo'),(.4,0,0)),(tr('Gora'),(0,.4,0)),(tr('Dol'),(0,-.4,0)),
            ('Zoom +',(0,0,.4)),('Zoom -',(0,0,-.4))])
    def ptz_action(self,choice):
        if not choice:return
        if self.ptz_job and not self.ptz_job.done:return
        c=self.active()[0];p=urlsplit(c['onvif']);url=credentials(c['onvif'],'','')
        self.ptz_job=Job(lambda:onvif.ptz(url,c['token'],unquote(p.username or ''),unquote(p.password or ''),*choice[1]))
    def finish(self):
        self.closed=True;self.timer.stop()
        jobs=list(self.jobs.values());folder=self.dir
        def cleanup():
            for job in jobs:job.thread.join(timeout=7)
            shutil.rmtree(folder,ignore_errors=True)
        threading.Thread(target=cleanup,daemon=True).start()
