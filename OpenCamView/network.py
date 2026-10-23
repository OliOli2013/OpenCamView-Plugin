import ipaddress, socket, threading, os, tempfile, time
from urllib.parse import urlsplit,unquote
from urllib.request import build_opener,HTTPPasswordMgrWithDefaultRealm,HTTPDigestAuthHandler,HTTPBasicAuthHandler,Request
from queue import Queue, Empty
from .core import valid,credentials

def subnet():
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    try:
        s.connect(('192.0.2.1',9));ip=s.getsockname()[0]
        if not ipaddress.ip_address(ip).is_private:raise ValueError('Brak lokalnego IPv4')
        return ipaddress.ip_network(ip+'/24',strict=False)
    finally:s.close()

def probe(host,port=554,timeout=0.7):
    try:
        with socket.create_connection((host,int(port)),timeout=timeout) as s:
            s.settimeout(timeout)
            s.sendall(('OPTIONS rtsp://%s:%s/ RTSP/1.0\r\nCSeq: 1\r\n\r\n'%(host,port)).encode())
            line=s.recv(512).split(b'\r\n')[0]
            if line.startswith((b'RTSP/1.0 ',b'RTSP/2.0 ')):return line.decode('ascii','replace')
    except (OSError,ValueError):pass
    return None

class Scanner:
    def __init__(self):
        self.results=[];self.running=False;self.error='';self._lock=threading.Lock();self._stop=threading.Event()
    def start(self,network=None):
        if self.running:return
        self._stop.clear();self.results=[];self.error='';self.running=True
        threading.Thread(target=self._run,args=(network,),daemon=True).start()
    def _run(self,network):
        try:
            net=ipaddress.ip_network(network,strict=False) if network else subnet()
            if net.version!=4 or not net.is_private or net.num_addresses>256:
                raise ValueError('Skan dozwolony tylko dla prywatnej podsieci /24 lub mniejszej')
            q=Queue()
            for ip in net.hosts():q.put(str(ip))
            def worker():
                while not self._stop.is_set():
                    try:ip=q.get_nowait()
                    except Empty:return
                    for port in (554,8554):
                        if self._stop.is_set():break
                        response=probe(ip,port)
                        if response:
                            with self._lock:self.results.append({'ip':ip,'port':port,'status':response})
                            break
            threads=[threading.Thread(target=worker,daemon=True) for _ in range(min(12,q.qsize()))]
            for t in threads:t.start()
            for t in threads:t.join()
        except Exception as e:self.error=str(e)
        finally:self.running=False
    def snapshot(self):
        with self._lock:return list(self.results)
    def stop(self):self._stop.set()

def jpeg(url,path):
    valid(url)
    p=urlsplit(url)
    if p.scheme not in ('http','https'):raise ValueError('Wymagany HTTP(S) JPEG')
    opener=build_opener()
    if p.username:
        clean=credentials(url,'','')
        pw=HTTPPasswordMgrWithDefaultRealm()
        pw.add_password(None,clean,unquote(p.username),unquote(p.password or ''))
        opener=build_opener(HTTPDigestAuthHandler(pw),HTTPBasicAuthHandler(pw))
        url=clean
    req=Request(url,headers={'User-Agent':'OpenCamView/2','Accept':'image/jpeg'})
    with opener.open(req,timeout=5) as res:data=res.read(2097153)
    if len(data)>2097152 or not data.startswith(b'\xff\xd8\xff') or not data.endswith(b'\xff\xd9'):
        raise ValueError('Serwer nie zwrocil poprawnego JPEG (maks 2 MiB)')
    if os.path.islink(path):raise ValueError('Niedozwolony plik')
    fd,tmp=tempfile.mkstemp(prefix='.ocv-img-',dir=os.path.dirname(path))
    try:
        os.fchmod(fd,0o600)
        with os.fdopen(fd,'wb') as f:f.write(data)
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
    return time.strftime('%H:%M:%S')
