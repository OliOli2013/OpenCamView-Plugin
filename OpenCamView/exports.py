from .i18n import tr
import os,tempfile
from urllib.parse import quote
BASE='/etc/enigma2'
def atomic_text(path,text):
    fd,tmp=tempfile.mkstemp(prefix='.ocv-',dir=os.path.dirname(path))
    try:
        os.fchmod(fd,0o600)
        with os.fdopen(fd,'w',encoding='utf-8') as f:f.write(text)
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
def clean(s):return s.replace('\n',' ').replace('\r',' ')[:80]
def m3u(cams,base=BASE):
    if not cams:raise ValueError(tr('Brak kamer'))
    path=os.path.join(base,'opencamview_cameras.m3u')
    atomic_text(path,'#EXTM3U\n'+''.join('#EXTINF:-1,%s\n%s\n'%(clean(c['name']),c['url']) for c in cams))
    return path
def bouquet(cams,base=BASE):
    if not cams:raise ValueError(tr('Brak kamer'))
    path=os.path.join(base,'userbouquet.opencamview.tv')
    atomic_text(path,'#NAME OpenCamView\n'+''.join('#SERVICE 4097:0:1:0:0:0:0:0:0:0:%s\n#DESCRIPTION %s\n'%(quote(c['url'],safe='/'),clean(c['name'])) for c in cams))
    registry=os.path.join(base,'bouquets.tv')
    if os.path.isfile(registry):
        with open(registry,encoding='utf-8') as f:
            text=f.read()
    else:
        text='#NAME Bouquets (TV)\n'
    row='#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.opencamview.tv" ORDER BY bouquet'
    if row not in text.splitlines():atomic_text(registry,text.rstrip('\n')+'\n'+row+'\n')
    return path
