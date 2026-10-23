"""Experimental on-demand local HTTP MPEG-TS proxy; requires FFmpeg and compatible hardware PiP."""
import http.server, socketserver, shutil, threading, subprocess, secrets
class Server(socketserver.ThreadingMixIn,http.server.HTTPServer):daemon_threads=True;allow_reuse_address=True
class Relay:
    def __init__(self,rtsp):self.rtsp=rtsp;self.server=None;self.process=None;self.path='/ocv-'+secrets.token_hex(12)
    def start(self):
        ffmpeg=shutil.which('ffmpeg')
        if not ffmpeg:raise RuntimeError('Brak ffmpeg w obrazie Enigma2')
        o=self
        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path!=o.path or self.client_address[0]!='127.0.0.1':self.send_error(404);return
                cmd=[ffmpeg,'-nostdin','-hide_banner','-loglevel','error','-rtsp_transport','tcp','-i',o.rtsp,'-map','0:v:0','-an','-c:v','copy','-f','mpegts','pipe:1']
                try:
                    o.process=subprocess.Popen(cmd,stdout=subprocess.PIPE,stdin=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                    self.send_response(200);self.send_header('Content-Type','video/mp2t');self.end_headers()
                    while o.process.poll() is None:
                        data=o.process.stdout.read(188*24)
                        if not data:break
                        self.wfile.write(data)
                except (OSError,BrokenPipeError,ConnectionResetError):pass
                finally:o.kill()
            def log_message(self,*args):pass
        self.server=Server(('127.0.0.1',0),Handler)
        threading.Thread(target=self.server.serve_forever,daemon=True).start()
        return 'http://127.0.0.1:%d%s'%(self.server.server_address[1],self.path)
    def kill(self):
        p=self.process;self.process=None
        if p:
            try:p.terminate();p.wait(timeout=2)
            except Exception:
                try:p.kill()
                except Exception:pass
    def stop(self):
        if self.server:self.server.shutdown();self.server.server_close();self.server=None
        self.kill()
