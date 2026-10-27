"""Minimal standard-library ONVIF Media 1 + PTZ. SOAP WSSE digest."""
from .i18n import tr
import os,base64,hashlib,datetime,re,xml.etree.ElementTree as ET
from urllib.request import Request,build_opener,HTTPPasswordMgrWithDefaultRealm,HTTPDigestAuthHandler,HTTPBasicAuthHandler,HTTPRedirectHandler
from urllib.parse import urlsplit,urlunsplit
from xml.sax.saxutils import escape
from .core import valid,credentials
D='http://www.onvif.org/ver10/device/wsdl';M='http://www.onvif.org/ver10/media/wsdl';P='http://www.onvif.org/ver20/ptz/wsdl'

def find(root,key):return next((x for x in root.iter() if x.tag.rsplit('}',1)[-1]==key),None)
def findall(root,key):return [x for x in root.iter() if x.tag.rsplit('}',1)[-1]==key]
def esc(s):return escape(str(s),{'"':'&quot;',"'":'&apos;'})
def wsse(user,pwd):
    if not user:return ''
    n=os.urandom(16);created=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    digest=base64.b64encode(hashlib.sha1(n+created.encode()+pwd.encode()).digest()).decode()
    return ('<wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd"><wsse:UsernameToken><wsse:Username>%s</wsse:Username><wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">%s</wsse:Password><wsse:Nonce>%s</wsse:Nonce><wsu:Created>%s</wsu:Created></wsse:UsernameToken></wsse:Security>'%(esc(user),digest,base64.b64encode(n).decode(),created))
class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*a,**kw):return None

def soap(url,action,payload,user='',pwd=''):
    url=valid(url)
    xml=('<?xml version="1.0"?><s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:tds="%s" xmlns:trt="%s" xmlns:tptz="%s"><s:Header>%s</s:Header><s:Body>%s</s:Body></s:Envelope>'%(D,M,P,wsse(user,pwd),payload)).encode()
    pw=HTTPPasswordMgrWithDefaultRealm();pw.add_password(None,url,user,pwd)
    opener=build_opener(NoRedirect(),HTTPDigestAuthHandler(pw),HTTPBasicAuthHandler(pw))
    r=Request(url,data=xml,headers={'Content-Type':'application/soap+xml; charset=utf-8; action="%s"'%action})
    with opener.open(r,timeout=5) as response:data=response.read(524289)
    if len(data)>524288:raise ValueError('Odpowiedz ONVIF za duza')
    root=ET.fromstring(data)
    if find(root,'Fault') is not None:raise ValueError('ONVIF SOAP Fault')
    return root

def endpoint(url,host,protocols=('http','https')):
    p=urlsplit(url)
    if p.scheme not in protocols:raise ValueError(tr('Niedozwolony protokol'))
    if p.hostname in ('0.0.0.0','localhost','127.0.0.1'):
        net=host+((':%d'%p.port) if p.port else '')
        url=urlunsplit((p.scheme,net,p.path,p.query,p.fragment))
    elif p.hostname!=host:raise ValueError('ONVIF przekierowuje na inny host')
    return valid(url)

def discover(host,port,user,pwd):
    if not re.fullmatch(r'[A-Za-z0-9.:-]+',host) or not 0<int(port)<65536:raise ValueError(tr('Bledny host/port'))
    base='http://%s:%d/onvif/device_service'%(host,int(port))
    cap=soap(base,D+'/GetCapabilities','<tds:GetCapabilities><tds:Category>All</tds:Category></tds:GetCapabilities>',user,pwd)
    media=find(cap,'Media')
    if media is None or find(media,'XAddr') is None:raise ValueError(tr('Brak ONVIF Media'))
    media_url=endpoint(find(media,'XAddr').text.strip(),host)
    ptz=find(cap,'PTZ');ptzurl=endpoint(find(ptz,'XAddr').text.strip(),host) if ptz is not None and find(ptz,'XAddr') is not None else ''
    profiles=soap(media_url,M+'/GetProfiles','<trt:GetProfiles/>',user,pwd)
    items=[]
    for profile in findall(profiles,'Profiles')[:16]:
        token=profile.attrib.get('token')
        if not token:continue
        name=find(profile,'Name')
        body='<trt:GetStreamUri><trt:StreamSetup><tt:Stream xmlns:tt="http://www.onvif.org/ver10/schema">RTP-Unicast</tt:Stream><tt:Transport xmlns:tt="http://www.onvif.org/ver10/schema"><tt:Protocol>RTSP</tt:Protocol></tt:Transport></trt:StreamSetup><trt:ProfileToken>%s</trt:ProfileToken></trt:GetStreamUri>'%esc(token)
        try:
            r=soap(media_url,M+'/GetStreamUri',body,user,pwd);stream=find(r,'Uri')
            uri=endpoint(stream.text.strip(),host,('rtsp','rtsps'))
            snapshot=''
            try:
                sr=soap(media_url,M+'/GetSnapshotUri','<trt:GetSnapshotUri><trt:ProfileToken>%s</trt:ProfileToken></trt:GetSnapshotUri>'%esc(token),user,pwd)
                snap=find(sr,'Uri')
                if snap is not None and snap.text:snapshot=credentials(endpoint(snap.text.strip(),host),user,pwd)
            except Exception:pass
            items.append({'name':(name.text if name is not None else 'Camera')[:60],
                 'url':credentials(uri,user,pwd),'snapshot':snapshot,'onvif':credentials(ptzurl,user,pwd) if ptzurl else '',
                 'token':token})
        except Exception:continue
    if not items:raise ValueError(tr('Nie wykryto strumieni ONVIF'))
    return items

def ptz(url,token,username,password,x,y,z):
    if not token or any(abs(k)>1 for k in (x,y,z)):raise ValueError(tr('Nieprawidlowy PTZ'))
    body='<tptz:ContinuousMove><tptz:ProfileToken>%s</tptz:ProfileToken><tptz:Velocity><tt:PanTilt xmlns:tt="http://www.onvif.org/ver10/schema" x="%s" y="%s"/><tt:Zoom xmlns:tt="http://www.onvif.org/ver10/schema" x="%s"/></tptz:Velocity><tptz:Timeout>PT0.4S</tptz:Timeout></tptz:ContinuousMove>'%(esc(token),x,y,z)
    try:soap(url,P+'/ContinuousMove',body,username,password)
    finally:
        try:soap(url,P+'/Stop','<tptz:Stop><tptz:ProfileToken>%s</tptz:ProfileToken><tptz:PanTilt>true</tptz:PanTilt><tptz:Zoom>true</tptz:Zoom></tptz:Stop>'%esc(token),username,password)
        except Exception:pass
