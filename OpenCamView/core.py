# -*- coding: utf-8 -*-
from .i18n import tr
"""Portable camera database: v1.3 migration, stable IDs, backup, atomic writes."""
import copy, json, os, tempfile, uuid
from urllib.parse import urlsplit, urlunsplit, quote
DB='/etc/enigma2/opencamview.json'
SETTINGS='/etc/enigma2/opencamview_settings.json'

def valid(url, optional=False):
    url=(url or '').strip()
    if optional and not url:return ''
    if len(url)>2048 or any(ord(c)<32 for c in url):raise ValueError(tr('Nieprawidlowy adres'))
    try:
        p=urlsplit(url)
        if p.scheme.lower() not in ('rtsp','rtsps','http','https') or not p.hostname or p.hostname=='0.0.0.0':raise ValueError(tr('Protokol/host'))
        if p.port and not (0<p.port<65536):raise ValueError(tr('Port'))
    except ValueError as ex:raise ValueError(tr('Nieprawidlowy URL: %s')%ex)
    return url

def credentials(url,user,password):
    p=urlsplit(valid(url));host=p.hostname
    if ':' in host:host='[%s]'%host
    if p.port:host+=':%s'%p.port
    if user:host='%s:%s@%s'%(quote(user,safe=''),quote(password,safe=''),host)
    return urlunsplit((p.scheme,host,p.path,p.query,p.fragment))

def masked(url):
    try:
        p=urlsplit(url)
        if not p.username:return url
        h=p.hostname
        if ':' in h:h='['+h+']'
        if p.port:h+=':'+str(p.port)
        return urlunsplit((p.scheme,'***@'+h,p.path,p.query,''))
    except Exception:return tr('[ukryty adres]')

def camera(name,url,**fields):
    name=str(name or '').strip().replace('\r',' ').replace('\n',' ')
    if not name or len(name)>90:raise ValueError(tr('Nazwa kamery musi miec 1-90 znakow'))
    uid=fields.get('id') or uuid.uuid4().hex
    if len(uid)!=32 or any(c not in '0123456789abcdef' for c in uid):raise ValueError(tr('Nieprawidlowe ID'))
    return {'id':uid,'name':name,'url':valid(url),
            'snapshot':valid(fields.get('snapshot') or fields.get('snapshot_url'),True),
            'substream':valid(fields.get('substream') or fields.get('substream_url'),True),
            'onvif':valid(fields.get('onvif') or fields.get('onvif_url'),True),
            'token':str(fields.get('token') or fields.get('onvif_token') or '')[:128],
            'favorite':bool(fields.get('favorite',False))}

def read(path):
    if not os.path.exists(path):return None
    if os.path.islink(path) or os.stat(path).st_size>2097152:raise ValueError(tr('Nieprawidlowy plik konfiguracji'))
    with open(path,encoding='utf-8') as f:return json.load(f)

def atomic(path,data,backup=True):
    parent=os.path.dirname(path)
    os.makedirs(parent,exist_ok=True)
    blob=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()
    if len(blob)>2097152:raise ValueError(tr('Konfiguracja zbyt duza'))
    fd,tmp=tempfile.mkstemp(prefix='.ocv-',dir=parent)
    try:
        os.fchmod(fd,0o600)
        with os.fdopen(fd,'wb') as f:f.write(blob);f.flush();os.fsync(f.fileno())
        if backup and os.path.isfile(path) and not os.path.islink(path):
            with open(path,'rb') as f:older=f.read(2097153)
            if len(older)<=2097152:
                bfd,btmp=tempfile.mkstemp(prefix='.ocv-backup-',dir=parent)
                try:
                    os.fchmod(bfd,0o600)
                    with os.fdopen(bfd,'wb') as f:f.write(older);f.flush();os.fsync(f.fileno())
                    os.replace(btmp,path+'.bak')
                finally:
                    if os.path.exists(btmp):os.unlink(btmp)
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

class Manager:
    def __init__(self,path=DB,settings=SETTINGS):
        self.path,self.settings=path,settings
        self.error=None
        for f in (path,settings):
            if os.path.isfile(f) and not os.path.islink(f):
                try:os.chmod(f,0o600)
                except OSError:pass
        try:self.cameras=self._parse(read(path))
        except Exception as e:self.error=str(e);self.cameras=[]

    def _parse(self,data):
        if data is None:return []
        rows=data['cameras'] if isinstance(data,dict) else data
        if not isinstance(rows,list) or len(rows)>500:raise ValueError(tr('Bledna lista kamer'))
        out=[camera(x['name'],x['url'],**{k:v for k,v in x.items() if k not in ('name','url')}) for x in rows]
        if len(set(x['id'] for x in out))!=len(out):raise ValueError(tr('Powtorzone ID'))
        return out

    def save(self):
        if self.error:raise IOError(tr('Baza uszkodzona: %s. Przywroc .bak!')%self.error)
        atomic(self.path,self.cameras)

    def add(self,name,url,**opts):
        c=camera(name,url,**opts)
        self.cameras.append(c)
        try:self.save()
        except Exception:self.cameras.pop();raise
        return c

    def edit(self,i,name,url,**opts):
        old=copy.deepcopy(self.cameras[i]);extra=dict(old,**opts)
        self.cameras[i]=camera(name,url,**{k:v for k,v in extra.items() if k not in ('name','url')})
        try:self.save()
        except Exception:self.cameras[i]=old;raise

    def setting(self):
        defaults={'intercom':None,'snapshot_interval':7,'language':'system'}
        v=read(self.settings)
        if v is None:return defaults
        if not isinstance(v,dict):raise ValueError(tr('Zle ustawienia'))
        defaults.update({k:v[k] for k in defaults if k in v})
        if not defaults['intercom'] and isinstance(v.get('domofon_index'),int):
            i=v['domofon_index']
            if 0<=i<len(self.cameras):defaults['intercom']=self.cameras[i]['id']
        return defaults

    def set_language(self, mode):
        if mode not in ('system','pl','en'):
            raise ValueError('Unsupported language')
        settings=self.setting()
        settings['language']=mode
        atomic(self.settings,settings)

    def set_intercom(self,uid):
        s=self.setting();s['intercom']=uid;atomic(self.settings,s)

    def intercom(self):
        uid=self.setting()['intercom']
        return next((c for c in self.cameras if c['id']==uid),None)

    def delete(self,i):
        s=self.setting()
        c=self.cameras[i]
        if s['intercom']==c['id']:s['intercom']=None
        del self.cameras[i]
        try:self.save();atomic(self.settings,s)
        except Exception:self.cameras.insert(i,c);self.save();raise

    def favorite(self,i):
        self.cameras[i]['favorite']=not self.cameras[i]['favorite']
        self.save()

    def backup(self,path='/etc/enigma2/opencamview-export.json'):
        if self.error:raise IOError(self.error)
        atomic(path,{'format':'ocv2','cameras':self.cameras,'settings':self.setting()})
        return path

    def restore(self,path='/etc/enigma2/opencamview-export.json'):
        if self.error:raise IOError(tr('Najpierw odzyskaj uszkodzona baze z .bak'))
        d=read(path)
        if not isinstance(d,dict) or d.get('format')!='ocv2':raise ValueError(tr('Zly format kopii'))
        if not isinstance(d.get('cameras'),list):raise ValueError(tr('Brak listy kamer w kopii'))
        cams=self._parse(d['cameras'])
        old=self.cameras;self.cameras=cams
        try:
            self.save()
            if isinstance(d.get('settings'),dict):atomic(self.settings,d['settings'])
        except Exception:self.cameras=old;self.save();raise
        return len(cams)

    def recover(self):
        backup=read(self.path+'.bak')
        if backup is None:raise ValueError(tr('Brak automatycznej kopii .bak'))
        parsed=self._parse(backup)
        atomic(self.path,parsed,False)
        self.cameras=parsed;self.error=None
        return len(parsed)
